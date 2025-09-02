from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('accounts/', include('accounts.urls')),
    # path('medications/', include('medications.urls')),
    # path('incidents/', include('incidents.urls')),
    # path('contacts/', include('contacts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # For login/logout
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)