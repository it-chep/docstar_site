from django.contrib import admin

from docstar_site.models import *


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'status_club', 'city', 'speciallity')
    search_fields = ("email", "name",)
    prepopulated_fields = {"slug": ("name",)}


class ExportAdmin(admin.ModelAdmin):
    list_display = ('export_id', 'export_time')


admin.site.register(Doctor, DoctorAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Speciallity)

from django.contrib.auth.models import Group
admin.site.unregister(Group)
