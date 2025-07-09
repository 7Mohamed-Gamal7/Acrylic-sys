from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Department, JobTitle, Employee

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(JobTitle) 
class JobTitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title', 'description')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'employee_code',
        'full_name',
        'department', 
        'job_title',
        'phone_number',
        'hiring_date',
        'is_active'
    )
    list_filter = (
        'department',
        'job_title',
        'is_active',
        'hiring_date'
    )
    search_fields = (
        'employee_code',
        'full_name',
        'national_id',
        'phone_number'
    )
