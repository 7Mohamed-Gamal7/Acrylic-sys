from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Dashboard route
    path('', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),

    # Authentication routes
    path('login/',
         auth_views.LoginView.as_view(
             template_name='registration/login.html'
         ),
         name='login'),

    path('logout/',
         auth_views.LogoutView.as_view(),
         name='logout'),

    # Employees app routes
    path('employees/', include('employees.urls', namespace='employees')),
]
