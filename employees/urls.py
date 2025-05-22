# المسار: Acrylic_sys/apps/employees/urls.py

from django.urls import path
from . import views # استيراد الـ views من نفس المجلد

# تحديد اسم للـ url pattern لتسهيل الرجوع إليه من القوالب
# هذا الاسم يجب أن يكون فريدًا على مستوى التطبيق
app_name = 'employees' # اختياري لكن موصى به بشدة

urlpatterns = [
    # المسار: /employees/ (عندما يتم تضمينه من المشروع الرئيسي)
    # الـ View: الدالة employee_list_view من views.py
    # الاسم: 'employee_list' (هذا الاسم هو الذي استخدمناه في القوالب {% url 'employee_list' %})
    path('', views.employee_list_view, name='employee_list'),
    path('<int:pk>/', views.employee_detail_view, name='employee_detail'),
    path('add/', views.EmployeeCreateView.as_view(), name='employee_add'),
    path('<int:pk>/edit/', views.EmployeeUpdateView.as_view(), name='employee_edit'),
  
]