from django.db import models

# Create your models here.
import datetime

from django.db import models
from django.utils import timezone

class Employees(models.Model):
    emp_no = models.IntegerField(primary_key=True)
    birth_date = models.DateField()
    first_name = models.CharField(max_length=14)
    last_name = models.CharField(max_length=16)
    gender = models.CharField(max_length=1)
    hire_date = models.DateField()
    email = models.CharField(max_length=50, blank=True)
    number = models.CharField(max_length=20, blank=True)
    img = models.ImageField(upload_to='images/', default="images/3.jpg")

    class Meta:
        managed = False
        db_table = 'employees'

    def __str__(self):
        return self.first_name



class Salaries(models.Model):
    emp_no = models.OneToOneField(Employees, models.DO_NOTHING, db_column='emp_no', primary_key=True)
    salary = models.IntegerField()
    from_date = models.DateField()
    to_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'salaries'
        unique_together = (('emp_no', 'from_date'),)


class TitlesName(models.Model):
    title_no = models.IntegerField(primary_key=True)
    title_name = models.CharField(unique=True, max_length=40)

    class Meta:
        managed = True
        db_table = 'titles_name'

    def __str__(self):
        return self.title_name


class Titles(models.Model):
    emp_no = models.OneToOneField(Employees, models.DO_NOTHING, db_column='emp_no', primary_key=True, unique=False)
    title_no = models.ForeignKey(TitlesName, models.DO_NOTHING, db_column='title_no', unique=False)
    from_date = models.DateField(unique=False)
    to_date = models.DateField(default='9999-01-01')

    class Meta:
        managed = True
        db_table = 'titles'
        unique_together = (('emp_no', 'title_no', 'from_date'),)


class Departments(models.Model):
    dept_no = models.CharField(primary_key=True, max_length=4)
    dept_name = models.CharField(unique=True, max_length=40)

    class Meta:
        managed = True
        db_table = 'departments'

    def __str__(self):
        return self.dept_name


class DeptEmp(models.Model):
    emp_no = models.OneToOneField('Employees', models.DO_NOTHING, db_column='emp_no', primary_key=True, unique=False)
    dept_no = models.ForeignKey(Departments, models.DO_NOTHING, db_column='dept_no')
    from_date = models.DateField()
    to_date = models.DateField(default='9999-01-01')

    class Meta:
        managed = False
        db_table = 'dept_emp'
        unique_together = (('emp_no', 'dept_no'),)


class DeptManager(models.Model):
    emp_no = models.OneToOneField('Employees', models.DO_NOTHING, db_column='emp_no', primary_key=True, unique=False)
    dept_no = models.ForeignKey(Departments, models.DO_NOTHING, db_column='dept_no')
    from_date = models.DateField()
    to_date = models.DateField(blank=True, default='9999-01-01')

    class Meta:
        managed = False
        db_table = 'dept_manager'
        unique_together = (('emp_no', 'dept_no'),)


class Functions(models.Model):
    func_no = models.IntegerField(primary_key=True)
    func_name = models.CharField(unique=True, max_length=200)

    class Meta:
        managed = True
        db_table = 'functions'

    def __str__(self):
        return self.func_name

class EmployeeFunctions(models.Model):
    emp_no = models.OneToOneField('Employees', models.DO_NOTHING, db_column='emp_no', primary_key=True, unique=False)
    func_no = models.ForeignKey(Functions, models.DO_NOTHING, db_column='func_no')
    func_assessment = models.FloatField()

    class Meta:
        managed = True
        db_table = 'emp_functions'
        unique_together = (('emp_no', 'func_no'),)


class PresenceLog(models.Model):
    emp_no = models.OneToOneField('Employees', models.DO_NOTHING, db_column='emp_no', primary_key=True, unique=False)
    from_date = models.DateField()
    to_date = models.DateField(default='9999-01-01')
    replaced = models.IntegerField(default=1)
    class Meta:
        managed = True
        db_table = 'presence_log'
        unique_together = (('emp_no', 'from_date'),)


class EmpTaskList(models.Model):
    emp_no = models.OneToOneField('Employees', models.DO_NOTHING, db_column='emp_no', primary_key=True, unique=False)
    func_no = models.ForeignKey(Functions, models.DO_NOTHING, db_column='func_no')
    new_func_assessment = models.FloatField()
    date = models.DateField()
    to_date = models.DateField()
    add_func = models.IntegerField(default=0)
    class Meta:
        managed = True
        db_table = 'emp_task_list'
        unique_together = (('emp_no', 'func_no', 'new_func_assessment', 'date', 'to_date', 'add_func'),)

class AddTasks(models.Model):
    emp_no = models.OneToOneField('Employees', models.DO_NOTHING, db_column='emp_no', primary_key=True,
                                  unique=False)
    func_no = models.ForeignKey(Functions, models.DO_NOTHING, db_column='func_no')
    new_func_assessment = models.FloatField()
    date = models.DateField()
    to_date = models.DateField()

    class Meta:
        managed = True
        db_table = 'add_tasks'
        unique_together = (('emp_no', 'func_no', 'date', 'to_date'),)


class FuncAssessment(models.Model):
    emp_no = models.OneToOneField('Employees', models.DO_NOTHING, db_column='emp_no', primary_key=True, unique=False)
    func_no = models.ForeignKey(Functions, models.DO_NOTHING, db_column='func_no')
    assessment = models.FloatField()
    class Meta:
        managed = True
        db_table = 'func_assessment'
        unique_together = (('emp_no', 'func_no', 'assessment'),)


class ManAcc(models.Model):
    emp_no = models.OneToOneField('Employees', models.DO_NOTHING, db_column='emp_no', primary_key=True)
    password = models.CharField(max_length=45)
    class Meta:
        managed = True
        db_table = 'manager_account'

class help(models.Model):
    emp_no = models.OneToOneField('Employees', models.DO_NOTHING, db_column='emp_no', primary_key=True,
                                  unique=False)
    func_no = models.ForeignKey(Functions, models.DO_NOTHING, db_column='func_no')
    assessment = models.FloatField()
    date = models.DateField()
    to_date = models.DateField()
    add = models.IntegerField()
    class Meta:
        managed = True
        db_table = 'help'
        unique_together = (('emp_no', 'func_no', 'assessment', 'date', 'to_date', 'add'),)
