from django.contrib import admin, messages

from docstar_site.models import *
from docstar_site.utils import validate_url


class CityAdmin(admin.ModelAdmin):
    list_display = ("id", 'name', 'code')
    search_fields = ("name",)


class DoctorAdmin(admin.ModelAdmin):
    list_display = ("id", 'name', 'email', 'display_cities', 'display_specialties', 'is_active')
    search_fields = ("email", "name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("id",)

    # todo кастом фильтр на доп и основные города
    list_filter = ('city','speciallity','is_active')
    filter_horizontal = ('additional_cities', 'additional_specialties')
    readonly_fields = ('s3_image', 'city', 'speciallity')

    def save_model(self, request, obj, form, change):
        if change and 'tg_channel_url' in form.changed_data:
            success = self._handle_tg_channel_url_change(request, obj.id, obj.tg_channel_url)
            if not success:
                return

        super().save_model(request, obj, form, change)

    def _handle_tg_channel_url_change(self, request, doctor_id, tg_channel_url):
        """Обработка изменения ссылки на канал телеграм"""
        client = settings.SUBSCRIBERS_CLIENT
        username = validate_url(tg_channel_url)
        try:
            created = client.create_doctor(doctor_id, username, "")
            if not created:
                messages.error(request,
                               "Не удалось обновить данные в сервисе подписчиков.")
                return False
            messages.success(request, "Данные телеграм-канала успешно обновлены в сервисе подписчиков")
            return True
        except Exception as e:
            messages.error(request, f"Ошибка при обновлении телеграм-канала: {str(e)}")
            return False

    def display_cities(self, obj):
        return ", ".join([city.name for city in obj.additional_cities.all()])

    display_cities.short_description = "Города"

    def display_specialties(self, obj):
        return ", ".join([spec.name for spec in obj.additional_specialties.all()])

    display_specialties.short_description = "Специальности"


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
