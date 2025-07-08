from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    Department, 
    JobTitle, 
    Employee,
    ZKDevice, 
    ZKAttendanceRecord,
    ZKSyncLog, 
    EmployeeDeviceMapping
)

@admin.register(ZKDevice)
class ZKDeviceAdmin(admin.ModelAdmin):
    list_display = ('device_name', 'ip_address', 'port', 'status', 'location', 'last_sync')
    list_filter = ('status', 'location')
    search_fields = ('device_name', 'ip_address', 'serial_number', 'model')
    ordering = ('device_name',)
    list_editable = ('status',)
    list_per_page = 20

@admin.register(ZKAttendanceRecord)
class ZKAttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('employee', 'device', 'record_time', 'status', 'is_processed')
    list_filter = ('status', 'is_processed', 'device')
    search_fields = ('employee__full_name', 'device__device_name')
    date_hierarchy = 'record_time'
    ordering = ('-record_time',)
    readonly_fields = ('raw_data',)

@admin.register(ZKSyncLog) 
class ZKSyncLogAdmin(admin.ModelAdmin):
    list_display = ('device', 'sync_time', 'records_fetched', 'status')
    list_filter = ('device', 'status')
    search_fields = ('device__device_name', 'status')
    ordering = ('-sync_time',)
    readonly_fields = ('device', 'sync_time', 'records_fetched', 'status', 'error_message', 'duration')

@admin.register(EmployeeDeviceMapping)
class EmployeeDeviceMappingAdmin(admin.ModelAdmin):
    list_display = ('employee', 'device', 'device_user_id', 'last_updated')
    list_filter = ('device',)
    search_fields = ('employee__full_name', 'device__device_name', 'device_user_id')
    raw_id_fields = ('employee', 'device')
    ordering = ('employee',)

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
