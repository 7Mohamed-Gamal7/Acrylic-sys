from rest_framework import serializers
from .models import Department, JobTitle, Employee


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
            'social_insurance_number': {'required': True},
            'national_id': {'required': True}  
        }
