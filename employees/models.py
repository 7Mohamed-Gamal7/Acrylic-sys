from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

class Department(models.Model):
    name = models.CharField(_("اسم القسم"), max_length=100, unique=True)
    description = models.TextField(_("الوصف"), blank=True)
    
    class Meta:
        verbose_name = _("قسم")
        verbose_name_plural = _("الأقسام")
        
    def __str__(self):
        return self.name

class JobTitle(models.Model):
    title = models.CharField(_("المسمى الوظيفي"), max_length=100, unique=True)
    description = models.TextField(_("الوصف"), blank=True)
    
    class Meta:
        verbose_name = _("مسمى وظيفي") 
        verbose_name_plural = _("المسميات الوظيفية")
        
    def __str__(self):
        return self.title

class Employee(models.Model):
    GENDER_CHOICES = [('M', _('ذكر')), ('F', _('أنثى'))]
    
    employee_code = models.CharField(_("كود الموظف"), max_length=20, unique=True)
    full_name = models.CharField(_("الاسم بالكامل"), max_length=200)
    gender = models.CharField(_("النوع"), max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(_("تاريخ الميلاد"))
    phone_number = models.CharField(_("رقم الهاتف"), max_length=20)
    address = models.TextField(_("العنوان"))
    
    hiring_date = models.DateField(_("تاريخ التعيين")) 
    standard_working_hours = models.PositiveIntegerField(_("ساعات العمل المعتادة"), default=8)
    is_active = models.BooleanField(_("نشط"), default=True)
    basic_salary = models.DecimalField(
        _("الراتب الأساسي"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    transportation_allowance = models.DecimalField(
        _("بدل مواصلات"),
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    phone_package = models.DecimalField(
        _("بدل هاتف"),
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    
    created_at = models.DateTimeField(_("تاريخ الإنشاء"), auto_now_add=True)
    updated_at = models.DateTimeField(_("تاريخ التحديث"), auto_now=True)
    
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        verbose_name=_("القسم")
    )
    job_title = models.ForeignKey(
        JobTitle,
        on_delete=models.PROTECT,
        verbose_name=_("المسمى الوظيفي")
    )
    
    class Meta:
        verbose_name = _("موظف")
        verbose_name_plural = _("الموظفون")
        
    def __str__(self):
        return f"{self.full_name} ({self.employee_code})"
    
    @property
    def total_salary(self):
        return self.basic_salary + self.transportation_allowance + self.phone_package
