from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('dashboard.urls')),
    path('students/', include('students.urls')),
    path('batches/', include('batches.urls')),
    path('attendance/', include('attendance.urls')),
    path('mocktests/', include('mocktests.urls')),
    path('interviews/', include('interviews.urls')),
    path('projects/', include('projects.urls')),
    path('placements/', include('placements.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
