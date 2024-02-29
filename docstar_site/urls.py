from django.urls import include
from django.views.decorators.cache import cache_page

from docstar_site.views import *
from docstar_site.admin import *
from docstar_site.cdek import process_request as cdek_view

urlpatterns = [
    path('spasibo_book/', spasibo_book, name='spasibo_book'),

    path('clinic/', Doctors.as_view(), name='clinic'),
    path('cdek/', cdek_view, name='cdek_view'),
    path('prelogin/', get_gk_email, name='chek_getcourse'),
    path('prelogin/check_club/', Get_gk_email_result, name='chek_getcourse_result'),

    path('lections/', Lections.as_view(), name='lections'),
    path('lections/<int:lection_id>/', ShowLection.as_view(), name='lection_card'),

    path('knowlege_base/', Lections.as_view(), name='knowleges'),
    path('knowlege_base/<int:knowlege_base_id>/', ShowLection.as_view(), name='knowleges_card'),

    path('get_new_data_gk/', getcourse_get_api, name='gk_data'),

    path('', cache_page(60 * 60 * 10)(Doctors.as_view()), name='homepage'),
    path('filter/', cache_page(60 * 60 * 12)(FilterDocViews.as_view()), name='doctors__filter'),
    path('<slug:slug>/', ShowDoc.as_view(), name='doctor_card'),
    path('<slug:slug>/edit/', AvaUpdate.as_view(), name='edit'),
    path('<slug:slug>/edit/success', success_edit, name='edit_photo'),
]
