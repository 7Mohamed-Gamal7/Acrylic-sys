# المسار: Acrylic_sys/apps/employees/models.py

from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _ # لاستخدام الترجمة لاحقًا (اختياري لكن جيد)
import datetime
from django.urls import reverse # لاسترجاع الروابط بسهولة في الـ views أو القوالب

# =============================
# نموذج الأقسام Department Model
# =============================
class Department(models.Model):
    name = models.CharField(
        _('اسم القسم'),
        max_length=100,
        unique=True, # يجب أن يكون اسم القسم فريدًا
        help_text=_('أدخل اسم القسم، يجب أن يكون فريدًا.')
    )
    description = models.TextField(
        _('الوصف'),
        blank=True, # يمكن ترك الوصف فارغًا
        null=True,  # يسمح بقيمة NULL في قاعدة البيانات
        help_text=_('أدخل وصفًا اختياريًا للقسم.')
    )
    created_at = models.DateTimeField(_('تاريخ الإنشاء'), auto_now_add=True)
    updated_at = models.DateTimeField(_('تاريخ التحديث'), auto_now=True)

    class Meta:
        verbose_name = _('قسم') # اسم النموذج المفرد في لوحة التحكم
        verbose_name_plural = _('الأقسام') # اسم النموذج الجمع في لوحة التحكم
        ordering = ['name'] # ترتيب الأقسام أبجديًا بالاسم افتراضيًا

    def __str__(self):
        # كيف سيظهر الكائن عند طباعته أو في لوحة التحكم
        return self.name

# =================================
# نموذج المسميات الوظيفية JobTitle Model
# =================================
class JobTitle(models.Model):
    title = models.CharField(
        _('المسمى الوظيفي'),
        max_length=100,
        unique=True, # يجب أن يكون المسمى الوظيفي فريدًا
        help_text=_('أدخل المسمى الوظيفي، يجب أن يكون فريدًا.')
    )
    description = models.TextField(
        _('الوصف'),
        blank=True,
        null=True,
        help_text=_('أدخل وصفًا اختياريًا للمسمى الوظيفي.')
    )
    created_at = models.DateTimeField(_('تاريخ الإنشاء'), auto_now_add=True)
    updated_at = models.DateTimeField(_('تاريخ التحديث'), auto_now=True)

    class Meta:
        verbose_name = _('مسمى وظيفي')
        verbose_name_plural = _('المسميات الوظيفية')
        ordering = ['title']

    def __str__(self):
        return self.title

