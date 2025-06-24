from django.contrib import admin, messages
from django.utils.html import format_html

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

    list_filter = ('additional_cities', 'additional_specialties', 'is_active')
    filter_horizontal = ('additional_cities', 'additional_specialties')
    raw_id_fields = ('city', 'speciallity')
    readonly_fields = ('s3_image',)

    def save_related(self, request, form, formsets, change):
        obj = self.model.objects.get(pk=form.instance.pk)

        if change and 'additional_specialties' in form.changed_data:
            success = self._handle_change_additional_specialties(request, obj, form.cleaned_data)
            if not success:
                return
        if change and 'additional_cities' in form.changed_data:
            success = self._handle_change_additional_cities(request, obj, form.cleaned_data)
            if not success:
                return

        super().save_related(request, form, formsets, change)

    def save_model(self, request, obj, form, change):
        if change and 'tg_channel_url' in form.changed_data:
            success = self._handle_tg_channel_url_change(request, obj.id, obj.tg_channel_url)
            if not success:
                return

        super().save_model(request, obj, form, change)

    @staticmethod
    def _handle_change_additional_cities(request, obj, cleaned_data) -> bool:
        """Обработка изменения дополнительных городов"""
        doctor_admin_url = reverse('admin:docstar_site_doctor_change', args=[obj.id])

        if obj.city_id not in cleaned_data['additional_cities'].all().values_list("id", flat=True):
            messages.set_level(request, messages.ERROR)
            messages.error(request,
                           format_html(
                               'Не удалось обновить дополнительные города. Основной город должен присутствовать в дополнительных.'
                               '<a href="{}">Перейти к редактированию доктора</a>',
                               doctor_admin_url
                           ))
            return False
        return True

    @staticmethod
    def _handle_change_additional_specialties(request, obj, cleaned_data) -> bool:
        """Обработка изменения дополнительных специальностей"""
        doctor_admin_url = reverse('admin:docstar_site_doctor_change', args=[obj.id])

        if obj.speciallity_id not in cleaned_data['additional_specialties'].all().values_list("id", flat=True):
            messages.set_level(request, messages.ERROR)
            messages.error(request,
                           format_html(
                               'Не удалось обновить дополнительные специальности. Основная специальность должна присутствовать в дополнительных. '
                               '<a href="{}">Перейти к редактированию доктора</a>',
                               doctor_admin_url
                           ))
            return False
        return True

    @staticmethod
    def _handle_tg_channel_url_change(request, doctor_id, tg_channel_url):
        """Обработка изменения ссылки на канал телеграм"""
        client = settings.SUBSCRIBERS_CLIENT
        username = validate_url(tg_channel_url)
        doctor_admin_url = reverse('admin:docstar_site_doctor_change', args=[obj.id])

        try:
            created = client.create_doctor(doctor_id, username, "")
            if not created:
                messages.set_level(request, messages.ERROR)
                messages.error(request,
                               format_html(
                                   'Не удалось обновить данные в сервисе подписчиков.'
                                   '<a href="{}">Перейти к редактированию доктора</a>',
                                   doctor_admin_url)
                               )
                return False
            messages.success(request, "Данные телеграм-канала успешно обновлены в сервисе подписчиков")
            return True
        except Exception as e:
            messages.set_level(request, messages.ERROR)
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
