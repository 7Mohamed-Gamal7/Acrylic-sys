# Generated by Django 5.0.14 on 2025-07-09 12:23

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='اسم القسم')),
                ('description', models.TextField(blank=True, verbose_name='الوصف')),
            ],
            options={
                'verbose_name': 'قسم',
                'verbose_name_plural': 'الأقسام',
            },
        ),
        migrations.CreateModel(
            name='JobTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='المسمى الوظيفي')),
                ('description', models.TextField(blank=True, verbose_name='الوصف')),
            ],
            options={
                'verbose_name': 'مسمى وظيفي',
                'verbose_name_plural': 'المسميات الوظيفية',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_code', models.CharField(max_length=20, unique=True, verbose_name='كود الموظف')),
                ('full_name', models.CharField(max_length=200, verbose_name='الاسم بالكامل')),
                ('gender', models.CharField(choices=[('M', 'ذكر'), ('F', 'أنثى')], max_length=1, verbose_name='النوع')),
                ('date_of_birth', models.DateField(verbose_name='تاريخ الميلاد')),
                ('phone_number', models.CharField(max_length=20, verbose_name='رقم الهاتف')),
                ('address', models.TextField(verbose_name='العنوان')),
                ('hiring_date', models.DateField(verbose_name='تاريخ التعيين')),
                ('standard_working_hours', models.PositiveIntegerField(default=8, verbose_name='ساعات العمل المعتادة')),
                ('is_active', models.BooleanField(default=True, verbose_name='نشط')),
                ('basic_salary', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='الراتب الأساسي')),
                ('transportation_allowance', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='بدل مواصلات')),
                ('phone_package', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='بدل هاتف')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='employees.department', verbose_name='القسم')),
                ('job_title', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='employees.jobtitle', verbose_name='المسمى الوظيفي')),
            ],
            options={
                'verbose_name': 'موظف',
                'verbose_name_plural': 'الموظفون',
            },
        ),
    ]
