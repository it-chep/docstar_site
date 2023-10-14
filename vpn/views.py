import datetime
import json
from json import JSONDecodeError

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse, JsonResponse
from django.utils.text import slugify
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError

from vpn.utils import validate_vpn_save_data_error
from vpn.decorators import validate_json_request
from vpn.forms import ClientFilterForm, BloggerFilterForm
from vpn.models import *
from vpn.filters import filter_date_from_param


# Только для salebot
@csrf_exempt
@validate_json_request
def get_statistic_vpn(request: HttpRequest, data: dict = None):
    price = 1900
    last_month_start = datetime.date.today() - datetime.timedelta(days=30)

    if request.method == "POST":

        try:
            sb_id = data['sb_id']
        except KeyError:
            return HttpResponse(status=500, content='Отсутствует необходимый параметр sb_id')

        blogger = Blogger.objects.filter(sb_id=sb_id).first()
        if blogger:
            utm = blogger.utm
            if utm is None:
                return HttpResponse(status=400, content='У данного блогера нет utm метки')
            discount = blogger.discount
            clients = Client.objects.filter(utm=utm)
            profit = price * discount * clients.count() / 100
            last_month_clients = clients.filter(registration_date_time__gte=last_month_start)
            last_month_profit = price * discount * last_month_clients.count() / 100

            response_data = {
                "count_clients": clients.count(),
                "profit": profit,
                "last_month_profit": last_month_profit
            }
            return JsonResponse(response_data)
        else:
            return HttpResponse(status=400, content='Блогера с таким sb_id не существует')


@csrf_exempt
def get_statistic_all_vpn(request: HttpRequest):
    clients = Client.objects.all()
    bloggers = Blogger.objects.all()

    client_filter_form = ClientFilterForm(request.GET)
    blogger_filter_form = BloggerFilterForm(request.GET)

    client_date_param = request.GET.get('client_date')
    if client_date_param:
        clients = filter_date_from_param(client_date_param, clients)

    # Фильтр по utm клиента
    client_utm_param = request.GET.get('client_utm')
    if client_utm_param:
        clients = clients.filter(utm=UTM.objects.filter(name=client_utm_param).first())

    # Фильтр по скидке блоггера
    blogger_discount_param = request.GET.get('blogger_discount')
    if blogger_discount_param:
        bloggers = bloggers.filter(discount=blogger_discount_param)

    # Фильтр по дате блоггера
    blogger_date_param = request.GET.get('blogger_date')
    if blogger_date_param:
        bloggers = filter_date_from_param(blogger_date_param, bloggers)

    context = {
        'clients': clients,
        'bloggers': bloggers,
        'clients_count': clients.count(),
        'bloggers_count': bloggers.count(),
        'client_filter_form': client_filter_form,
        'blogger_filter_form': blogger_filter_form,
    }

    return render(request, 'vpn/all_statistic.html', context)


@csrf_exempt
def get_statistic_all_vpn_bot(request: HttpRequest):
    if request.method == "POST":
        clients = Client.objects.all().count()
        bloggers = Blogger.objects.all().count()
        return JsonResponse(status=200, data={'clients': clients, 'blogger': bloggers})


@csrf_exempt
@validate_json_request
def create_client_vpn(request: HttpRequest, data: dict = None):
    blogger = None

    if request.method == "POST":

        name = data.get('name', 'default')
        username = data.get('username', '')
        try:
            tg_id = data['tg_id']
            sb_id = data['sb_id']
            gk_id = data['gk_id']
        except KeyError:
            return HttpResponse(status=500, content='Отсутствуют необходимые параметры tg_id, sb_id, gk_id')

        utm_source = data.get('utm_source')
        utm = UTM.objects.filter(name=utm_source).first()
        if utm is not None:
            blogger = Blogger.objects.filter(utm=utm).first()

        client = Client(
            name=name,
            username=username,
            tg_id=tg_id,
            sb_id=sb_id,
            gk_id=gk_id,
            utm=utm,
            blogger=blogger
        )
        try:
            client.save()
        except IntegrityError as e:
            return validate_vpn_save_data_error(e)
        except ValueError:
            return HttpResponse(status=500, content='Поля sb_id, gk_id и tg_id должны быть числом')

        return HttpResponse(status=200, content='Пользователь сохранен')


@csrf_exempt
@validate_json_request
def create_blogger_vpn(request: HttpRequest, data: dict = None):
    if request.method == "POST":

        name = data.get('name', 'default')
        username = data.get('username', '')

        try:
            tg_id = data['tg_id']
            sb_id = data['sb_id']
        except KeyError:
            return HttpResponse(status=500, content='Отсутствуют необходимые параметры tg_id, sb_id')

        blogger = Blogger(
            name=name,
            username=username,
            tg_id=tg_id,
            sb_id=sb_id,
        )

        try:
            blogger.save()
        except IntegrityError as e:
            return validate_vpn_save_data_error(e)
        except ValueError:
            return HttpResponse(status=500, content='Поля sb_id и tg_id должны быть числом')

        return HttpResponse(status=200, content='Пользователь сохранен')
