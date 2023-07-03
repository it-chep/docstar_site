from django.contrib import admin
from django.http import HttpResponse
from django.template.defaulttags import url
from django.template.response import TemplateResponse
from django.views.generic import ListView, DetailView
from guardian.admin import GuardedModelAdmin

from django.contrib import admin
from django.contrib.admin.models import LogEntry, DELETION
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


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = '<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return mark_safe(link)
    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"

