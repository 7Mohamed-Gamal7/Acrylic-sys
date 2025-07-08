from rest_framework import serializers
from .models import (
    Department,
    JobTitle, 
    Employee,
    ZKDevice,
    ZKAttendanceRecord,
    ZKSyncLog,
    EmployeeDeviceMapping
)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class JobTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTitle
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    job_title = JobTitleSerializer(read_only=True)
    
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        source='department',
        write_only=True
    )
    job_title_id = serializers.PrimaryKeyRelatedField(
        queryset=JobTitle.objects.all(),
        source='job_title',
        write_only=True
    )

    class Meta:
        model = Employee
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'social_insurance_number': {'required': True},
            'national_id': {'required': True}
        }


class ZKDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZKDevice
        fields = '__all__'
        extra_kwargs = {
            'ip_address': {'required': True},
            'serial_number': {'required': True}
        }


class ZKAttendanceRecordSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    device = ZKDeviceSerializer(read_only=True)
    
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        source='employee',
        write_only=True
    )
    device_id = serializers.PrimaryKeyRelatedField(
        queryset=ZKDevice.objects.all(),
        source='device',
        write_only=True
    )

    class Meta:
        model = ZKAttendanceRecord
        fields = '__all__'


class ZKSyncLogSerializer(serializers.ModelSerializer):
    device = ZKDeviceSerializer(read_only=True)
    
    device_id = serializers.PrimaryKeyRelatedField(
        queryset=ZKDevice.objects.all(),
        source='device',
        write_only=True
    )

    class Meta:
        model = ZKSyncLog
        fields = '__all__'
        extra_kwargs = {
            'sync_time': {'read_only': True},
            'duration': {'read_only': True}
        }


class EmployeeDeviceMappingSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    device = ZKDeviceSerializer(read_only=True)
    
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        source='employee',
        write_only=True
    )
    device_id = serializers.PrimaryKeyRelatedField(
        queryset=ZKDevice.objects.all(),
        source='device',
        write_only=True
    )

    class Meta:
        model = EmployeeDeviceMapping
        fields = '__all__'
        extra_kwargs = {
            'device_user_id': {'required': True}
        }
