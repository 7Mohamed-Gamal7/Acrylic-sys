from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Employee, Department, JobTitle

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['created_at', 'updated_at']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hiring_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'insurance_subscription_start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
    )
    insurance_subscription_start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        label="تاريخ بدء الاشتراك في التأمينات"
    )

    # --- إعادة تعريف حقول ForeignKey لاستخدام Select2 أو ما شابه لاحقًا (اختياري) ---
    # حاليًا ستظهر كقائمة منسدلة عادية
    # department = forms.ModelChoiceField(queryset=Department.objects.all(), label="القسم")
    # job_title = forms.ModelChoiceField(queryset=JobTitle.objects.all(), label="المسمى الوظيفي")

    class Meta:
        model = Employee # النموذج الذي يرتبط به هذا الفورم
        # تحديد الحقول التي ستظهر في الفورم وترتيبها
        fields = [
            'employee_code', 'full_name', 'national_id', 'date_of_birth',
            'gender', 'marital_status', 'phone_number', 'address',
            'department', 'job_title', 'hiring_date', 'standard_working_hours',
            'basic_salary', 'transportation_allowance', 'phone_package',
            'social_insurance_number', 'insurance_status', 'insured_salary',
            'insurance_subscription_start_date',
            'annual_leave_entitlement', 'casual_leave_entitlement', 'sick_leave_entitlement',
            'performance_evaluation', 'salary_increase_rate',
            'is_active', # إضافة حقل الحالة للسماح بتعطيل الموظف
        ]
        # يمكنك تخصيص الـ widgets أو الـ labels هنا أيضًا إذا أردت
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}), # جعل حقل العنوان أكبر قليلاً
            'performance_evaluation': forms.Textarea(attrs={'rows': 3}),
            # --- إضافة كلاسات Bootstrap هنا (طريقة أخرى بدلاً من JS) ---
            # لكن استخدام JS في القالب أكثر مرونة لأنه لا يكرر الكلاس لكل حقل
            # 'employee_code': forms.TextInput(attrs={'class': 'form-control'}),
            # 'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            # ... وهكذا لباقي الحقول
        }
        # يمكنك تحديد الـ labels هنا أيضًا إذا لم تكن الأسماء الافتراضية مناسبة
        # labels = {
        #     'employee_code': 'كود الموظف المميز',
        # }
        # يمكنك إضافة help_texts هنا أيضًا
        # help_texts = {
        #     'national_id': 'أدخل الرقم القومي المكون من 14 رقمًا.',
        # }

    # دالة لتنظيف البيانات (مثال: التحقق من أن الكود الوظيفي فريد بشكل حساس لحالة الأحرف إذا أردت)
    # def clean_employee_code(self):
    #     code = self.cleaned_data.get('employee_code')
    #     # استبعاد الحالة الحالية عند التعديل
    #     instance_pk = self.instance.pk if self.instance else None
    #     if Employee.objects.filter(employee_code__iexact=code).exclude(pk=instance_pk).exists():
    #         raise forms.ValidationError("هذا الكود الوظيفي مستخدم بالفعل.")
    #     return code

    # def clean_national_id(self):
    #     nid = self.cleaned_data.get('national_id')
    #     instance_pk = self.instance.pk if self.instance else None
    #     if Employee.objects.filter(national_id=nid).exclude(pk=instance_pk).exists():
    #         raise forms.ValidationError("هذا الرقم القومي مسجل لموظف آخر.")
    #     return nid

    # ملاحظة: التحقق من التفرد (unique=True) في النموذج كافٍ لمعظم الحالات،
    # لكن دوال clean_ تتيح لك إضافة منطق تحقق أكثر تعقيدًا.