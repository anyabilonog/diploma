# Generated by Django 3.0.5 on 2022-05-21 23:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20220522_0107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titles',
            name='emp_no',
            field=models.OneToOneField(db_column='emp_no', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='app.Employees'),
        ),
    ]
