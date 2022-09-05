# Generated by Django 3.0.5 on 2022-06-02 00:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0050_auto_20220601_0733'),
    ]

    operations = [
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
            model_name='presencelog',
            name='emp_no',
            field=models.OneToOneField(db_column='emp_no', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='app.Employees'),
        ),
        migrations.AlterField(
            model_name='titles',
            name='emp_no',
            field=models.OneToOneField(db_column='emp_no', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='app.Employees'),
        ),
        migrations.CreateModel(
            name='help',
            fields=[
                ('emp_no', models.OneToOneField(db_column='emp_no', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='app.Employees')),
                ('assessment', models.FloatField()),
                ('date', models.DateField()),
                ('to_date', models.DateField()),
                ('add', models.IntegerField()),
                ('func_no', models.ForeignKey(db_column='func_no', on_delete=django.db.models.deletion.DO_NOTHING, to='app.Functions')),
            ],
            options={
                'db_table': 'help',
                'managed': True,
                'unique_together': {('emp_no', 'func_no', 'assessment', 'date', 'to_date', 'add')},
            },
        ),
    ]
