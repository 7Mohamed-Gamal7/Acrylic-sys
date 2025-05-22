# المسار: Acrylic_sys/apps/employees/admin.py

from django.contrib import admin
from django.utils.translation import gettext_lazy as _ # Import translation function
from .models import Department, JobTitle, Employee # استيراد النماذج من نفس المجلد
from django.utils.translation import gettext_lazy as _

# تخصيص واجهة عرض الأقسام
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at') # الحقول التي تظهر في قائمة الأقسام
    search_fields = ('name', 'description') # الحقول التي يمكن البحث فيها

# تخصيص واجهة عرض المسميات الوظيفية
@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at')
    search_fields = ('title', 'description')

# تخصيص واجهة عرض الموظفين (أكثر تفصيلاً)
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    # الحقول التي تظهر في قائمة الموظفين
    list_display = (
        'employee_code',
        'full_name',
        'department',
        'job_title',
        'phone_number',
        'hiring_date',
        'is_active',
        'get_age', # عرض الدالة المحسوبة (العمر)
    )
    # فلاتر تظهر في الشريط الجانبي
    list_filter = (
        'department',
        'job_title',
        'gender',
        'marital_status',
        'is_active',
        'hiring_date', # يمكنك الفلترة حسب تاريخ التعيين (مثل هذا الشهر، هذا العام)
    )
    # الحقول التي يمكن البحث فيها
    search_fields = (
        'employee_code',
        'full_name',
        'national_id',
        'phone_number',
        'department__name', # البحث في اسم القسم المرتبط
        'job_title__title', # البحث في اسم المسمى الوظيفي المرتبط
    )
    # ترتيب الحقول في صفحة إضافة/تعديل الموظف باستخدام fieldsets
    fieldsets = (
        (_('المعلومات الأساسية والشخصية'), { # اسم القسم الأول
            'fields': (
                'employee_code',
                'full_name',
                ('national_id', 'date_of_birth'), # وضع حقلين في نفس السطر
                ('gender', 'marital_status'),
                'phone_number',
                'address',
            )
        }),
        (_('المعلومات الوظيفية'), { # اسم القسم الثاني
            'fields': (
                'department',
                'job_title',
                'hiring_date',
                'standard_working_hours',
                'is_active',
            )
        }),
        (_('المعلومات المالية'), { # اسم القسم الثالث
            'fields': (
                'basic_salary',
                'transportation_allowance',
                'phone_package',
            )
        }),
        (_('معلومات التأمينات'), { # اسم القسم الرابع
            'classes': ('collapse',), # جعل القسم قابلاً للطي (collapsible)
            'fields': (
                'social_insurance_number',
                'insurance_status',
                'insured_salary',
                'insurance_subscription_start_date',
            )
        }),
        (_('معلومات الإجازات والتقييم'), { # اسم القسم الخامس
            'classes': ('collapse',),
            'fields': (
                'annual_leave_entitlement',
                'casual_leave_entitlement',
                'sick_leave_entitlement',
                'performance_evaluation',
                'salary_increase_rate',
            )
        }),
    )
    # جعل حقول التاريخ للقراءة فقط لمنع التعديل التلقائي (اختياري)
    # readonly_fields = ('created_at', 'updated_at')

# طريقة التسجيل الأساسية (بدون تخصيص):
# admin.site.register(Department)
# admin.site.register(JobTitle)
# admin.site.register(Employee)