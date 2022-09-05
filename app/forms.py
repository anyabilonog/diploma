from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from . import models


class DateInput(forms.DateInput):
    input_type = 'date'

    def format_value(self, value):
        return value

class NewDepartmentsForm(forms.ModelForm):
    class Meta:
        model = models.Departments
        fields = ['dept_name']


class NewEmployeeForm(forms.ModelForm):
    CHOICES = (('F', 'F'), ('M', 'M'),)
    gender = forms.ChoiceField(choices=CHOICES)
    hire_date = forms.DateField(widget=DateInput)
    birth_date = forms.DateField(widget=DateInput)
    class Meta:
        model = models.Employees
        fields = ['first_name', 'last_name', 'email', 'number', 'img']


class EmployeeTitleForm(forms.ModelForm):
    class Meta:
        model = models.TitlesName
        fields = ['title_name']


class EmployeeManagerForm(forms.ModelForm):
    from_date = forms.DateField(widget=DateInput)

    class Meta:
        model = models.DeptManager
        fields = ['to_date']


class EmployeeDepartmentForm(forms.ModelForm):
    from_date = forms.DateField(widget=DateInput)
    class Meta:
        model = models.DeptEmp
        fields = ['to_date']

class EditEmployeeForm(forms.ModelForm):
    CHOICES = (('F', 'F'), ('M', 'M'),)
    gender = forms.ChoiceField(choices=CHOICES)
    hire_date = forms.DateField(widget=DateInput)
    birth_date = forms.DateField(widget=DateInput)
    class Meta:
        model = models.Employees
        fields = ['emp_no', 'first_name', 'last_name', 'email', 'number', 'img']