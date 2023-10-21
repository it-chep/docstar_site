from django.urls import path, include

from vpn.views import *


urlpatterns = [
    path('get_statistic/', get_statistic_vpn, name='get_statistic'),
    path('get_statistic_all/', get_statistic_all_vpn, name='get_statistic_all'),
    path('get_statistic_all_bot/', get_statistic_all_vpn_bot, name='get_statistic_all'),

    path('create_client/', create_client_vpn, name='create_client'),
    path('create_blogger/', create_blogger_vpn, name='create_blogger'),
]

