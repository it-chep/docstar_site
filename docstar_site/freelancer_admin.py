from django.contrib import admin
from django.utils.html import format_html
from django.contrib.admin import AdminSite
from docstar_site.models import (
    FreelancersSpeciality,
    FreelancersCity,
    SocialNetworks,
    Freelancer,
    FreelancerSpecialityM2M,
    FreelancerCityM2M,
    FreelancerSocialNetworksM2M,
    FreelancersPriceList,
    FreelancerCooperationType
)


@admin.register(FreelancersSpeciality)
class FreelancersSpecialityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(FreelancersCity)
class FreelancersCityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(SocialNetworks)
class SocialNetworksAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


class FreelancerSpecialityM2MInline(admin.TabularInline):
    model = FreelancerSpecialityM2M
    extra = 1
    verbose_name = "Дополнительная специальность"
    verbose_name_plural = "Дополнительные специальности"


class FreelancerCityM2MInline(admin.TabularInline):
    model = FreelancerCityM2M
    extra = 1
    verbose_name = "Дополнительный город"
    verbose_name_plural = "Дополнительные города"


class FreelancerSocialNetworksM2MInline(admin.TabularInline):
    model = FreelancerSocialNetworksM2M
    extra = 1
    verbose_name = "Социальная сеть"
    verbose_name_plural = "Социальные сети"


class FreelancersPriceListInline(admin.TabularInline):
    model = FreelancersPriceList
    extra = 1
    verbose_name = "Услуга в прайс-листе"
    verbose_name_plural = "Прайс-лист"


@admin.register(Freelancer)
class FreelancerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'email', 'slug', 'is_active',
        'is_worked_with_doctors', 'price_category',
        'speciality', 'city', 'display_avatar', 'cooperation_type'
    )
    list_display_links = ('id', 'name')
    list_filter = (
        'is_active', 'is_worked_with_doctors', 'price_category',
        'speciality', 'city'
    )
    search_fields = ('name', 'email', 'slug', 'tg_username')
    readonly_fields = ('display_avatar',)
    raw_id_fields = ('city', 'speciality', 'cooperation_type')
    fieldsets = (
        ('Основная информация', {
            'fields': (
                'name', 'email', 'slug', 'is_active',
                'is_worked_with_doctors', 'price_category',
                'cooperation_type'
            )
        }),
        ('Контакты', {
            'fields': ('tg_username', 'portfolio_link')
        }),
        ('Локация и специализация', {
            'fields': ('speciality', 'city')
        }),
        ('Фотографии', {
            'fields': ('avatar', 's3_image')
        }),
    )
    inlines = [
        FreelancerSpecialityM2MInline,
        FreelancerCityM2MInline,
        FreelancerSocialNetworksM2MInline,
        FreelancersPriceListInline,
    ]

    def display_avatar(self, obj):
        if obj.get_s3_file:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: cover;" />',
                obj.get_s3_file
            )
        return "Нет фото"

    display_avatar.short_description = 'Текущее фото'

    def save_model(self, request, obj, form, change):
        # Сохраняем модель, чтобы сработал кастомный save
        super().save_model(request, obj, form, change)


@admin.register(FreelancerSpecialityM2M)
class FreelancerSpecialityM2MAdmin(admin.ModelAdmin):
    list_display = ('id', 'freelancer', 'speciality')
    list_display_links = ('id', 'freelancer')
    raw_id_fields = ('speciality', 'freelancer')
    list_filter = ('speciality',)
    search_fields = ('freelancer__name', 'speciality__name')


@admin.register(FreelancerCityM2M)
class FreelancerCityM2MAdmin(admin.ModelAdmin):
    list_display = ('id', 'freelancer', 'city')
    list_display_links = ('id', 'freelancer')
    list_filter = ('city',)
    search_fields = ('freelancer__name', 'city__name')
    raw_id_fields = ('freelancer', 'city')


@admin.register(FreelancerSocialNetworksM2M)
class FreelancerSocialNetworksM2MAdmin(admin.ModelAdmin):
    list_display = ('id', 'freelancer', 'social_network')
    list_display_links = ('id', 'freelancer')
    list_filter = ('social_network',)
    search_fields = ('freelancer__name', 'social_network__name')
    raw_id_fields = ('freelancer', 'social_network')


@admin.register(FreelancersPriceList)
class FreelancersPriceListAdmin(admin.ModelAdmin):
    list_display = ('id', 'freelancer', 'name', 'price')
    list_display_links = ('id', 'name')
    list_filter = ('freelancer',)
    search_fields = ('freelancer__name', 'name')
    raw_id_fields = ('freelancer',)


@admin.register(FreelancerCooperationType)
class FreelancerCooperationTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
