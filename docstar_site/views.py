import os

from asgiref.sync import sync_to_async
from django.conf.urls import handler500
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites import requests
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, UpdateView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from time import sleep
import threading

# from new_site.urls import handler500
from .forms import UpdateDoc
from .models import *
from .utils import *
from django.http import HttpResponse, Http404
# from .serializers import DoctorSerializer
from .permissions import DoctorPermissionsMixin, MembersPermissionsMixin
from .Treads import get_export_id
from .functions import *
# from apscheduler.schedulers.blocking import BlockingScheduler

import logging

logger = logging.getLogger(__name__)

# GETCOURSE CONFIG
secret_key = '5yvK6Jxqvjn0XcLoaZhlEKgWVDi7OcIGoVSkPnV7bikIAtliZe2mekpuhCPlcXz9f6uLrkm67APEfS562u6FzB4SXo6vJy0Oa9qxo9K94M0g5DGRChkjPgZmHdXKYOE5'
account_name = 'readymama'
group_id = 1728991
# GETCOURSE CONFIG

# def Treads():
thread_1 = threading.Thread(target=get_export_id, daemon=True)
thread_1.start()


# thread_2 = BlockingScheduler()
# thread_2.start()

@cache_page(60*60*10)
def page_not_found_view(request, exception):
    return render(request, 'docstar/404.html', status=404, )


@cache_page(60*60*10)
def spasibo_book(request):
    # uid = {uid} & gkname = {first_name} & gkphone = {phone} & gkemail = {email}
    uid = request.GET.get("uid")
    gkname = request.GET.get("gkname")
    gkphone = request.GET.get("gkphone")
    gkemail = request.GET.get("gkemail")
    return render(request, 'docstar/docstar_book.html', {'uid': uid,
                                                         'gkname': gkname,
                                                         'gkphone': gkphone,
                                                         'gkemail': gkemail
                                                         })


def e_handler500(request):
    return HttpResponse('<h1">Данной страницы не существует :(</h1>')


# @cache_page(60*60*24)
# def index(request):
# return render(request, 'docstar/index.html', {'title': 'Главная страница', 'menu': menu})


class CitySpeciallity:

    def get_citys(self):
        return City.objects.all()

    def get_speciallity(self):
        return Speciallity.objects.all()


class Doctors(CitySpeciallity, DataMixin, ListView):
    model = Doctor
    template_name = "docstar/doctors.html"
    context_object_name = 'doctors'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Доктора")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Doctor.objects.all().select_related('city').select_related('speciallity')


class ShowDoc(DataMixin, DetailView):
    model = Doctor
    template_name = 'docstar/doctor_card.html'
    context_object_name = 'doctor'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['doctor'].name)
        if self.request.user.is_authenticated:
            email = self.request.user.email
        else:
            email = '123@yandex.ru'

        return dict(list(context.items()) + list(c_def.items()))


class Lections(DataMixin, ListView):
    model = Lection
    template_name = "docstar/tech_work.html"
    context_object_name = 'lections'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Лекции')
        return dict(list(context.items()) + list(c_def.items()))


class ShowLection(DataMixin, DetailView):
    model = Lection
    template_name = 'docstar/lection_card.html'
    context_object_name = 'lection'
    pk_url_kwarg = 'lection_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['lection'].lection_name)
        return dict(list(context.items()) + list(c_def.items()))


class DoctorsApiView(APIView):

    def get(self, request):
        docs = User.objects.all().values()
        return Response({"doc": list(docs)})

    def post(self, request):
        new_doc = User.objects.create(
            name=request.data['name'],
        )
        return Response({'doc': model_to_dict(new_doc)})


@sync_to_async
def getcourse_get_api(request):
    try:
        export_id = GetCourseExportID.objects.latest('export_time')

        response = requests.get(
            f'https://{account_name}.getcourse.ru/pl/api/account/exports/{export_id}?key={secret_key}')  # Экспрот пользователей по круппе клуб докстар
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

        return render(request, 'docstar/gk_respo.html', {'title': 'Обнова'})

    except Exception as ex:
        logger.error(ex)


class FilterDocViews(Doctors, CitySpeciallity, ListView):
    model = Doctor
    template_name = "docstar/doctors.html"

    def get_queryset(self):
        queryset = []
        queryset = Doctor.objects.filter(city__in=self.request.GET.getlist("city"),
                                         speciallity__in=self.request.GET.getlist("speciallity")).select_related(
            'city').select_related('speciallity')

        if not queryset:
            queryset = Doctor.objects.filter(
                Q(city__in=self.request.GET.getlist("city")) |
                Q(speciallity__in=self.request.GET.getlist("speciallity"))).select_related('city').select_related(
                'speciallity')

        if not queryset:
            queryset = Doctor.objects.all().select_related('city').select_related('speciallity')

        return queryset


@sync_to_async
def Get_gk_email_result(request):
    try:
        exp_id = GetCourseExportID.objects.latest('export_time').export_id
        email = request.GET["email"]

        response = requests.get(
            f'https://{account_name}.getcourse.ru/pl/api/account/exports/{exp_id}?key={secret_key}')  # Экспрот пользователей по круппе клуб докстар

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


@cache_page(60 * 60 * 10)
class DoctorUpdateView(DoctorPermissionsMixin, DataMixin, DetailView):
    model = Doctor
    template_name = 'docstar/edit_doc.html'
    form_class = UpdateDoc
    success_url = 'doctors'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обновление')
        if self.request.user.is_authenticated:
            print(self.request.user.email)
        else:
            email = '123@yandex.ru'

        return dict(list(context.items()) + list(c_def.items()))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        email_doc = kwargs['instance'].email
        user = self.request.user.email

        if user != email_doc:
            self.handle_no_permission()
        else:
            pass

        return kwargs


@cache_page(60 * 60 * 10)
def success_edit(request):
    return render(request, 'docstar/success_edit.html', {'title': 'Мое имя успех'})


class AvaUpdate(UpdateView):
    model = Doctor
    form_class = UpdateDoc
    template_name = 'docstar/edit_doc.html'
    success_url = '/'

    def save(self):
        try:
            form = UpdateDoc(self.request.POST or None)
            if form.is_valid():
                form.save()
                # validate user + remove old photo
                # os.remove()
                return redirect('success')
        except Exception as ex:
            logger.error(ex)


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
            print(new_slug)

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

            # print(self.request.GET.get('name'),
            #     new_slug,
            #     # "slug": "agaverdieva-aida-mamedovna",
            #     self.request.GET.get('email'),
            #     self.request.GET.get('inst_url'),
            #     self.request.GET.get('vk_url'),
            #     self.request.GET.get('dzen_url'),
            #     self.request.GET.get('tg_url'),
        # ----     self.request.GET.get('medical_directions'),
            #     spec_name,
            #     city_name,
            #     self.request.GET.get('additional_speciallity'),
        #----     self.request.GET.get('main_blog_theme'),
            #     self.request.GET.get('status_club'),
            #     "user_photos/zag.png",
            #     self.request.GET.get('prodoc'),
            #     self.request.GET.get('subscribers_inst'))

            # new_city=City.objects.create(
            #     name=self.request.GET.get('city'),
            #     code=0
            # )
            print(f'new_city')
            logger.info(f'Создан новый пользователь, {new_doc}')

            return Response({'status': 200})

        except Exception as ex:
            logger.error(ex)
