# المسار: Acrylic_sys/apps/employees/views.py

from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required # لاستلزام تسجيل الدخول للوصول للـ view
from .models import Employee # استيراد نموذج الموظف


# المسار: Acrylic_sys/apps/employees/views.py
from django.views.generic import CreateView, UpdateView # <-- استيراد CBVs
from django.urls import reverse_lazy # <-- لتحديد روابط النجاح للـ CBVs
from django.contrib.messages.views import SuccessMessageMixin # <-- لإظهار رسائل نجاح
from django.contrib.auth.mixins import LoginRequiredMixin # <-- للـ CBVs بدلاً من decorator
from .forms import EmployeeForm # <-- استيراد الفورم الذي أنشأناه




# View لعرض قائمة الموظفين
@login_required # يتطلب أن يكون المستخدم مسجل الدخول للوصول لهذه الصفحة
def employee_list_view(request):
    # جلب جميع الموظفين الذين حالتهم نشطة (is_active=True)
    # وترتيبهم حسب الاسم الكامل
    employees = Employee.objects.filter(is_active=True).order_by('full_name')

    # البيانات التي سيتم تمريرها إلى القالب
    context = {
        'employees': employees,
        'page_title': 'قائمة الموظفين' # يمكن استخدام هذا المتغير في القالب إذا أردت
    }
    # عرض القالب وتمرير البيانات إليه
    return render(request, 'employees/employee_list.html', context)

@login_required
def employee_detail_view(request, pk): # لاحظ استقبال معامل pk من الـ URL
    # جلب الموظف المطلوب باستخدام pk، أو إظهار خطأ 404 إذا لم يكن موجودًا
    employee = get_object_or_404(Employee, pk=pk)

    # البيانات التي سيتم تمريرها للقالب
    context = {
        'employee': employee,
        'page_title': f'تفاصيل الموظف: {employee.full_name}' # عنوان ديناميكي للصفحة
    }
    # عرض قالب التفاصيل وتمرير بيانات الموظف إليه
    return render(request, 'employees/employee_detail.html', context)



# --- أضف الكلاسات التالية ---

# View لإضافة موظف جديد (Class-Based View)
class EmployeeCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Employee                # النموذج الذي نعمل عليه
    form_class = EmployeeForm       # الفورم الذي سيتم استخدامه
    template_name = 'employees/employee_add.html' # القالب الذي سيعرض الفورم
    success_url = reverse_lazy('employees:employee_list') # الرابط الذي يتم التوجيه إليه بعد النجاح
    success_message = "تمت إضافة الموظف %(full_name)s بنجاح!" # رسالة تظهر للمستخدم بعد النجاح

    def get_success_message(self, cleaned_data):
        # تخصيص رسالة النجاح لتشمل اسم الموظف
        return self.success_message % dict(
            cleaned_data,
            full_name=self.object.full_name,
        )
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'إضافة موظف جديد'
        context['cancel_url'] = reverse_lazy('employees:employee_list')  # تأكد من أن هذا هو اسم نمط الـ URL الصحيح
        return context




# View لتعديل بيانات موظف (Class-Based View)
class EmployeeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_edit.html'
    # success_url = reverse_lazy('employees:employee_list') # يمكن التوجيه للقائمة أو للتفاصيل
    success_message = "تم تحديث بيانات الموظف %(full_name)s بنجاح!"

    def get_success_url(self):
        # التوجيه إلى صفحة تفاصيل نفس الموظف بعد التعديل
        return reverse_lazy('employees:employee_detail', kwargs={'pk': self.object.pk})

    def get_success_message(self, cleaned_data):
        # تخصيص رسالة النجاح
        return self.success_message % dict(
            cleaned_data,
            full_name=self.object.full_name,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'تعديل: {self.object.full_name}'
         # تمرير الكائن الحالي للقالب (مفيد للروابط أو العناوين) - UpdateView يمرره تلقائيًا باسم 'object' أو اسم النموذج
        # context['employee'] = self.object
        return context

# ---------------------------