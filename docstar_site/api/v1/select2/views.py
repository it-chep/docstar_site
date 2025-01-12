from django.http import JsonResponse
from django.core.paginator import Paginator

from rest_framework.views import APIView
from docstar_site.models import City, Speciallity


class CitySearchSelect2ApiView(APIView):

    def get(self, request):
        query = request.GET.get('q', '').strip()
        cities = City.objects.filter(name__icontains=query) if query else City.objects.all()
        results = [{"id": city.id, "name": city.name} for city in cities]
        return JsonResponse({
            "results": results,
        })


class SpecialitiesSearchSelect2ApiView(APIView):

    def get(self, request):
        query = request.GET.get('q', '').strip()
        specialities = Speciallity.objects.filter(name__icontains=query) if query else Speciallity.objects.all()
        results = [{"id": speciality.id, "name": speciality.name} for speciality in specialities]
        return JsonResponse({
            "results": results,
        })