# =============================
# نموذج الموظف Employee Model
# =============================
class Employee(models.Model):

    # --- تعريف الخيارات Choices ---
    GENDER_CHOICES = [
        ('M', _('ذكر')),
        ('F', _('أنثى')),
    ]
    MARITAL_STATUS_CHOICES = [
        ('S', _('أعزب/عزباء')),
        ('M', 'متزوج/متزوجة'),
        ('D', 'مطلق/مطلقة'),
        ('W', 'أرمل/أرملة'),
    ]
    INSURANCE_STATUS_CHOICES = [
        ('N', _('غير مؤمن عليه')),
        ('A', _('نشط')),
        ('S', _('موقوف')),
    ]

    # --- محددات الصحة Validators ---
    # للتحقق من أن الرقم القومي يتكون من 14 رقمًا (حسب النظام المصري كمثال، يمكن تعديله)
    national_id_validator = RegexValidator(
        regex=r'^\d{14}$',
        message=_("الرقم القومي يجب أن يتكون من 14 رقمًا.")
    )
    # للتحقق من أن رقم الهاتف يبدأ بـ + أو 0 ويتكون من أرقام (مثال عام)
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("رقم الهاتف يجب أن يكون بتنسيق صحيح (مثال: +201xxxxxxxxx أو 01xxxxxxxxx).")
    )
    # للتحقق من أن الرقم التأميني يتكون من أرقام فقط (مثال)
    social_insurance_validator = RegexValidator(
        regex=r'^\d+$',
        message=_("الرقم التأميني يجب أن يحتوي على أرقام فقط.")
    )

    # --- معلومات أساسية Basic Information ---
    employee_code = models.CharField(
        _('الكود الوظيفي'),
        max_length=20,
        unique=True,
        help_text=_('الكود الفريد للموظف داخل الشركة.')
    )
    full_name = models.CharField(
        _('الاسم الكامل'),
        max_length=255,
        help_text=_('اسم الموظف بالكامل.')
    )
    national_id = models.CharField(
        _('الرقم القومي'),
        max_length=14,
        unique=True,
        validators=[national_id_validator],
        help_text=_('الرقم القومي المكون من 14 رقمًا.')
    )
    phone_number = models.CharField(
        _('رقم الهاتف'),
        max_length=20,
        validators=[phone_validator],
        blank=True, # يمكن تركه فارغًا
        null=True,
        help_text=_('رقم الهاتف المحمول أو الأرضي.')
    )
    address = models.TextField(
        _('العنوان'),
        blank=True,
        null=True,
        help_text=_('عنوان سكن الموظف.')
    )
    gender = models.CharField(
        _('النوع'),
        max_length=1,
        choices=GENDER_CHOICES,
        help_text=_('جنس الموظف.')
    )
    marital_status = models.CharField(
        _('الحالة الاجتماعية'),
        max_length=1,
        choices=MARITAL_STATUS_CHOICES,
        blank=True,
        null=True,
        help_text=_('الحالة الاجتماعية للموظف.')
    )
    date_of_birth = models.DateField(
        _('تاريخ الميلاد'),
        blank=True,
        null=True,
        help_text=_('تاريخ ميلاد الموظف.')
    )

    # --- معلومات وظيفية Job Information ---
    department = models.ForeignKey(
        Department,
        verbose_name=_('القسم'),
        on_delete=models.PROTECT, # منع حذف القسم إذا كان به موظفين
        related_name='employees', # اسم للوصول للموظفين من كائن القسم
        help_text=_('القسم الذي ينتمي إليه الموظف.')
    )
    job_title = models.ForeignKey(
        JobTitle,
        verbose_name=_('المسمى الوظيفي'),
        on_delete=models.PROTECT, # منع حذف المسمى الوظيفي إذا كان مستخدمًا
        related_name='employees',
        help_text=_('المسمى الوظيفي للموظف.')
    )
    hiring_date = models.DateField(
        _('تاريخ التعيين'),
        default=datetime.date.today, # القيمة الافتراضية هي تاريخ اليوم
        help_text=_('تاريخ بدء العمل الرسمي للموظف.')
    )
    standard_working_hours = models.DecimalField(
        _('عدد ساعات العمل القياسية'),
        max_digits=4, # مثل 99.99
        decimal_places=2,
        default=8.00, # قيمة افتراضية شائعة
        validators=[MinValueValidator(0)],
        help_text=_('عدد ساعات العمل اليومية المطلوبة من الموظف.')
    )

    # --- معلومات مالية Financial Information ---
    basic_salary = models.DecimalField(
        _('المرتب الأساسي'),
        max_digits=10, # مثال: 99999999.99
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text=_('المرتب الشهري الأساسي قبل أي إضافات أو خصومات.')
    )
    # يمكن إضافة حقول أخرى هنا للحوافز والبدلات الثابتة إذا أردت، أو إدارتها في نظام الرواتب
    # variable_salary = models.DecimalField(...)
    # total_basic_incentives = models.DecimalField(...)
    # allowances = models.DecimalField(...)
    transportation_allowance = models.DecimalField(
        _('بدل المواصلات'),
        max_digits=8,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
        help_text=_('بدل المواصلات الشهري إن وجد.')
    )
    phone_package = models.DecimalField(
        _('باقة الهاتف'),
        max_digits=8,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
        help_text=_('قيمة باقة الهاتف الشهرية المخصصة للموظف إن وجدت.')
    )

    # --- معلومات التأمينات Social Insurance Information ---
    social_insurance_number = models.CharField(
        _('الرقم التأميني'),
        max_length=50, # قد يختلف الطول
        validators=[social_insurance_validator],
        blank=True,
        null=True,
        unique=True, # يفترض أن يكون فريدًا لكل موظف
        help_text=_('الرقم التأميني الخاص بالموظف.')
    )
    insurance_status = models.CharField(
        _('الحالة التأمينية'),
        max_length=1,
        choices=INSURANCE_STATUS_CHOICES,
        default='N', # القيمة الافتراضية: غير مؤمن عليه
        help_text=_('حالة اشتراك الموظف في التأمينات الاجتماعية.')
    )
    insured_salary = models.DecimalField(
        _('الأجر التأميني'),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text=_('الأجر الذي يتم حساب التأمينات على أساسه.')
    )
    # الأجر المتغير يمكن حسابه أو إضافته كحقل منفصل إذا لزم الأمر
    # variable_insured_salary = models.DecimalField(...)
    insurance_subscription_start_date = models.DateField(
        _('تاريخ بدء الاشتراك في التأمينات'),
        blank=True,
        null=True,
        help_text=_('تاريخ بدء سريان التأمين على الموظف.')
    )

    # --- معلومات الإجازات Leave Information ---
    annual_leave_entitlement = models.PositiveIntegerField(
        _('رصيد الإجازة الاعتيادية السنوي'),
        default=21, # قيمة افتراضية شائعة
        help_text=_('عدد أيام الإجازة الاعتيادية المستحقة للموظف سنويًا.')
    )
    casual_leave_entitlement = models.PositiveIntegerField(
        _('رصيد الإجازة العارضة السنوي'),
        default=7, # قيمة افتراضية شائعة
        help_text=_('عدد أيام الإجازة العارضة المستحقة للموظف سنويًا.')
    )
    sick_leave_entitlement = models.PositiveIntegerField(
        _('رصيد الإجازة المرضية السنوي'),
        default=14, # قيمة افتراضية شائعة (تعتمد على القانون)
        help_text=_('عدد أيام الإجازة المرضية المستحقة للموظف سنويًا (قد يكون غير محدود أو حسب القانون).')
    )
    # ملاحظة: سيتم إدارة الرصيد الفعلي واستخدامه في تطبيق الحضور والإجازات

    # --- معلومات أخرى Other Information ---
    performance_evaluation = models.TextField(
        _('التقييم السنوي/الدوري للأداء'),
        blank=True,
        null=True,
        help_text=_('آخر تقييم لأداء الموظف وملاحظاته.')
    )
    salary_increase_rate = models.DecimalField(
        _('معدل الزيادة السنوية/الدورية المتوقعة (%)'),
        max_digits=5, # مثل 99.99%
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text=_('نسبة الزيادة المتوقعة في الراتب بناءً على التقييم أو السياسات.')
    )
    is_active = models.BooleanField(
        _('نشط'),
        default=True, # الموظف نشط افتراضيًا عند إضافته
        help_text=_('هل الموظف يعمل حاليًا في الشركة؟ (لأغراض الأرشفة)')
    )
    created_at = models.DateTimeField(_('تاريخ الإنشاء'), auto_now_add=True)
    updated_at = models.DateTimeField(_('تاريخ التحديث'), auto_now=True)

    class Meta:
        verbose_name = _('موظف')
        verbose_name_plural = _('الموظفين')
        ordering = ['full_name'] # ترتيب الموظفين أبجديًا بالاسم افتراضيًا

    def __str__(self):
        return f"{self.full_name} ({self.employee_code})"

    def get_age(self):
        # دالة لحساب عمر الموظف (إذا كان تاريخ الميلاد متاحًا)
        if self.date_of_birth:
            today = datetime.date.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None
    get_age.short_description = _('العمر') # اسم العمود في لوحة التحكم

    # يمكنك إضافة دوال أخرى هنا حسب الحاجة (مثل حساب مدة الخدمة)

    def get_absolute_url(self):
        # يرجع الرابط إلى صفحة تفاصيل هذا الموظف
        return reverse('employees:employee_detail', kwargs={'pk': self.pk})
    get_absolute_url.short_description = 'رابط التفاصيل'