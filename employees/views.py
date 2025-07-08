from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Employee, Department, JobTitle, ZKDevice, ZKAttendanceRecord, ZKSyncLog, EmployeeDeviceMapping
from .forms import EmployeeForm
from .serializers import (
    DepartmentSerializer,
    JobTitleSerializer,
    EmployeeSerializer,
    ZKDeviceSerializer,
    ZKAttendanceRecordSerializer,
    ZKSyncLogSerializer,
    EmployeeDeviceMappingSerializer
)


# Standard Django Views
class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.GET.get('department'):
            queryset = queryset.filter(department__id=self.request.GET['department'])
        if self.request.GET.get('is_active') == 'true':
            queryset = queryset.filter(is_active=True)
        return queryset.select_related('department', 'job_title')


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = 'employees/employee_detail.html'
    context_object_name = 'employee'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("تفاصيل الموظف")
        return context


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_add.html'

    def form_valid(self, form):
        messages.success(self.request, _("تم إضافة الموظف بنجاح"))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('employees:employee_detail', kwargs={'pk': self.object.pk})


class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_edit.html'

    def form_valid(self, form):
        messages.success(self.request, _("تم تحديث بيانات الموظف بنجاح"))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("تعديل بيانات الموظف")
        return context

    def get_success_url(self):
        return reverse_lazy('employees:employee_detail', kwargs={'pk': self.object.pk})


class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    model = Employee
    template_name = 'employees/employee_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _("تم حذف الموظف بنجاح"))
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('employees:employee_list')


def employee_search(request):
    query = request.GET.get('q')
    departments = request.GET.getlist('department')
    status = request.GET.get('status')

    employees = Employee.objects.all().select_related('department', 'job_title')

    if query:
        employees = employees.filter(full_name__icontains=query)

    if departments:
        employees = employees.filter(department__id__in=departments)

    if status == 'active':
        employees = employees.filter(is_active=True)
    elif status == 'inactive':
        employees = employees.filter(is_active=False)

    context = {
        'employees': employees,
        'departments': Department.objects.all(),
        'query': query,
        'selected_departments': departments,
        'status': status
    }
    return render(request, 'employees/employee_search.html', context)


# DRF API Views
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class JobTitleViewSet(viewsets.ModelViewSet):
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer
    permission_classes = [permissions.IsAuthenticated]


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def active(self, request):
        active_employees = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(active_employees, many=True)
        return Response(serializer.data)


class ZKDeviceViewSet(viewsets.ModelViewSet):
    queryset = ZKDevice.objects.all()
    serializer_class = ZKDeviceSerializer
    permission_classes = [permissions.IsAuthenticated]


class ZKAttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = ZKAttendanceRecord.objects.all()
    serializer_class = ZKAttendanceRecordSerializer
    permission_classes = [permissions.IsAuthenticated]


class ZKSyncLogViewSet(viewsets.ModelViewSet):
    queryset = ZKSyncLog.objects.all()
    serializer_class = ZKSyncLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def sync_now(self, request):
        # Implement sync logic here
        return Response({'status': 'sync initiated'}, status=status.HTTP_202_ACCEPTED)


class EmployeeDeviceMappingViewSet(viewsets.ModelViewSet):
    queryset = EmployeeDeviceMapping.objects.all()
    serializer_class = EmployeeDeviceMappingSerializer
    permission_classes = [permissions.IsAuthenticated]
