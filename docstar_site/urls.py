from django.urls import path
from django.views.decorators.cache import cache_page

from docstar_site.views import (
    health_check,
    spasibo_book,
    NewClubParticipantView,
    SpasiboClubParticipantView,
    ShowDoc,
    Doctors,
)

urlpatterns = [
    path("health/", health_check, name="health_check"),

    path('spasibo_book/', spasibo_book, name='spasibo_book'),
    path('new_club_participant/', NewClubParticipantView.as_view(), name="new_club_participant"),
    path('spasibo_club_participant/', SpasiboClubParticipantView.as_view(), name="spasibo_club_participant"),

    path('<slug:slug>/', ShowDoc.as_view(), name='doctor_card'),

    path('', cache_page(60 * 60 * 10)(Doctors.as_view()), name='homepage'),
]
