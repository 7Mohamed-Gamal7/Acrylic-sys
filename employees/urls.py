from django.urls import path, include
from django.contrib.auth.decorators import login_required
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from . import views

app_name = 'employees'

# API Router Configuration
router = routers.DefaultRouter()
router.register(r'api/departments', views.DepartmentViewSet)
router.register(r'api/job-titles', views.JobTitleViewSet)
router.register(r'api/employees', views.EmployeeViewSet)
router.register(r'api/devices', views.ZKDeviceViewSet)
router.register(r'api/attendance', views.ZKAttendanceRecordViewSet)
router.register(r'api/sync-logs', views.ZKSyncLogViewSet)
router.register(r'api/device-mappings', views.EmployeeDeviceMappingViewSet)

urlpatterns = [
    # Standard Employee URLs
    path('', login_required(views.EmployeeListView.as_view()), name='employee_list'),
    path('search/', login_required(views.employee_search), name='employee_search'),
    path('add/', login_required(views.EmployeeCreateView.as_view()), name='employee_add'),
    path('<int:pk>/', login_required(views.EmployeeDetailView.as_view()), name='employee_detail'),
    path('<int:pk>/edit/', login_required(views.EmployeeUpdateView.as_view()), name='employee_edit'),
    path('<int:pk>/delete/', login_required(views.EmployeeDeleteView.as_view()), name='employee_delete'),

    # API Auth URLs
    path('api/auth/', obtain_auth_token, name='api_token_auth'),
    
    # Include API router URLs
    path('', include(router.urls)),
]
