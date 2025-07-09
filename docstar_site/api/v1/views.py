import math
from typing import List

import requests

from django.http import JsonResponse
from django.db import connection
from django.db.models import Q
from django.conf import settings
from django.urls import reverse, NoReverseMatch
from rest_framework import views, status

from docstar_site.clients.s3.client import DEFAULT_DOCTOR_IMAGE
from docstar_site.clients.subscribers.dto import FilterDoctorsRequest

from docstar_site.models import Doctor, Speciallity, City
from docstar_site.forms import CreateDoctorForm
from docstar_site.utils import get_site_url, validate_tg_channel_url, validate_inst_url


class CitySpecialityMixin:
    @staticmethod
    def _prepare_cities_data(cities: List[dict]) -> list[dict]:
        """Сериализация города из базы"""
        cities_list = []
        for city in cities:
            cities_list.append({
                'id': city["city_id"],
                'name': city["city_name"],
                'doctors_count': city["doctors_count"],
            })

        return cities_list

    @staticmethod
    def _prepare_specialities_data(specialities: List[dict]) -> list[dict]:
        """Сериализация специальности из базы"""
        specialities_list = []
        for speciality in specialities:
            specialities_list.append({
                'id': speciality["speciality_id"],
                'name': speciality["speciality_name"],
                'doctors_count': speciality["doctors_count"],
            })

        return specialities_list


