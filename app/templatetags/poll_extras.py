from django import template
from ..views import namedtuplefetchall
import mysql.connector
from ..models import EmployeeFunctions


register = template.Library()
@register.simple_tag
def date(date):
    if type(date) != str:

        if date.month < 10:
            month = '0' + str(date.month)
        else:
            month = str(date.month)
        if date.day < 10:
            day = '0' + str(date.day)
        else:
            day = str(date.day)

        new_date = str(date.year) + '-' + month + '-' + day
    else:
        new_date = date

    return new_date

@register.simple_tag
def print_i(data):
    print(data)


@register.simple_tag
def employee_functions(employee_id):

    emp_func = EmployeeFunctions.objects.filter(pk = employee_id)
    return emp_func