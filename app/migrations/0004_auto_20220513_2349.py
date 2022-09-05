# Generated by Django 3.2.11 on 2022-05-13 20:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_titles'),
    ]

    operations = [
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('dept_no', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('dept_name', models.CharField(max_length=40, unique=True)),
            ],
            options={
                'db_table': 'departments',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DeptEmp',
            fields=[
                ('emp_no', models.OneToOneField(db_column='emp_no', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='app.employees')),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
            ],
            options={
                'db_table': 'dept_emp',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DeptManager',
            fields=[
                ('emp_no', models.OneToOneField(db_column='emp_no', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='app.employees')),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
            ],
            options={
                'db_table': 'dept_manager',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EmployyesDatabase',
            fields=[
                ('emp_no', models.OneToOneField(db_column='emp_no', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='app.employees')),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
            ],
            options={
                'db_table': 'dept_manager',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Salaries',
            fields=[
                ('emp_no', models.OneToOneField(db_column='emp_no', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='app.employees')),
                ('salary', models.IntegerField()),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
            ],
            options={
                'db_table': 'salaries',
                'managed': False,
            },
        ),
        migrations.AlterModelOptions(
            name='employees',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='titles',
            options={'managed': False},
        ),
    ]
