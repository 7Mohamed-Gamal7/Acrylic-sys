# المسار: Acrylic_sys/acrylic_sys/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views # <-- استيراد واجهات المصادقة المدمجة

urlpatterns = [
    path('admin/', admin.site.urls),

    # روابط المصادقة المدمجة
    path('',
         auth_views.LoginView.as_view(
             template_name='registration/login.html' # تحديد قالب تسجيل الدخول
         ),
         name='login'), # اسم الرابط لصفحة الدخول

    path('logout/',
         auth_views.LogoutView.as_view(
             # next_page='login' # يمكنك تحديد الصفحة التالية هنا أو الاعتماد على LOGOUT_REDIRECT_URL في settings.py
         ),
         name='logout'), # اسم الرابط لصفحة الخروج

    # يمكنك إضافة روابط استعادة كلمة المرور هنا لاحقًا إذا أردت
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # ... etc ...

    # تضمين روابط تطبيق الموظفين
    path('employees/', include('employees.urls', namespace='employees')),

    # يمكنك إضافة رابط للصفحة الرئيسية هنا لاحقًا
    # path('', include('apps.dashboard.urls', namespace='dashboard')),
]