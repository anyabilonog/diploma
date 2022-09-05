# Generated by Django 3.2.11 on 2022-05-13 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_employees'),
    ]

    operations = [
        migrations.CreateModel(
            name='titles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('emp_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.employees')),
            ],
        ),
    ]