class BaseDoctorApiView(CitySpecialityMixin):
    limit = settings.LIMIT_DOCTORS_ON_PAGE
    search_speciality_limit = settings.LIMIT_SPECIALITY_ON_SEARCH
    search_city_limit = settings.LIMIT_CITY_ON_SEARCH

    @staticmethod
    def configure_doctors_map(doctors):
        doctors_dict = dict()
        for doctor in doctors:
            try:
                reverse('doctor_card', kwargs={'slug': doctor.slug})
            except NoReverseMatch as e:
                continue

            doctors_dict[doctor.id] = {
                'name': doctor.name,
                'city': ", ".join(doctor.additional_cities.all().values_list("name", flat=True)),
                'slug': doctor.slug,
                'speciality': ", ".join(doctor.additional_specialties.all().values_list("name", flat=True)),
                'doctor_url': doctor.get_absolute_url(),
                'local_file': doctor.get_local_file,
                'tg_channel_url': doctor.tg_channel_url,
                'inst_url': doctor.inst_url,
            }

        return doctors_dict

    @staticmethod
    def enrich_subscribers(doctors_dict, subscribers_dict) -> dict:
        for doctor_id, doctor_data in doctors_dict.items():
            # Проверяем, что doctor_data является словарем
            if not isinstance(doctor_data, dict):
                continue

            # Получаем данные о подписчиках
            subscriber_data = subscribers_dict.get(doctor_id)

            if subscriber_data:
                doctor_data.update({
                    "tg_subs_count": subscriber_data.tg_subs_count,
                    "tg_subs_count_text": subscriber_data.tg_subs_count_text,
                    "inst_subs_count": subscriber_data.inst_subs_count,
                    "inst_subs_count_text": subscriber_data.inst_subs_count_text,
                })
            else:
                doctor_data.update({
                    "tg_subs_count": 0,
                    "tg_subs_count_text": "подписчиков",
                    "inst_subs_count": 0,
                    "inst_subs_count_text": "подписчиков",
                })

        return doctors_dict

    @staticmethod
    def prepare_doctors_data(doctors) -> list[dict]:
        """Сериализация queryset докторов"""
        doctors_list = []
        for doctor in doctors:
            try:
                reverse('doctor_card', kwargs={'slug': doctor.slug})
            except NoReverseMatch as e:
                continue

            doctors_list.append({
                'name': doctor.name,
                'city': doctor.city.name,
                'slug': doctor.slug,
                'speciality': doctor.speciallity.name,
                'doctor_url': doctor.get_absolute_url(),
                'local_file': doctor.get_local_file,
            })
        return doctors_list

    @staticmethod
    def enrich_photo_from_s3_map(doctors_map: dict) -> list:
        photos_map = settings.S3_CLIENT.get_user_photos()
        enriched_photos = []

        for _, doctor in doctors_map.items():
            # Дефолтно s3
            doctor['avatar_url'] = photos_map.get(doctor['slug'], None)

            # Если нет ни в s3 ни на серваке, то ставим заглушку
            if not doctor['avatar_url']:
                doctor['avatar_url'] = DEFAULT_DOCTOR_IMAGE

                # Если фотка на серваке, то отображаем ее для обратной совместимости
                if doctor['local_file']:
                    doctor['avatar_url'] = doctor['local_file']

            enriched_photos.append(doctor)

        return enriched_photos

    @staticmethod
    def enrich_photo_from_s3(doctors_list) -> list:
        """Обогащение карточек докторов фотографиями с S3"""
        photos_map = settings.S3_CLIENT.get_user_photos()
        enriched_photos = []

        for doctor in doctors_list:
            # Дефолтно s3
            doctor['avatar_url'] = photos_map.get(doctor['slug'], None)

            # Если нет ни в s3 ни на серваке, то ставим заглушку
            if not doctor['avatar_url']:
                doctor['avatar_url'] = DEFAULT_DOCTOR_IMAGE

                # Если фотка на серваке, то отображаем ее для обратной совместимости
                if doctor['local_file']:
                    doctor['avatar_url'] = doctor['local_file']

            enriched_photos.append(doctor)

        return enriched_photos

    @staticmethod
    def prepare_cities_data(cities: List[dict]) -> list[dict]:
        cities_list = []
        for city in cities:
            cities_list.append({
                'id': city["city_id"],
                'name': city["city_name"],
                'doctors_count': city["doctors_count"],
            })

        return cities_list

    @staticmethod
    def prepare_specialities_data(specialities: List[dict]) -> list[dict]:
        specialities_list = []
        for speciality in specialities:
            specialities_list.append({
                'id': speciality["speciality_id"],
                'name': speciality["speciality_name"],
                'doctors_count': speciality["doctors_count"],
            })

        return specialities_list

    @staticmethod
    def get_city_speciality_query_args(city_list, speciality_list):
        city_query = Q()
        speciality_query = Q()

        if city_list:
            city_query = Q(
                additional_cities__id__in=city_list.split(',')
            ) | Q(
                city__id__in=city_list.split(',')
            )
        if speciality_list:
            speciality_query = Q(
                additional_specialties__id__in=speciality_list.split(',')
            ) | Q(
                speciallity__id__in=speciality_list.split(',')
            )

        return city_query & speciality_query

    def get_pages_and_doctors_with_offset(self, current_page: int, doctors):
        """Получение данных для пагинации, отрезание по лимиту"""
        pages = max(math.ceil(len(doctors) / settings.LIMIT_DOCTORS_ON_PAGE), 1)

        if current_page == 1:
            doctors = doctors[:self.limit]
        else:
            current_page -= 1
            offset = current_page * settings.LIMIT_DOCTORS_ON_PAGE
            doctors = doctors[offset:offset + self.limit]

        return pages, doctors

    def get_doctors(self, request, *args, **kwargs):
        """Фильтрация докторов по QUERY параметрам"""
        city_list = request.GET.get('city')
        speciality_list = request.GET.get('speciality')
        current_page = int(request.GET.get('page', 1))

        if not city_list and not speciality_list:
            doctors = (
                Doctor.objects.filter(is_active=True).
                order_by('name').
                select_related('city', 'speciallity').
                prefetch_related('additional_cities', 'additional_specialties')
            )
            pages, doctors = self.get_pages_and_doctors_with_offset(current_page, doctors)
            doctors_ids = [doctor.id for doctor in doctors]
            subscribers_map = settings.SUBSCRIBERS_CLIENT.get_subscribers_by_doctors_ids(doctors_ids)

            doctors_map = self.configure_doctors_map(doctors)
            enriched_by_subscribers_map = self.enrich_subscribers(doctors_map, subscribers_map)
            doctors_list = self.enrich_photo_from_s3_map(enriched_by_subscribers_map)

            return JsonResponse({'data': doctors_list, 'pages': pages, 'page': current_page}, status=status.HTTP_200_OK)

        q_args = self.get_city_speciality_query_args(city_list, speciality_list)

        doctors = (
            Doctor.objects.filter(
                q_args,
                is_active=True,
            ).
            order_by('name').
            select_related('city', 'speciallity').
            prefetch_related('additional_cities', 'additional_specialties').
            distinct()
        )

        pages, doctors = self.get_pages_and_doctors_with_offset(current_page, doctors)

        doctors_ids = [doctor.id for doctor in doctors]
        subscribers_map = settings.SUBSCRIBERS_CLIENT.get_subscribers_by_doctors_ids(doctors_ids)

        doctors_map = self.configure_doctors_map(doctors)
        enriched_by_subscribers_map = self.enrich_subscribers(doctors_map, subscribers_map)
        doctors_list = self.enrich_photo_from_s3_map(enriched_by_subscribers_map)

        return JsonResponse({'data': doctors_list, 'pages': pages, 'page': current_page}, status=status.HTTP_200_OK)

    def get_doctors_by_ids_with_subs(self, request, doctors_with_subs, *args, **kwargs):
        city_list = request.GET.get('city')
        speciality_list = request.GET.get('speciality')
        current_page = int(request.GET.get('page', 1))

        q_args = self.get_city_speciality_query_args(city_list, speciality_list)

        doctor_ids = []
        for doctor in doctors_with_subs:
            doctor_ids.append(doctor.doctor_id)

        doctors = (
            Doctor.objects.filter(
                q_args,
                is_active=True,
                id__in=doctor_ids,
            ).
            order_by('name').
            select_related('city', 'speciallity').
            prefetch_related('additional_cities', 'additional_specialties').
            distinct()
        )

        pages, doctors = self.get_pages_and_doctors_with_offset(current_page, doctors)

        doctors_map = self.configure_doctors_map(doctors)
        for doctor in doctors_with_subs:
            if doctors_map.get(doctor.doctor_id):
                doctors_map[doctor.doctor_id]["tg_subs_count"] = doctor.tg_subs_count
                doctors_map[doctor.doctor_id]["tg_subs_count_text"] = doctor.tg_subs_count_text
                doctors_map[doctor.doctor_id]["inst_subs_count"] = doctor.inst_subs_count
                doctors_map[doctor.doctor_id]["inst_subs_count_text"] = doctor.inst_subs_count_text

        doctors_list = self.enrich_photo_from_s3(doctors_map.values())

        return JsonResponse({'data': doctors_list, 'pages': pages, 'page': current_page}, status=status.HTTP_200_OK)

    def filter_doctors(self, request, *args, **kwargs):
        """Мини фасад либо отдает докторов по фильтрам либо ходит в сервис subscriber и фильтрует по ID"""
        max_subscribers = request.GET.get('max_subscribers', 100_000)
        min_subscribers = request.GET.get('min_subscribers', 300)
        social_media = request.GET.get('social_media', [])

        if (max_subscribers or min_subscribers) and (
                int(max_subscribers) != 100_000 or int(min_subscribers) != 300) or len(social_media) != 0:
            doctors = settings.SUBSCRIBERS_CLIENT.filter_doctors_ids(
                FilterDoctorsRequest(
                    social_media=social_media,
                    offset=0,
                    max_subscribers=max_subscribers,
                    min_subscribers=min_subscribers,
                )
            )
            if len(doctors) != 0:
                return self.get_doctors_by_ids_with_subs(request, doctors, *args, **kwargs)

        return self.get_doctors(request, *args, **kwargs)


