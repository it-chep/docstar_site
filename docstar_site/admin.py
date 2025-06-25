from django.contrib import admin, messages

from docstar_site.models import *
from docstar_site.utils import validate_url


class CityAdmin(admin.ModelAdmin):
    list_display = ("id", 'name', 'code')
    search_fields = ("name",)


class DoctorAdmin(admin.ModelAdmin):
    list_display = ("id", 'name', 'email', 'city', 'speciallity', 'is_active')
    search_fields = ("email", "name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("id",)

    list_filter = ('city', 'speciallity', 'is_active')
    raw_id_fields = ('city', 'speciallity')

    readonly_fields = ('s3_image',)

    def save_model(self, request, obj, form, change):
        if change and ('tg_channel_url' in form.changed_data or 'instagram_url' in form.changed_data):
            success = self._handle_tg_channel_url_change(request, obj.id, obj.tg_channel_url)
            if not success:
                return

        super().save_model(request, obj, form, change)

    def _handle_tg_channel_url_change(self, request, doctor_id, tg_channel_url):
        """Обработка изменения ссылки на канал телеграм"""
        client = settings.SUBSCRIBERS_CLIENT
        username = validate_url(tg_channel_url)
        try:
            # todo сделать валидацию и отправку инстаграмма
            status = client.update_doctor(doctor_id, username, "")
            if status > 400:
                messages.error(request,
                               "Не удалось обновить данные в сервисе подписчиков.")
                return False
            if status == 200:
                messages.success(request, "Данные телеграм-канала успешно обновлены в сервисе подписчиков")
            if status == 201:
                messages.success(request, "Успешно создал новую запись в сервисе подписчиков")
            return True
        except Exception as e:
            messages.error(request, f"Ошибка при обновлении телеграм-канала: {str(e)}")
            return False


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
