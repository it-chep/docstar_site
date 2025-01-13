from django.urls import path, include

from .views import (
    SearchDoctorApiView,
    FilterDoctorApiView,
    DoctorListApiView,
    CreateNewDoctorApiView,
)

urlpatterns = [
    path("select2/", include("docstar_site.api.v1.select2.urls")),

    path(
        'doctor-list/',
        DoctorListApiView.as_view(),
        name='doctor-list'
    ),
    path(
        "search-doctor/",
        SearchDoctorApiView.as_view(),
        name="search-doctor",
    ),
    path(
        "filter-doctor/",
        FilterDoctorApiView.as_view(),
        name="filter-doctor"
    ),
    path(
        "create_new_doctor/",
        CreateNewDoctorApiView.as_view(),
        name="create_new_doctor"
    ),
]
