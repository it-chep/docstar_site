from django.urls import path

from .views import (
    SearchDoctorApiView,
    FilterDoctorApiView,
    DoctorListApiView,
)

urlpatterns = [
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
    )
]
