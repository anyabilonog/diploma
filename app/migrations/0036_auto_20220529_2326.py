# Generated by Django 3.0.5 on 2022-05-29 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0035_auto_20220529_2301'),
    ]

    operations = [
        migrations.RenameField(
            model_name='titles',
            old_name='title',
            new_name='title_no',
        ),
        migrations.AlterField(
            model_name='titles',
            name='emp_no',
            field=models.OneToOneField(db_column='emp_no', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='app.Employees'),
        ),
        migrations.AlterUniqueTogether(
            name='titles',
            unique_together={('emp_no', 'title_no', 'from_date')},
        ),
    ]