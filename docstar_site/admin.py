from django.contrib import admin

from docstar_site.models import *


class CityAdmin(admin.ModelAdmin):
    list_display = ("id", 'name', 'code')
    search_fields = ("name",)


class DoctorAdmin(admin.ModelAdmin):
    list_display = ("id", 'name', 'email', 'city', 'speciallity', 'is_active')
    search_fields = ("email", "name",)
    prepopulated_fields = {"slug": ("name",)}

    list_filter = ('city', 'speciallity', 'is_active')
    raw_id_fields = ('city', 'speciallity')


class SpeciallityAdmin(admin.ModelAdmin):
    list_display = ("id", 'name',)
    search_fields = ("name",)


class ExportAdmin(admin.ModelAdmin):
    list_display = ('export_id', 'export_time')


admin.site.register(Doctor, DoctorAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Speciallity, SpeciallityAdmin)

from django.contrib.auth.models import Group

admin.site.unregister(Group)
