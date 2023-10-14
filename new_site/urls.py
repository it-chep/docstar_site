import debug_toolbar
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf.urls.static import static
from docstar_site.views import *

from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('grappelli/', include('grappelli.urls')),
    path('users/', include('users.urls')),
    path('vpn/', include('vpn.urls')),
    path('api/v1/doctorlist/', DoctorApiView.as_view(), name='doctor-list'),
    path('', include('docstar_site.urls')),
]

# handler404 = 'docstar_site.views.page_not_found_view'

if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls))
    ] + urlpatterns
    urlpatterns += static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [

    re_path(f'^{settings.STATIC_URL.lstrip("/")}(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

    re_path(f'^{settings.MEDIA_URL.lstrip("/")}(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

]


handler404 = TemplateView.as_view(template_name='docstar/404.html')
handler500 = TemplateView.as_view(template_name='docstar/500.html')
