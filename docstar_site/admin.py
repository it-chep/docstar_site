from django.contrib import admin, messages
from django.utils.html import format_html
from django.template.response import TemplateResponse

from docstar_site.models import *
from docstar_site.utils import validate_tg_channel_url, validate_inst_url
from django.utils import timezone


def custom_admin_index_wrapper(original_index):
    def wrapper(request, extra_context=None):
        # Получаем стандартный response
        response = original_index(request, extra_context)

        if not isinstance(response, TemplateResponse):
            return response

        # Добавляем статистику только для superusers
        if request.user.is_superuser:
            now = timezone.now()
            periods = {
                'year': now - timezone.timedelta(days=365),
                'month_6': now - timezone.timedelta(days=180),
                'month': now - timezone.timedelta(days=30),
                'week': now - timezone.timedelta(weeks=1),
                'day': now - timezone.timedelta(days=1),
            }

            stats = []
            for type_id, type_name in CooperationType.choices:
                type_stats = {'type_name': type_name}
                for period_name, period_date in periods.items():
                    count = Doctor.objects.filter(
                        cooperation_type=type_id,
                        date_created__gte=period_date
                    ).count()
                    type_stats[period_name] = count
                stats.append(type_stats)

            # Добавляем статистику в контекст
            response.context_data['stats'] = stats

        return response

    return wrapper


# Применяем декоратор к стандартному index
admin.site.index = custom_admin_index_wrapper(admin.site.index)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("id", 'name', 'cooperation_type', 'display_cities', 'display_specialties', 'is_active')
    search_fields = ("email", "name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("id",)

    list_filter = ('additional_cities', 'additional_specialties', 'is_active', 'cooperation_type')
    filter_horizontal = ('additional_cities', 'additional_specialties')
    raw_id_fields = ('city', 'speciallity')
    readonly_fields = ('s3_image', 'date_created')

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
        if change and ('tg_channel_url' in form.changed_data or 'instagram_url' in form.changed_data):
            success = self._handle_subscribers_url_change(request, obj.id, obj.tg_channel_url, obj.inst_url)
            if not success:
                return

        if change and ('is_active' in form.changed_data):
            success = self._handle_change_is_active(request, obj, obj.is_active)
            if not success:
                return

        super().save_model(request, obj, form, change)

    @staticmethod
    def _handle_change_is_active(request, obj, is_active) -> bool:
        """Обработка изменения IS_ACTIVE"""

        client = settings.SUBSCRIBERS_CLIENT

        doctor_admin_url = reverse('admin:docstar_site_doctor_change', args=[obj.id])

        try:
            status = client.update_doctor_is_active(obj.id, is_active)
            if status > 400:
                messages.error(request,
                               format_html(
                                   'Не удалось обновить данные в сервисе подписчиков.'
                                   '<a href="{}">Перейти к редактированию доктора</a>',
                                   doctor_admin_url)
                               )
                return False
            return True
        except Exception as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, f"Ошибка при обновлении признака АКТИВНОСТИ: {str(e)}")
            return False

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
    def _handle_subscribers_url_change(request, doctor_id, tg_channel_url, instagram_url):
        """Обработка изменения ссылки на канал телеграм"""
        client = settings.SUBSCRIBERS_CLIENT
        username = validate_tg_channel_url(tg_channel_url)
        inst_username = validate_inst_url(instagram_url)

        doctor_admin_url = reverse('admin:docstar_site_doctor_change', args=[doctor_id])

        try:
            # todo сделать валидацию и отправку инстаграмма
            status = client.update_doctor(doctor_id, username, inst_username)
            if status > 400:
                messages.error(request,
                               format_html(
                                   'Не удалось обновить данные в сервисе подписчиков.'
                                   '<a href="{}">Перейти к редактированию доктора</a>',
                                   doctor_admin_url)
                               )
                return False
            if status == 200:
                messages.success(request, "Данные телеграм-канала успешно обновлены в сервисе подписчиков")
            if status == 201:
                messages.success(request, "Успешно создал новую запись в сервисе подписчиков")
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


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", 'name', 'code')
    search_fields = ("name",)


@admin.register(Speciallity)
class SpeciallityAdmin(admin.ModelAdmin):
    list_display = ("id", 'name',)
    search_fields = ("name",)


class ExportAdmin(admin.ModelAdmin):
    list_display = ('export_id', 'export_time')


from django.contrib.auth.models import Group

admin.site.unregister(Group)
