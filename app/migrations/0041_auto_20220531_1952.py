# Generated by Django 3.0.5 on 2022-05-31 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0040_auto_20220530_0051'),
    ]

    operations = [
        migrations.CreateModel(
            name='Functions',
            fields=[
                ('func_no', models.IntegerField(primary_key=True, serialize=False)),
                ('func_name', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'db_table': 'functions',
                'managed': True,
            },
        ),
        migrations.AlterField(
            model_name='titles',
            name='emp_no',
            field=models.OneToOneField(db_column='emp_no', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='app.Employees'),
        ),
        migrations.CreateModel(
            name='PresenceLog',
            fields=[
                ('emp_no', models.OneToOneField(db_column='emp_no', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='app.Employees')),
                ('func_assessment', models.FloatField()),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('func_no', models.ForeignKey(db_column='func_no', on_delete=django.db.models.deletion.DO_NOTHING, to='app.Functions')),
            ],
            options={
                'db_table': 'presence_log',
                'managed': True,
                'unique_together': {('emp_no', 'func_no', 'from_date')},
            },
        ),
        migrations.CreateModel(
            name='EmployeeFunctions',
            fields=[
                ('emp_no', models.OneToOneField(db_column='emp_no', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='app.Employees')),
                ('func_assessment', models.FloatField()),
                ('func_no', models.ForeignKey(db_column='func_no', on_delete=django.db.models.deletion.DO_NOTHING, to='app.Functions')),
            ],
            options={
                'db_table': 'emp_functions',
                'managed': True,
                'unique_together': {('emp_no', 'func_no')},
            },
        ),
    ]