class SearchDoctorApiView(BaseDoctorApiView, views.APIView):

    def get_cities_with_doctors(self, query) -> List[dict]:
        with connection.cursor() as cursor:
            cursor.execute(f"""
                            select c.id                      as city_id,
                                   c.name                    as city_name,
                                   count(distinct doctor_id) as doctors_count
                            from docstar_site_city c
                                     left join (select dc.city_id, dc.doctor_id
                                                from docstar_site_doctor_additional_cities dc
                                                         join docstar_site_doctor d on dc.doctor_id = d.id
                                                where d.is_active = true) as combined on c.id = combined.city_id
                            where c.name ilike %s                   
                            group by c.id, c.name
                            order by c.name
                            limit %s;
                           """, [f'%{query}%', self.search_city_limit])

            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_specialities_with_doctors(self, query) -> List[dict]:
        with connection.cursor() as cursor:
            cursor.execute(f"""
                            select s.id                      as speciality_id,
                                   s.name                    as speciality_name,
                                   count(distinct doctor_id) as doctors_count
                            from docstar_site_speciallity s
                                     left join (select dc.speciallity_id, dc.doctor_id
                                                from docstar_site_doctor_additional_specialties dc
                                                         join docstar_site_doctor d on dc.doctor_id = d.id
                                                where d.is_active = true) as combined on s.id = combined.speciallity_id
                            where s.name ilike %s                   
                            group by s.id, s.name
                            order by s.name
                            limit %s;
                           """, [f'%{query}%', self.search_speciality_limit])

            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query')
        if not query:
            return JsonResponse({'data': []}, status=status.HTTP_200_OK)

        # Специальности
        specialities = self.get_specialities_with_doctors(query)

        # Города
        cities = self.get_cities_with_doctors(query)

        # Доктора
        doctors = Doctor.objects.filter(
            name__icontains=query,
            is_active=True,
        ).order_by('name')[:self.limit].prefetch_related('additional_cities', 'additional_specialties')

        # ковертация в json
        doctors_list = self.enrich_photo_from_s3(self.prepare_doctors_data(doctors))
        cities_list = self._prepare_cities_data(cities)
        specialities_list = self._prepare_specialities_data(specialities)

        return JsonResponse(
            {
                'data': doctors_list,
                'cities': cities_list,
                'specialities': specialities_list,
            },
            status=status.HTTP_200_OK
        )


