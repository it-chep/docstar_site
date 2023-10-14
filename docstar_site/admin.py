from django.contrib import admin
from django.http import HttpResponse
from django.template.defaulttags import url
from django.template.response import TemplateResponse
from django.views.generic import ListView, DetailView

from django.contrib import admin
from django.utils.html import escape
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import *
from django.urls import path


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'status_club', 'city', 'speciallity')
    prepopulated_fields = {"slug": ("name", )}


class ExportAdmin(admin.ModelAdmin):
    list_display = ('export_id', 'export_time')
    # prepopulated_fields = {"slug": ("name",)}
    # user_owned_objects_field = 'email'


# admin.site.register(Doctor, ProjectAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Lection)
admin.site.register(City, CityAdmin)
admin.site.register(Speciallity)
admin.site.register(Knowledge)
admin.site.register(GetCourseExportID, ExportAdmin)

