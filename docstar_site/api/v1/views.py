from rest_framework import views
from docstar_site.models import Doctor
from django.http import JsonResponse
from django.db.models import Q


class BaseDoctorApiView:

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


class SearchDoctorApiView(BaseDoctorApiView, views.APIView):

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query')
        if not query:
            return JsonResponse({'data': []}, status=200)

        doctors = Doctor.objects.filter(
            name__icontains=query
        )[:30].select_related('city', 'speciallity')

        doctors_list = self.prepare_doctors_data(doctors)

        return JsonResponse({'data': doctors_list}, status=200)


class FilterDoctorApiView(BaseDoctorApiView, views.APIView):

    def get(self, request, *args, **kwargs):
        city_list = request.GET.get('city')
        speciallity_list = request.GET.get('speciality')

        if not city_list and not speciallity_list:
            doctors = Doctor.objects.all().select_related('city', 'speciallity')
            doctors_list = self.prepare_doctors_data(doctors)
            return JsonResponse({'data': doctors_list}, status=200)

        city_query = Q()
        speciallity_query = Q()

        if city_list:
            city_query = Q(city__name__in=city_list.split(','))
        if speciallity_list:
            speciallity_query = Q(speciallity__name__in=speciallity_list.split(','))

        q_args = city_query & speciallity_query
        doctors = Doctor.objects.filter(q_args).select_related('city', 'speciallity')[:30]

        doctors_list = self.prepare_doctors_data(doctors)
        return JsonResponse({'data': doctors_list}, status=200)


class DoctorListApiView(BaseDoctorApiView, views.APIView):

    def get(self, request, *args, **kwargs):
        doctors = Doctor.objects.all().select_related('city', 'speciallity')

        doctors_list = self.prepare_doctors_data(doctors)
        return JsonResponse({'data': doctors_list}, status=200)
