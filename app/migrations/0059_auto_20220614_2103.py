# Generated by Django 3.0.5 on 2022-06-14 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0058_auto_20220614_1806'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManagerAccount',
            fields=[
                ('emp_no', models.OneToOneField(db_column='emp_no', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='app.Employees')),
                ('password', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'manager_account',
                'managed': True,
            },
        ),
        migrations.AlterField(
            model_name='addtasks',
            name='emp_no',
            field=models.OneToOneField(db_column='emp_no', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='app.Employees'),
        ),
        migrations.AlterField(
            model_name='employeefunctions',
            name='emp_no',
            field=models.OneToOneField(db_column='emp_no', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='app.Employees'),
        ),
        migrations.AlterField(
            model_name='emptasklist',
            name='emp_no',
            field=models.OneToOneField(db_column='emp_no', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='app.Employees'),
        ),
        migrations.AlterField(
            model_name='funcassessment',
            name='emp_no',
            field=models.OneToOneField(db_column='emp_no', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='app.Employees'),
        ),
        migrations.AlterField(
            model_name='help',
            name='emp_no',
            field=models.OneToOneField(db_column='emp_no', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='app.Employees'),
        ),
        migrations.AlterField(
            model_name='presencelog',
            name='emp_no',
            field=models.OneToOneField(db_column='emp_no', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='app.Employees'),
        ),
        migrations.AlterField(
            model_name='titles',
            name='emp_no',
            field=models.OneToOneField(db_column='emp_no', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='app.Employees'),
        ),
    ]
