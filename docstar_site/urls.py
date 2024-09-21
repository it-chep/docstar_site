from django.urls import path

from docstar_site.views import *

urlpatterns = [
    path('spasibo_book/', spasibo_book, name='spasibo_book'),
    path('prelogin/', get_gk_email, name='chek_getcourse'),
    path('prelogin/check_club/', Get_gk_email_result, name='chek_getcourse_result'),
    path('filter/', cache_page(60 * 60 * 12)(FilterDocViews.as_view()), name='doctors__filter'),
    path('<slug:slug>/', ShowDoc.as_view(), name='doctor_card'),
    path('<slug:slug>/edit/', AvaUpdate.as_view(), name='edit'),
    path('<slug:slug>/edit/success', success_edit, name='edit_photo'),
    path('', cache_page(60 * 60 * 10)(Doctors.as_view()), name='homepage'),
]
