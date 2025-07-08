from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Employee, Department, JobTitle

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'hiring_date': forms.DateInput(attrs={'type': 'date'}),
            'insurance_subscription_start_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'employee_code': _('كود الموظف'),
            'full_name': _('الاسم بالكامل'),
            'national_id': _('الرقم القومي'),
            'date_of_birth': _('تاريخ الميلاد'),
            'gender': _('النوع'),
            'marital_status': _('الحالة الاجتماعية'),
            'phone_number': _('رقم الهاتف'),
            'address': _('العنوان'),
            'department': _('القسم'),
            'job_title': _('المسمى الوظيفي'),
            'hiring_date': _('تاريخ التعيين'),
            'standard_working_hours': _('ساعات العمل المعتادة'),
            'is_active': _('نشط'),
            'basic_salary': _('الراتب الأساسي'),
            'transportation_allowance': _('بدل مواصلات'),
            'phone_package': _('بدل هاتف'),
            'social_insurance_number': _('رقم التأمين الاجتماعي'),
            'insurance_status': _('حالة التأمين'),
            'insured_salary': _('الراتب المؤمن عليه'),
            'insurance_subscription_start_date': _('تاريخ بداية الاشتراك'),
            'annual_leave_entitlement': _('رصيد الإجازة السنوية'),
            'casual_leave_entitlement': _('رصيد الإجازة العرضية'),
            'sick_leave_entitlement': _('رصيد الإجازة المرضية'),
            'performance_evaluation': _('تقييم الأداء'),
            'salary_increase_rate': _('نسبة زيادة الراتب'),
        }
        help_texts = {
            'employee_code': _('كود فريد لكل موظف'),
            'national_id': _('يجب إدخال الرقم القومي المكون من 14 رقم'),
            'phone_number': _('قم بإدخال رقم الهاتف بالصيغة الدولية إن أمكن'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.all()
        self.fields['job_title'].queryset = JobTitle.objects.all()
        
        # إضافة كلاس Bootstrap لجميع الحقول
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        # تخصيص كلاسات إضافية لحقول محددة
        self.fields['date_of_birth'].widget.attrs.update({'class': 'form-control datepicker'})
        self.fields['hiring_date'].widget.attrs.update({'class': 'form-control datepicker'})
        self.fields['insurance_subscription_start_date'].widget.attrs.update({'class': 'form-control datepicker'})
        
    def clean_national_id(self):
        national_id = self.cleaned_data.get('national_id')
        if len(national_id) != 14:
            raise forms.ValidationError(_("الرقم القومي يجب أن يتكون من 14 رقم"))
        return national_id
        
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit():
            raise forms.ValidationError(_("رقم الهاتف يجب أن يحتوي على أرقام فقط"))
        return phone_number
