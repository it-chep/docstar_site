import math
import requests
from django.db.models import Count

from django.http import JsonResponse
from django.db.models import Q, QuerySet
from django.conf import settings
from django.urls import reverse, NoReverseMatch
from rest_framework import views, status

from docstar_site.clients.s3.client import DEFAULT_DOCTOR_IMAGE
from docstar_site.clients.subscribers.dto import FilterDoctorsRequest

from docstar_site.models import Doctor, Speciallity, City
from docstar_site.forms import CreateDoctorForm
from docstar_site.utils import get_site_url


class BaseDoctorApiView:
    limit = settings.LIMIT_DOCTORS_ON_PAGE
    search_speciality_limit = settings.LIMIT_SPECIALITY_ON_SEARCH
    search_city_limit = settings.LIMIT_CITY_ON_SEARCH

    @staticmethod
    def prepare_doctors_data(doctors) -> list[dict]:
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
    def enrich_photo_from_s3(doctors_list) -> list:
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
    def prepare_cities_data(cities: QuerySet) -> list[dict]:
        cities_list = []
        for city in cities:
            cities_list.append({
                'id': city.id,
                'name': city.name,
                'doctors_count': city.doctors_count,
            })

        return cities_list

    @staticmethod
    def prepare_specialities_data(specialities: QuerySet) -> list[dict]:
        specialities_list = []
        for speciality in specialities:
            specialities_list.append({
                'id': speciality.id,
                'name': speciality.name,
                'doctors_count': speciality.doctors_count,
            })

        return specialities_list

    def get_pages_and_doctors_with_offset(self, current_page: int, doctors):

        pages = max(math.ceil(len(doctors) / settings.LIMIT_DOCTORS_ON_PAGE), 1)

        if current_page == 1:
            doctors = doctors[:self.limit]
        else:
            current_page -= 1
            offset = current_page * settings.LIMIT_DOCTORS_ON_PAGE
            doctors = doctors[offset:offset + self.limit]

        return pages, doctors

    @staticmethod
    def get_offset(current_page: int) -> int:
        if current_page <= 1:
            offset = 0
        else:
            offset = current_page * settings.LIMIT_DOCTORS_ON_PAGE

        return offset

    def get_doctors(self, request, *args, **kwargs):
        city_list = request.GET.get('city')
        speciallity_list = request.GET.get('speciality')
        current_page = int(request.GET.get('page', 1))

        if not city_list and not speciallity_list:
            doctors = Doctor.objects.filter(is_active=True).order_by('name').select_related('city', 'speciallity')
            pages, doctors = self.get_pages_and_doctors_with_offset(current_page, doctors)
            doctors_list = self.enrich_photo_from_s3(self.prepare_doctors_data(doctors))
            return JsonResponse({'data': doctors_list, 'pages': pages, 'page': current_page}, status=status.HTTP_200_OK)

        city_query = Q()
        speciallity_query = Q()

        if city_list:
            city_query = Q(city__id__in=city_list.split(','))
        if speciallity_list:
            speciallity_query = Q(speciallity__id__in=speciallity_list.split(','))

        q_args = city_query & speciallity_query
        doctors = Doctor.objects.filter(
            q_args,
            is_active=True,
        ).order_by('name').select_related('city', 'speciallity')

        pages, doctors = self.get_pages_and_doctors_with_offset(current_page, doctors)

        doctors_list = self.enrich_photo_from_s3(self.prepare_doctors_data(doctors))

        return JsonResponse({'data': doctors_list, 'pages': pages, 'page': current_page}, status=status.HTTP_200_OK)

    def get_doctors_by_ids(self, request, doctor_ids, *args, **kwargs):
        city_list = request.GET.get('city')
        speciality_list = request.GET.get('speciality')
        current_page = int(request.GET.get('page', 1))

        city_query = Q()
        speciality_query = Q()

        if city_list:
            city_query = Q(city__id__in=city_list.split(','))
        if speciality_list:
            speciality_query = Q(speciallity__id__in=speciality_list.split(','))

        q_args = city_query & speciality_query
        doctors = Doctor.objects.filter(
            q_args,
            is_active=True,
            id__in=doctor_ids,
        ).order_by('name').select_related('city', 'speciallity')

        pages, doctors = self.get_pages_and_doctors_with_offset(current_page, doctors)

        doctors_list = self.enrich_photo_from_s3(self.prepare_doctors_data(doctors))

        return JsonResponse({'data': doctors_list, 'pages': pages, 'page': current_page}, status=status.HTTP_200_OK)

    def filter_doctors(self, request, *args, **kwargs):
        if request.GET.get('max_subscribers', None) or request.GET.get('min_subscribers', None):
            doctor_ids = settings.SUBSCRIBERS_CLIENT.filter_doctors_ids(
                FilterDoctorsRequest(
                    social_media="tg",
                    offset=self.get_offset(current_page=int(request.GET.get('page', 1))),
                    limit=settings.LIMIT_DOCTORS_ON_PAGE,
                    max_subscribers=request.GET.get('max_subscribers', 100_000),
                    min_subscribers=request.GET.get('min_subscribers', 300),
                )
            )

            return self.get_doctors_by_ids(request, doctor_ids, *args, **kwargs)

        return self.get_doctors(request, *args, **kwargs)


class SearchDoctorApiView(BaseDoctorApiView, views.APIView):

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query')
        if not query:
            return JsonResponse({'data': []}, status=status.HTTP_200_OK)

        # Специальности
        specialities = Speciallity.objects.filter(
            name__icontains=query,
        ).annotate(
            doctors_count=Count('doctor', filter=Q(doctor__is_active=True))
        ).order_by('name')[:self.search_speciality_limit]

        # Города
        cities = City.objects.filter(
            name__icontains=query,
        ).annotate(
            doctors_count=Count('doctor', filter=Q(doctor__is_active=True))
        ).order_by('name')[:self.search_city_limit]

        # Доктора
        doctors = Doctor.objects.filter(
            name__icontains=query,
            is_active=True,
        ).order_by('name')[:self.limit].select_related('city', 'speciallity')

        # ковертация в json
        doctors_list = self.enrich_photo_from_s3(self.prepare_doctors_data(doctors))
        cities_list = self.prepare_cities_data(cities)
        specialities_list = self.prepare_specialities_data(specialities)

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


class CreateNewDoctorApiView(views.APIView):
    # todo при реге сохранять в subscribers
    form_class = CreateDoctorForm

    def post(self, request, *args, **kwargs):
        data = request.data
        form = self.form_class(data)
        try:
            if form.is_valid():
                doctor = form.save()
                self.send_data_to_google_script(doctor)
                self.notificator_bot(doctor)
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
    def send_data_to_google_script(doctor):
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
