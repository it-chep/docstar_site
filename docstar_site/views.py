from typing import List

from asgiref.sync import sync_to_async

from django.contrib.sites import requests
from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponse, JsonResponse
from django.forms import model_to_dict
from django.db import connection
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView
import requests

from docstar_site.clients.subscribers.dto import GetDoctorSubscribersResponse
from docstar_site.forms import CreateDoctorForm
from docstar_site.utils import *
from docstar_site.functions import *

import logging

logger = logging.getLogger(__name__)


@cache_page(60 * 60 * 10)
def page_not_found_view(request, exception):
    return render(request, 'docstar/404.html', status=404, )


def health_check(request):
    return JsonResponse({"status": "ok"}, status=200)


def e_handler500(request):
    return HttpResponse('<h1">Данной страницы не существует :(</h1>')


class CitySpeciallity:

    def get_citys(self):
        return City.objects.all()

    def get_speciallity(self):
        return Speciallity.objects.all()


class Doctors(TemplateView):
    template_name = "docstar/doctors.html"

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
                            having count(distinct doctor_id) != 0
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
                            having count(distinct doctor_id) != 0
                            order by s.name
                           """)

            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cities'] = self._prepare_cities_data(self._get_cities())
        context['specialities'] = self._prepare_specialities_data(self._get_specialities())
        context["new_doctor_banner"] = True
        return context


class DoctorDetail(DataMixin, DetailView):
    model = Doctor
    template_name = 'docstar/doctor_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        primary_city = self.object.city
        primary_city_id = primary_city.id
        cities = self.object.additional_cities.all().values("id", "name")

        context["title"] = f"{self.object.name}"

        context["city_help_text"] = "Город" if len(cities) == 1 else "Города"
        primary_city_text = f"{primary_city.name}" if len(cities) == 1 else f"{primary_city.name}, "
        context["additional_doctor_cities_str"] = primary_city_text + ", ".join(
            [city['name'] for city in cities if city["id"] != primary_city_id]
        )

        context["additional_doctor_specialities"] = self.object.additional_specialties.all().exclude(
            id=self.object.speciallity.id)

        return context

    def prepare_tg_url(self):
        tg = self.object.tg_url
        if not tg:
            return

        tg = tg.replace('@', "")
        if tg and "https" not in tg:
            self.object.tg_url = f"https://t.me/{tg}"

    def prepare_tg_channel_url(self):
        tg = self.object.tg_channel_url
        if not tg:
            return

        tg = tg.replace('@', "")
        if tg and "https" not in tg:
            self.object.tg_channel_url = f"https://t.me/{tg}"

    def prepare_doctor_link(self):
        doc_link = self.object.prodoctorov
        some_url = self.object.inst_url or self.object.tg_url or self.object.vk_url
        if doc_link and "http" not in doc_link and not doc_link[0:4] == "http":
            self.object.prodoctorov = some_url

    def enrich_doctor_subs(self):
        doctor_id = self.object.id
        subscribers_response: GetDoctorSubscribersResponse = settings.SUBSCRIBERS_CLIENT.get_doctor_subscribers(
            doctor_id
        )
        self.object.tg_subs_count = subscribers_response.tg_subs_count
        self.object.tg_subs_count_text = subscribers_response.tg_subs_count_text
        self.object.tg_last_updated_date = subscribers_response.tg_last_updated_date

        self.object.inst_subs_count = subscribers_response.inst_subs_count
        self.object.inst_subs_count_text = subscribers_response.inst_subs_count_text
        self.object.inst_last_updated_date = subscribers_response.inst_last_updated_date
        return

    def get(self, request, *args, **kwargs):
        self.object: Doctor = self.get_object()
        self.prepare_tg_url()
        self.prepare_tg_channel_url()
        self.prepare_doctor_link()

        self.enrich_doctor_subs()

        context = self.get_context_data()
        return self.render_to_response(context)


class NewClubParticipantView(TemplateView):
    template_name = "docstar/new_club_participant.html"
    form_class = CreateDoctorForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["form"] = self.form_class
        return context


class WelcomeView(TemplateView):
    template_name = "docstar/welcome_to_base.html"


class SpasiboClubParticipantView(TemplateView):
    template_name = "docstar/spasibo_club_participant.html"


class DoctorsApiView(APIView):

    def get(self, request):
        docs = User.objects.all().values()
        return Response({"doc": list(docs)})

    def post(self, request):
        new_doc = User.objects.create(
            name=request.data['name'],
        )
        return Response({'doc': model_to_dict(new_doc)})


def getcourse_get_api(request):
    try:
        export_id = GetCourseExportID.objects.latest('export_time')

        # Экспрот пользователей по круппе клуб докстар
        response = requests.get(
            f'https://{settings.GK_ACCOUNT_NAME}.getcourse.ru/pl/api/account/exports/{export_id}?key={settings.GK_KEY}')
        data = response.json()["info"]["items"]

        city_list = [k.name for k in City.objects.all()]
        spec_list = [j.name for j in Speciallity.objects.all()]

        for i in range(len(data)):

            city = validate_foreign(data[i][33], 0, city_list, spec_list)
            spec = validate_foreign(0, data[i][28], city_list, spec_list)

            validated_data = get_params(data[i])
            try:
                doc = Doctor.objects.get(email=validated_data['email'])
                doc.inst_url = validated_data['inst_url']
                doc.vk_url = validated_data['vk_url']
                doc.dzen_url = validated_data['dzen_url']
                doc.tg_url = validated_data['tg_url']
                doc.subscribers_inst = validated_data['subs']
                doc.additional_speciallity = validated_data['additional_speciallity']
                doc.main_blog_theme = validated_data['main_theme']
                doc.medical_directions = validated_data['medical_direcion']
                doc.city = City.objects.get(name=city)
                doc.speciallity = Speciallity.objects.get(name=spec)
                doc.prodoctorov = validated_data['prodoc']
                doc.save()

                logger.info(f'Обновлён пользователь {doc}')
            except ObjectDoesNotExist:
                continue

        return render(request, 'base.html', {'title': 'Обнова'})

    except Exception as ex:
        logger.error(ex)


@sync_to_async
def Get_gk_email_result(request):
    try:
        exp_id = GetCourseExportID.objects.latest('export_time').export_id
        email = request.GET["email"]

        # Экспрот пользователей по круппе клуб докстар
        response = requests.get(
            f'https://{settings.GK_ACCOUNT_NAME}.getcourse.ru/pl/api/account/exports/{exp_id}?key={settings.GK_KEY}')

        if response is None:
            return render(request, 'docstar/404.html')

        data = response.json()["info"]["items"]

        for item in data:
            if email in item[1] and email != "":
                return render(request, 'docstar/result_gk.html', {'answer': 'Отлично, вы есть в клубе )',
                                                                  'result': 1, 'title': 'Успешная проверка'})

        return render(request, 'docstar/result_gk.html', {'answer': 'К сожалению, вас нет в клубе (', 'result': 0,
                                                          'title': 'Купи клуб'})

    except Exception as ex:
        logger.error(ex)


def get_gk_email(request):
    return render(request, 'docstar/chek_gk.html', {'title': 'Проверка на подлинность'})


class DoctorApiView(APIView):
    queryset = Doctor.objects.all()

    def post(self, request):
        vals = Doctor.objects.all().values()
        return Response({'docs': list(vals)})

    def get(self, request):

        try:
            city_name = City.objects.get(name=self.request.GET.get('city'))
            spec_name = Speciallity.objects.get(name=self.request.GET.get('speciallity'))
            slug = get_eng_slug(text=self.request.GET.get('name')).split()
            new_slug = "-".join(slug).lower()

            new_doc = Doctor.objects.create(
                name=self.request.GET.get('name'),
                slug=new_slug,
                # "slug": "agaverdieva-aida-mamedovna",
                email=self.request.GET.get('email'),
                inst_url=self.request.GET.get('inst_url'),
                vk_url=self.request.GET.get('vk_url'),
                dzen_url=self.request.GET.get('dzen_url'),
                tg_url=self.request.GET.get('tg_url'),
                medical_directions=self.request.GET.get('medical_directions'),
                speciallity=spec_name,
                city=city_name,
                additional_speciallity=self.request.GET.get('additional_speciallity'),
                main_blog_theme=self.request.GET.get('main_blog_theme'),
                status_club=self.request.GET.get('status_club'),
                avatar="user_photos/zag.png",
                prodoctorov=self.request.GET.get('prodoc'),
                subscribers_inst=self.request.GET.get('subscribers_inst')
            )

            logger.info(f'Создан новый пользователь, {new_doc}')

            return Response({'status': 200})

        except Exception as ex:
            logger.error(ex)
