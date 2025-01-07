import math

from rest_framework import views
from docstar_site.models import Doctor
from django.http import JsonResponse
from django.db.models import Q
from django.conf import settings


class BaseDoctorApiView:
    limit = settings.LIMIT_DOCTORS_ON_PAGE

    @staticmethod
    def prepare_doctors_data(doctors) -> list[dict]:
        doctors_list = []
        for doctor in doctors:
            doctors_list.append({
                'name': doctor.name,
                'city': doctor.city.name,
                'speciality': doctor.speciallity.name,
                'avatar_url': doctor.avatar.url if doctor.avatar else None,
                'doctor_url': doctor.get_absolute_url(),
            })
        return doctors_list

    def get_pages_and_doctors_with_offset(self, current_page: int, doctors):

        pages = max(math.ceil(len(doctors) / settings.LIMIT_DOCTORS_ON_PAGE), 1)

        if current_page == 1:
            doctors = doctors[:self.limit]
        else:
            current_page -= 1
            offset = current_page * settings.LIMIT_DOCTORS_ON_PAGE
            doctors = doctors[offset:offset + self.limit]

        return pages, doctors


class SearchDoctorApiView(BaseDoctorApiView, views.APIView):

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query')
        if not query:
            return JsonResponse({'data': []}, status=200)

        doctors = Doctor.objects.filter(
            name__icontains=query,
            is_active=True,
        ).order_by('name')[:self.limit].select_related('city', 'speciallity')

        doctors_list = self.prepare_doctors_data(doctors)

        return JsonResponse({'data': doctors_list}, status=200)


class FilterDoctorApiView(BaseDoctorApiView, views.APIView):

    def get(self, request, *args, **kwargs):
        city_list = request.GET.get('city')
        speciallity_list = request.GET.get('speciality')
        current_page = int(request.GET.get('page', 1))

        if not city_list and not speciallity_list:
            doctors = Doctor.objects.filter(is_active=True).order_by('name').select_related('city', 'speciallity')
            pages, doctors = self.get_pages_and_doctors_with_offset(current_page, doctors)
            doctors_list = self.prepare_doctors_data(doctors)
            return JsonResponse({'data': doctors_list, 'pages': pages, 'page': current_page}, status=200)

        city_query = Q()
        speciallity_query = Q()

        if city_list:
            city_query = Q(city__name__in=city_list.split(','))
        if speciallity_list:
            speciallity_query = Q(speciallity__name__in=speciallity_list.split(','))

        q_args = city_query & speciallity_query
        doctors = Doctor.objects.filter(
            q_args,
            is_active=True,
        ).order_by('name').select_related('city', 'speciallity')

        pages, doctors = self.get_pages_and_doctors_with_offset(current_page, doctors)

        doctors_list = self.prepare_doctors_data(doctors)

        return JsonResponse({'data': doctors_list, 'pages': pages, 'page': current_page}, status=200)


class DoctorListApiView(BaseDoctorApiView, views.APIView):

    def get(self, request, *args, **kwargs):
        current_page = int(request.GET.get('page', 1))

        doctors = Doctor.objects.filter(is_active=True).order_by('name').select_related('city', 'speciallity')
        pages, doctors = self.get_pages_and_doctors_with_offset(current_page, doctors)
        doctors_list = self.prepare_doctors_data(doctors)

        return JsonResponse({'data': doctors_list, 'pages': pages, 'page': current_page}, status=200)
