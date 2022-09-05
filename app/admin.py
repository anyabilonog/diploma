from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import *

class EmployeesAdmin(admin.ModelAdmin):
    list_display = ['birth_date','first_name','last_name','gender']


class SalariesAdmin(admin.ModelAdmin):
    list_display = ['salary','from_date','to_date']


class TitlesAdmin(admin.ModelAdmin):
    list_display = ['emp_no','title_no']


class DepartmentsAdmin(admin.ModelAdmin):
    list_display = ['dept_name']


class DeptManagerAdmin(admin.ModelAdmin):
    list_display = ['emp_no','dept_no']


class DeptEmpAdmin(admin.ModelAdmin):
    list_display = ['emp_no','dept_no']

class TitlesNameAdmin(admin.ModelAdmin):
    list_display = ['title_name']


class FunctionsAdmin(admin.ModelAdmin):
    list_display = ['func_name']


class EmployeeFunctionsAdmin(admin.ModelAdmin):
    list_display = ['emp_no', 'func_no', 'func_assessment']


class PresenceLogAdmin(admin.ModelAdmin):
    list_display = ['emp_no', 'from_date', 'to_date', 'replaced']


class EmpTaskListAdmin(admin.ModelAdmin):
    list_display = ['emp_no', 'func_no', 'new_func_assessment', 'date', 'to_date', 'add_func']


class AddTasksAdmin(admin.ModelAdmin):
    list_display = ['emp_no', 'func_no', 'new_func_assessment', 'date', 'to_date']

class helpAdmin(admin.ModelAdmin):
    list_display = ['emp_no', 'func_no', 'assessment', 'date', 'to_date','add']


class ManAccAdmin(admin.ModelAdmin):
    list_display = ['emp_no', 'password']


admin.site.register(Employees,EmployeesAdmin)
admin.site.register(Salaries,SalariesAdmin)
admin.site.register(Titles,TitlesAdmin)
admin.site.register(Departments,DepartmentsAdmin)
admin.site.register(DeptEmp,DeptEmpAdmin)
admin.site.register(DeptManager,DeptManagerAdmin)
admin.site.register(TitlesName, TitlesNameAdmin)
admin.site.register(Functions, FunctionsAdmin)
admin.site.register(EmployeeFunctions, EmployeeFunctionsAdmin)
admin.site.register(PresenceLog, PresenceLogAdmin)
admin.site.register(EmpTaskList, EmpTaskListAdmin)
admin.site.register(AddTasks, AddTasksAdmin)
admin.site.register(FuncAssessment)
admin.site.register(help,helpAdmin)
admin.site.register(ManAcc,ManAccAdmin)