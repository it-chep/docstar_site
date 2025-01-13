from django.urls import path
from docstar_site.api.v1.select2.views import CitySearchSelect2ApiView, SpecialitiesSearchSelect2ApiView

urlpatterns = [
    path(
        'cities/',
        CitySearchSelect2ApiView.as_view(),
        name='select2_cities',
    ),
    path(
        'specialities/',
        SpecialitiesSearchSelect2ApiView.as_view(),
        name='select2_specialities',
    ),
]
