from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.core.validators import MinValueValidator

class Department(models.Model):
    name = models.CharField(_("اسم القسم"), max_length=100, unique=True)
    description = models.TextField(_("الوصف"), blank=True)
    created_at = models.DateTimeField(_("تاريخ الإنشاء"), auto_now_add=True)
    updated_at = models.DateTimeField(_("تاريخ التحديث"), auto_now=True)

    class Meta:
        verbose_name = _("قسم")
        verbose_name_plural = _("الأقسام")
        ordering = ["name"]

    def __str__(self):
        return self.name

class JobTitle(models.Model):
    title = models.CharField(_("المسمى الوظيفي"), max_length=100, unique=True)
    description = models.TextField(_("الوصف"), blank=True)
    created_at = models.DateTimeField(_("تاريخ الإنشاء"), auto_now_add=True)
    updated_at = models.DateTimeField(_("تاريخ التحديث"), auto_now=True)

    class Meta:
        verbose_name = _("مسمى وظيفي")
        verbose_name_plural = _("المسميات الوظيفية")
        ordering = ["title"]

    def __str__(self):
        return self.title

class Employee(models.Model):
    GENDER_CHOICES = [
        ('M', _('ذكر')),
        ('F', _('أنثى')),
    ]

    MARITAL_STATUS_CHOICES = [
        ('S', _('أعزب')),
        ('M', _('متزوج')),
        ('D', _('مطلق')),
        ('W', _('أرمل')),
    ]

    INSURANCE_STATUS_CHOICES = [
        ('active', _('نشط')),
        ('inactive', _('غير نشط')),
        ('suspended', _('معلق')),
    ]

    employee_code = models.CharField(_("كود الموظف"), max_length=20, unique=True)
    full_name = models.CharField(_("الاسم بالكامل"), max_length=200)
    national_id = models.CharField(_("الرقم القومي"), max_length=14, unique=True)
    date_of_birth = models.DateField(_("تاريخ الميلاد"))
    gender = models.CharField(_("النوع"), max_length=1, choices=GENDER_CHOICES)
    marital_status = models.CharField(_("الحالة الاجتماعية"), max_length=1, choices=MARITAL_STATUS_CHOICES)
    phone_number = models.CharField(_("رقم الهاتف"), max_length=20)
    address = models.TextField(_("العنوان"))
    
    department = models.ForeignKey(Department, on_delete=models.PROTECT, verbose_name=_("القسم"))
    job_title = models.ForeignKey(JobTitle, on_delete=models.PROTECT, verbose_name=_("المسمى الوظيفي"))
    hiring_date = models.DateField(_("تاريخ التعيين"))
    standard_working_hours = models.PositiveIntegerField(_("ساعات العمل المعتادة"), default=8)
    is_active = models.BooleanField(_("نشط"), default=True)
    
    basic_salary = models.DecimalField(_("الراتب الأساسي"), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    transportation_allowance = models.DecimalField(_("بدل مواصلات"), max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    phone_package = models.DecimalField(_("بدل هاتف"), max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    social_insurance_number = models.CharField(_("رقم التأمين الاجتماعي"), max_length=20, blank=True)
    insurance_status = models.CharField(_("حالة التأمين"), max_length=10, choices=INSURANCE_STATUS_CHOICES, blank=True)
    insured_salary = models.DecimalField(_("الراتب المؤمن عليه"), max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    insurance_subscription_start_date = models.DateField(_("تاريخ بداية الاشتراك"), null=True, blank=True)
    
    annual_leave_entitlement = models.PositiveIntegerField(_("رصيد الإجازة السنوية"), default=21)
    casual_leave_entitlement = models.PositiveIntegerField(_("رصيد الإجازة العرضية"), default=7)
    sick_leave_entitlement = models.PositiveIntegerField(_("رصيد الإجازة المرضية"), default=14)
    performance_evaluation = models.CharField(_("تقييم الأداء"), max_length=2, blank=True)
    salary_increase_rate = models.DecimalField(_("نسبة زيادة الراتب"), max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    created_at = models.DateTimeField(_("تاريخ الإنشاء"), auto_now_add=True)
    updated_at = models.DateTimeField(_("تاريخ التحديث"), auto_now=True)

    class Meta:
        verbose_name = _("موظف")
        verbose_name_plural = _("الموظفون")
        ordering = ["full_name"]

    def __str__(self):
        return f"{self.full_name} - {self.job_title}"

    def get_absolute_url(self):
        return reverse('employees:employee_detail', kwargs={'pk': self.pk})

    def get_age(self):
        import datetime
        return datetime.date.today().year - self.date_of_birth.year - ((datetime.date.today().month, datetime.date.today().day) < (self.date_of_birth.month, self.date_of_birth.day))

    @property
    def total_salary(self):
        return self.basic_salary + self.transportation_allowance + self.phone_package

class ZKDevice(models.Model):
    STATUS_CHOICES = [
        ('active', _('نشط')),
        ('inactive', _('غير نشط')),
        ('maintenance', _('صيانة')),
    ]

    device_name = models.CharField(_("اسم الجهاز"), max_length=100)
    ip_address = models.CharField(_("عنوان IP"), max_length=15)
    port = models.PositiveIntegerField(_("المنفذ"), default=4370)
    serial_number = models.CharField(_("الرقم التسلسلي"), max_length=50, unique=True)
    model = models.CharField(_("الموديل"), max_length=50)
    status = models.CharField(_("الحالة"), max_length=11, choices=STATUS_CHOICES, default='active')
    last_sync = models.DateTimeField(_("آخر مزامنة"), null=True, blank=True)
    sync_interval = models.PositiveIntegerField(_("فترة المزامنة (دقائق)"), default=15)
    location = models.CharField(_("الموقع"), max_length=100)
    notes = models.TextField(_("ملاحظات"), blank=True)

    class Meta:
        verbose_name = _("جهاز ZK")
        verbose_name_plural = _("أجهزة ZK")

    def __str__(self):
        return f"{self.device_name} ({self.ip_address})"

class ZKAttendanceRecord(models.Model):
    STATUS_CHOICES = [
        ('check_in', _('حضور')),
        ('check_out', _('انصراف')),
    ]

    device = models.ForeignKey(ZKDevice, on_delete=models.CASCADE, verbose_name=_("الجهاز"))
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name=_("الموظف"))
    record_time = models.DateTimeField(_("وقت التسجيل"))
    status = models.CharField(_("الحالة"), max_length=10, choices=STATUS_CHOICES)
    device_user_id = models.CharField(_("معرف المستخدم بالجهاز"), max_length=20)
    is_processed = models.BooleanField(_("تمت معالجته"), default=False)
    raw_data = models.TextField(_("البيانات الخام"), blank=True)

    class Meta:
        verbose_name = _("سجل حضور ZK")
        verbose_name_plural = _("سجلات حضور ZK")
        indexes = [
            models.Index(fields=['employee', 'record_time']),
        ]

    def __str__(self):
        return f"{self.employee} - {self.get_status_display()} @ {self.record_time}"

class ZKSyncLog(models.Model):
    device = models.ForeignKey(ZKDevice, on_delete=models.CASCADE, verbose_name=_("الجهاز"))
    sync_time = models.DateTimeField(_("وقت المزامنة"), auto_now_add=True)
    records_fetched = models.PositiveIntegerField(_("عدد السجلات المستلمة"))
    status = models.CharField(_("حالة المزامنة"), max_length=20)
    error_message = models.TextField(_("رسالة الخطأ"), blank=True)
    duration = models.DurationField(_("مدة المزامنة"), null=True, blank=True)

    class Meta:
        verbose_name = _("سجل مزامنة ZK")
        verbose_name_plural = _("سجلات مزامنة ZK")
        ordering = ['-sync_time']

    def __str__(self):
        return f"{self.device} @ {self.sync_time}"

class EmployeeDeviceMapping(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, verbose_name=_("الموظف"))
    device = models.ForeignKey(ZKDevice, on_delete=models.CASCADE, verbose_name=_("الجهاز"))
    device_user_id = models.CharField(_("معرف المستخدم بالجهاز"), max_length=20, unique=True)
    last_updated = models.DateTimeField(_("آخر تحديث"), auto_now=True)

    class Meta:
        verbose_name = _("تعيين موظف لجهاز")
        verbose_name_plural = _("تعيينات الموظفين للأجهزة")
        unique_together = ('employee', 'device')

    def __str__(self):
        return f"{self.employee} → {self.device}"