class FilterDoctorApiView(BaseDoctorApiView, views.APIView):
    def get(self, request, *args, **kwargs):
        return self.filter_doctors(request, *args, **kwargs)


class DoctorListApiView(BaseDoctorApiView, views.APIView):

    def get(self, request, *args, **kwargs):
        return self.filter_doctors(request, *args, **kwargs)


class CitiesListApiView(views.APIView):

    def get(self, request, *args, **kwargs):
        cities = City.objects.all().order_by('name')
        data = [{"city_id": city.id, "city_name": city.name} for city in cities]
        return JsonResponse(
            {"cities": data},
            status=status.HTTP_200_OK
        )


class SpecialityListApiView(views.APIView):

    def get(self, request, *args, **kwargs):
        specialities = Speciallity.objects.all().order_by('name')
        data = [{"speciality_id": spec.id, "speciality_name": spec.name} for spec in specialities]
        return JsonResponse(
            {"specialities": data},
            status=status.HTTP_200_OK
        )


class CreateNewDoctorApiView(views.APIView):
    form_class = CreateDoctorForm

    def post(self, request, *args, **kwargs):
        data = request.data
        form = self.form_class(data)
        try:
            if form.is_valid():
                doctor = form.save()

                self.send_data_to_google_script(doctor)
                self.notificator_bot(doctor)
                self.save_to_subscribers(doctor)

                return JsonResponse(
                    {
                        "redirect_url": reverse("spasibo_club_participant"),
                        "endpoint": reverse('doctor_card', kwargs={'slug': doctor.slug}),
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                return JsonResponse(
                    {"errors": form.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as ex:
            return JsonResponse(
                {"alert": "Произошла ошибка, пожалуйста обратитесь в техподдержку"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @staticmethod
    def save_to_subscribers(doctor):
        """Сохраняет пользователя в сервисе subscriber"""
        # todo негативные кейсы отработать
        client = settings.SUBSCRIBERS_CLIENT
        if not doctor.tg_channel_url:
            return None

        tg_username = validate_tg_channel_url(doctor.tg_channel_url)
        inst_username = validate_inst_url(doctor.instagram_url)

        return client.create_doctor(doctor.id, tg_username, inst_username)

    @staticmethod
    def send_data_to_google_script(doctor):
        """Отправляет данные в гугл таблицу"""
        data = {
            "name": doctor.name,
            "age": doctor.age,
            "birthday": doctor.birth_date.strftime("%d.%m.%Y"),
            "inst_url": doctor.inst_url,
            "vk_url": doctor.vk_url,
            "dzen_url": doctor.dzen_url,
            "tg_url": doctor.tg_url,
            "subscribers": doctor.subscribers_inst,
            "city": doctor.city.name,
            "medical_direction": doctor.medical_directions,
            "speciallity": doctor.speciallity.name,
            "additional_speciallity": doctor.additional_speciallity,
            "main_theme": doctor.main_blog_theme,
        }

        try:
            response = requests.post(settings.GOOGLE_SHEET_URL, data=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(e)

    @staticmethod
    def notificator_bot(doctor):
        """Уведомляет в бот о заполненной анкете в базе"""
        data = {
            "url": get_site_url() + reverse('doctor_card', kwargs={'slug': doctor.slug}),
            "name": doctor.name,
            "inst_url": doctor.inst_url,
            "tg_url": doctor.tg_url,
            "message": "doctor_on_site_notification",
            "client_id": settings.ADMIN_CHAT_ID
        }
        try:
            response = requests.post(settings.SALEBOT_API_URL, data=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(e)


class SettingsApiView(CitySpecialityMixin, views.APIView):
    @staticmethod
    def _get_doctors_count():
        """Возвращает количество активных врачей"""
        with connection.cursor() as cursor:
            cursor.execute(f"""
                            select count(*) as doctors_count
                            from docstar_site_doctor d
                            where d.is_active = true
                           """, )

            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def _get_cities() -> List[dict]:
        """Возвращает список городов с количеством врачей в каждом"""
        with connection.cursor() as cursor:
            cursor.execute(f"""
                            select c.id                      as city_id,
                                   c.name                    as city_name,
                                   count(distinct doctor_id) as doctors_count
                            from docstar_site_city c
                                     left join (select dc.city_id, dc.doctor_id
                                                from docstar_site_doctor_additional_cities dc
                                                         join docstar_site_doctor d on dc.doctor_id = d.id
                                                where d.is_active = true) as combined on c.id = combined.city_id
                            group by c.id, c.name
                            order by c.name
                           """, )

            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def _get_specialities() -> List[dict]:
        """Возвращает список специализаций с количеством врачей в каждой"""
        with connection.cursor() as cursor:
            cursor.execute(f"""
                            select s.id                      as speciality_id,
                                   s.name                    as speciality_name,
                                   count(distinct doctor_id) as doctors_count
                            from docstar_site_speciallity s
                                     left join (select dc.speciallity_id, dc.doctor_id
                                                from docstar_site_doctor_additional_specialties dc
                                                         join docstar_site_doctor d on dc.doctor_id = d.id
                                                where d.is_active = true) as combined on s.id = combined.speciallity_id
                            group by s.id, s.name
                            order by s.name
                           """)

            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def _serialize_doctors_count(data: List[dict]) -> int:
        """Сериализует данные о количестве врачей"""
        return data[0]['doctors_count'] if data else 0

    @staticmethod
    def _get_subscribers_info():
        return settings.SUBSCRIBERS_CLIENT.get_all_subscribers_info()

    @staticmethod
    def _get_filter_info():
        filtersDTO = settings.SUBSCRIBERS_CLIENT.filter_info()

        resp = list()
        for filterDTO in filtersDTO:
            resp.append({
                "name": filterDTO.name,
                "slug": filterDTO.slug,
            })

        return resp

    def get(self, request, *args, **kwargs):
        subscribers_info = self._get_subscribers_info()
        return JsonResponse(
            {
                'doctors_count': self._serialize_doctors_count(self._get_doctors_count()),
                'subscribers_count': subscribers_info.subscribers_count or 0,
                'subscribers_count_text': subscribers_info.subscribers_count_text,
                'subscribers_last_updated': subscribers_info.last_updated,
                'filter_info': self._get_filter_info(),
                'cities': self._prepare_cities_data(self._get_cities()),
                'specialities': self._prepare_specialities_data(self._get_specialities()),
                'new_doctor_banner': True,
            },
            status=status.HTTP_200_OK
        )
