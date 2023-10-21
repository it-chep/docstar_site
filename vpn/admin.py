from django.contrib import admin
from vpn.models import Blogger, UTM, Client


class BloggerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'username', 'tg_id', 'sb_id', 'utm')
    list_filter = ('utm',)
    search_fields = ('name', 'username')
    list_display_links = ('id', 'name')
    change_form_template = 'admin/change_blogger_form.html'


class UTMAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'tg_id', 'sb_id', 'gk_id', 'registration_date_time', 'utm', 'blogger')
    list_filter = ('utm', 'blogger')
    search_fields = ('name', 'tg_id', 'sb_id', 'gk_id')
    list_display_links = ('id', 'name')


admin.site.register(Blogger, BloggerAdmin)
admin.site.register(UTM, UTMAdmin)
admin.site.register(Client, ClientAdmin)