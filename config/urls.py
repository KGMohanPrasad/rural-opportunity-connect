"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('jobs/', include('opportunities.urls')),
    path('scholarships/', include('scholarships.urls')),
    path('schemes/', include('government_schemes.urls')),
    path('skills/', include('skills.urls')),
    path('business/', include('business.urls')),
    path('applications/', include('applications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'accounts.views.custom_404'
handler500 = 'accounts.views.custom_500'
