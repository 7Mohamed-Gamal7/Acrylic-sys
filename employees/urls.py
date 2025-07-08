from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'employees'

urlpatterns = [
    # Employee URLs
    path('', login_required(views.EmployeeListView.as_view()), name='employee_list'),
    path('search/', login_required(views.employee_search), name='employee_search'),
    path('add/', login_required(views.EmployeeCreateView.as_view()), name='employee_add'),
    path('<int:pk>/', login_required(views.EmployeeDetailView.as_view()), name='employee_detail'),
    path('<int:pk>/edit/', login_required(views.EmployeeUpdateView.as_view()), name='employee_edit'),
    path('<int:pk>/delete/', login_required(views.EmployeeDeleteView.as_view()), name='employee_delete'),
    
    # Department URLs (يمكن إضافتها لاحقاً)
    # path('departments/', login_required(views.DepartmentListView.as_view()), name='department_list'),
    # path('departments/add/', login_required(views.DepartmentCreateView.as_view()), name='department_add'),
    
    # Job Title URLs  (يمكن إضافتها لاحقاً)
    # path('job-titles/', login_required(views.JobTitleListView.as_view()), name='jobtitle_list'),
    # path('job-titles/add/', login_required(views.JobTitleCreateView.as_view()), name='jobtitle_add'),
]
