from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'grappelli/', include('grappelli.urls')),
    path('users/', include('users.urls')),
    path('vpn/', include('vpn.urls')),
    path('api/v1/', include('docstar_site.api.v1.urls')),
    path('tickets/', include('tickets.urls')),
    path('', include('docstar_site.urls')),
]

if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = TemplateView.as_view(template_name='docstar/404.html')
handler500 = TemplateView.as_view(template_name='docstar/500.html')
