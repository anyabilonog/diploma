import os
import re
from datetime import date

from MySQLdb.constants.FIELD_TYPE import NULL
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib import messages

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.shortcuts import render, redirect
import time
from collections import Counter

from django.urls import reverse

from .models import *
import mysql.connector
from collections import namedtuple
from .forms import *

conn = mysql.connector.connect(
        user='root', password='qwerty8*', host='localhost', database='employees'
    )
    # Creating a cursor object using the cursor() method
cur = conn.cursor()

'''
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('app/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
'''


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def manager_page(request, employee_id):
    conn = mysql.connector.connect(
        user='root', password='qwerty8*', host='localhost', database='employees'
    )
    # Creating a cursor object using the cursor() method
    cur = conn.cursor()
    print("employee_id - ", employee_id)
    print("employee_id - ", type(employee_id))
    emp_id = Employees.objects.get(emp_no=int(employee_id))
    emp_dept = DeptEmp.objects.filter(to_date='9999-01-01').get(emp_no=emp_id.emp_no)
    # emp_dept = DeptEmp.objects.filter(to_date='9999-01-01').filter(dept_no = emp_dept.dept_no)[:50]

    cur.execute(
        "SELECT employees.gender, employees.emp_no, employees.first_name, employees.last_name, employees.email,"
        "employees.number, employees.img, titles_name.title_name, departments.dept_name "
        "FROM employees "
        "INNER JOIN titles ON employees.emp_no = titles.emp_no "
        "INNER JOIN dept_emp ON employees.emp_no = dept_emp.emp_no "
        "INNER JOIN departments ON dept_emp.dept_no = departments.dept_no "
        "INNER JOIN titles_name ON titles.title_no = titles_name.title_no "
        "WHERE titles.to_date='9999-01-01' and dept_emp.to_date='9999-01-01' and "
        "dept_emp.dept_no = %s "
        "ORDER BY employees.emp_no DESC LIMIT 50", (emp_dept.dept_no_id,))
    # managerseee = [item for item in cur.fetchall()]
    results = namedtuplefetchall(cur)

    employyes_info = Employees.objects.all().values()[:8]
    departments = Departments.objects.all()
    today = date.today()
    today = today.strftime('%Y-%m-%d')
    presencelog = PresenceLog.objects.filter(to_date__gte=today).filter(replaced=0).values()
    presencelog_emp = [emp_no["emp_no_id"] for emp_no in presencelog]
    presencelog_emp_replaced = [emp_no["replaced"] for emp_no in presencelog]
    print(presencelog_emp)
    # results = cur
    cur.execute("SELECT employees.emp_no "
                "FROM employees "
                "INNER JOIN dept_manager ON employees.emp_no = dept_manager.emp_no "
                "INNER JOIN departments ON dept_manager.dept_no = departments.dept_no "
                "WHERE dept_manager.to_date='9999-01-01'")

    # managers = cur.fetchall()
    managers = [item[0] for item in cur.fetchall()]
    # managers = cur)
    titles = TitlesName.objects.all()

    cur.execute("SELECT dept_no FROM departments ORDER BY dept_no DESC LIMIT 1")

    dept_no = namedtuplefetchall(cur)
    cur.execute("SELECT title_no FROM titles_name ORDER BY title_no DESC LIMIT 1")

    title_no = namedtuplefetchall(cur)
    cur.execute("SELECT employees.img "
                "FROM employees "
                "ORDER BY employees.emp_no DESC LIMIT 15")
    img = namedtuplefetchall(cur)

    # Журнал присутності
    """
    cur.execute("SELECT from_date "
                "FROM presence_log "
                "ORDER BY from_date DESC LIMIT 1")
    """
    # from_date = namedtuplefetchall(cur)

    new_department = NewDepartmentsForm()
    new_employee = NewEmployeeForm()
    new_title = EmployeeTitleForm()
    dept_manager = EmployeeManagerForm()

    today = date.today()
    today = today.strftime('%Y-%m-%d')
    cur.execute("SELECT emp_no FROM presence_log WHERE from_date <= %s AND to_date >= %s", (today, today))
    presence_emp = [item[0] for item in cur.fetchall()]
    if EmpTaskList.objects.filter(date=today).exists():
        day_exist = 0
        day_exist = 1
    else:
        day_exist = 1

    if request.method == "POST" and 'empPresences' in request.POST:
        from_date = request.POST.get("presence_from_date")
        to_date = request.POST.get("presence_to_date")
        emp_no = request.POST.get("emp_no")
        emp_no = Employees.objects.get(pk=emp_no)
        PresenceLog.objects.create(emp_no=emp_no,
                                   from_date=from_date,
                                   to_date=to_date,
                                   replaced = 1)
        print(request)

        return HttpResponseRedirect(request.path_info)

    if request.method == "POST" and 'addNewEmployee' in request.POST:
        cur.execute("SELECT emp_no FROM employees ORDER BY emp_no DESC LIMIT 1")

        emp_no = namedtuplefetchall(cur)
        emp_no = int(emp_no[0][0]) + 1
        form = NewEmployeeForm(request.POST, request.FILES)
        # department_name = NewDepartmentsForm(request.POST)
        # department = EmployeeDepartmentForm(request.POST)
        department = request.POST.get("departament_addNewEmployee")
        department = Departments.objects.get(pk=department)
        title = request.POST.get("title")
        title = TitlesName.objects.get(pk=title)
        # dept_manager = EmployeeManagerForm()
        dept_manager = request.POST.get("dept_manager")

        # if form.is_valid() and title.is_valid():
        if form.is_valid():


            employee = Employees.objects.create(birth_date=form.cleaned_data["birth_date"],
                                                first_name=form.cleaned_data["first_name"],
                                                last_name=form.cleaned_data["last_name"],
                                                gender=form.cleaned_data["gender"],
                                                hire_date=form.cleaned_data["hire_date"],
                                                email=form.cleaned_data["email"],
                                                number=form.cleaned_data["number"],
                                                img=form.cleaned_data["img"],
                                                emp_no=emp_no)

            Titles.objects.create(emp_no=employee,
                                  title_no=title,
                                  from_date=form.cleaned_data["hire_date"])
            # department = department_name.cleaned_data["dept_name"]
            # author = Departments.objects.get(dept_name=request.POST["dept_name"])

            DeptEmp.objects.create(emp_no=employee,
                                   dept_no=department,
                                   from_date=form.cleaned_data["hire_date"])
            if request.POST.get("manager_check") == "clicked":
                DeptManager.objects.create(emp_no=employee,
                                           dept_no=department,
                                           from_date=form.cleaned_data["hire_date"])
            # form.save()

            return HttpResponseRedirect(request.path_info)
            # return render(request, 'error.html', department)
        # return render(request, 'index.html')
    else:
        print("presence_emp - ", presence_emp)
        return render(request, 'manager_page.html',
                      {"employee_id": employee_id,
                       'emp': results, 'departments': departments, 'titles': titles,
                       'new_department': new_department, 'new_employee': new_employee,
                       'new_title': new_title,
                       'dept_manager': dept_manager, 'managers': managers,
                       'presence': presence_emp, 'presencelog_emp': presencelog_emp,
                       'presencelog_emp_replaced': presencelog_emp_replaced,
                       'day_exist': day_exist, 'emp_manager': emp_id})

def login(request):
    conn = mysql.connector.connect(
        user='root', password='qwerty8*', host='localhost', database='employees'
    )
    # Creating a cursor object using the cursor() method
    cur = conn.cursor()
    today = date.today()
    today = today.strftime('%Y-%m-%d')
    '''
    account = ManagerAccountForm()
    if request.method == "POST" and 'login' in request.POST:

        form = ManagerAccountForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]


            # form.save()
            return redirect('index')

    return render(request, 'login.html', {'account': account})
    '''

    if request.method == "POST" and 'login_man' in request.POST:
        email = request.POST.get("email")
        password = request.POST.get("password")
        if email == "login" and password == "login":
            return HttpResponseRedirect('index')


        else:

            '''
            cur.execute(
                "SELECT employees.emp_no, manager_account.password "
                "FROM employees "
                "INNER JOIN manager_account ON manager_account.emp_no = employees.emp_no "
                "WHERE employees.emp_no = %s ", (emp.emp_no,))
            # managerseee = [item for item in cur.fetchall()]
            password_check = namedtuplefetchall(cur)[0]
            return HttpResponseRedirect(reverse('manager_page', args=(),
                                                kwargs={'employee_id': emp.emp_no}))
            return HttpResponseRedirect('manager_page/',headers={"employee_id": emp})
            return manager_page(request, emp)
            '''
            #return render(request, 'manager_page.html', {'emp': results, 'emp_manager': emp})

            try:
                emp = Employees.objects.get(email=email)
                emp_dept = DeptEmp.objects.filter(to_date='9999-01-01').get(emp_no=emp.emp_no)
                try:

                    cur.execute(
                        "SELECT employees.emp_no, manager_account.password "
                        "FROM employees "
                        "INNER JOIN manager_account ON manager_account.emp_no = employees.emp_no "
                        "WHERE employees.emp_no = %s ", (emp.emp_no,))
                    # managerseee = [item for item in cur.fetchall()]
                    password_check = namedtuplefetchall(cur)[0]
                    if password_check.password == password:

                        return HttpResponseRedirect(reverse('manager_page',
                                               args=(),
                                               kwargs={'employee_id': emp.emp_no}))
                    else:

                        messages.warning(request,'Невірний пароль!')
                except:
                    messages.warning(request, 'Аккауту не існує!')
                
            except:
                messages.warning(request, 'Невірний логін!')




    return render(request, 'login.html')


def index(request):
    employyes_info = Employees.objects.all().values()[:8]
    departments = Departments.objects.all()

    conn = mysql.connector.connect(
        user='root', password='qwerty8*', host='localhost', database='employees'
    )
    # Creating a cursor object using the cursor() method
    cur = conn.cursor()

    cur.execute("SELECT employees.gender, employees.emp_no, employees.first_name, employees.last_name, employees.email,"
                "employees.number, employees.img, titles_name.title_name, departments.dept_name "
                "FROM employees "
                "INNER JOIN titles ON employees.emp_no = titles.emp_no "
                "INNER JOIN dept_emp ON employees.emp_no = dept_emp.emp_no "
                "INNER JOIN departments ON dept_emp.dept_no = departments.dept_no "
                "INNER JOIN titles_name ON titles.title_no = titles_name.title_no "
                "WHERE titles.to_date='9999-01-01' and dept_emp.to_date='9999-01-01' "
                "ORDER BY employees.emp_no DESC LIMIT 100  ")
    #managerseee = [item for item in cur.fetchall()]
    results = namedtuplefetchall(cur)
    today = date.today()
    today = today.strftime('%Y-%m-%d')
    presencelog = PresenceLog.objects.filter(to_date__gte=today).filter(replaced=0).values()
    presencelog_emp = [ emp_no["emp_no_id"] for emp_no in presencelog]
    presencelog_emp_replaced = [ emp_no["replaced"] for emp_no in presencelog]
    #print(presencelog_emp)
    #results = cur
    cur.execute("SELECT employees.emp_no "
                "FROM employees "
                "INNER JOIN dept_manager ON employees.emp_no = dept_manager.emp_no "
                "INNER JOIN departments ON dept_manager.dept_no = departments.dept_no "
                "WHERE dept_manager.to_date='9999-01-01'")

    #managers = cur.fetchall()
    managers = [item[0] for item in cur.fetchall()]
    #managers = cur)
    titles = TitlesName.objects.all()

    cur.execute("SELECT dept_no FROM departments ORDER BY dept_no DESC LIMIT 1")

    dept_no = namedtuplefetchall(cur)
    cur.execute("SELECT title_no FROM titles_name ORDER BY title_no DESC LIMIT 1")

    title_no = namedtuplefetchall(cur)
    cur.execute("SELECT employees.img "
                "FROM employees "
                "ORDER BY employees.emp_no DESC LIMIT 15")
    img = namedtuplefetchall(cur)

    # Журнал присутності
    """
    cur.execute("SELECT from_date "
                "FROM presence_log "
                "ORDER BY from_date DESC LIMIT 1")
    """
    #from_date = namedtuplefetchall(cur)

    if request.method == "POST" and 'empPresence' in request.POST:
        from_date = request.POST.get("presence_from_date")
        to_date = request.POST.get("presence_to_date")
        emp_no = request.POST.get("emp_no")
        emp_no = Employees.objects.get(pk=emp_no)
        PresenceLog.objects.create(emp_no=emp_no,
                                   from_date=from_date,
                                   to_date=to_date)
        return redirect('index')
    if request.method == "POST" and 'addNewTitle' in request.POST:
        title_no = title_no[0][0]+1
        form = EmployeeTitleForm(request.POST)
        if form.is_valid():
            #department = Departments(dept_name=form.cleaned_data["dept_name"],dept_no=dept_no)

            #department.save()
            TitlesName.objects.create(title_name=form.cleaned_data["title_name"],title_no=title_no)
            #form.save()
            return redirect('index')
    if request.method == "POST" and 'addNewDepartment' in request.POST:
        dept_no = 'd0'+str(int(dept_no[0][0][1:])+1)
        form = NewDepartmentsForm(request.POST)
        if form.is_valid():
            #department = Departments(dept_name=form.cleaned_data["dept_name"],dept_no=dept_no)

            #department.save()
            Departments.objects.create(dept_name=form.cleaned_data["dept_name"],dept_no=dept_no)
            #form.save()
            return redirect('index')
    if request.method == "POST" and 'addNewEmployee' in request.POST:
        cur.execute("SELECT emp_no FROM employees ORDER BY emp_no DESC LIMIT 1")

        emp_no = namedtuplefetchall(cur)
        emp_no = int(emp_no[0][0])+1
        form = NewEmployeeForm(request.POST, request.FILES)
        #department_name = NewDepartmentsForm(request.POST)
        #department = EmployeeDepartmentForm(request.POST)
        department = request.POST.get("departament_addNewEmployee")
        department = Departments.objects.get(pk = department)
        title = request.POST.get("title")
        title = TitlesName.objects.get(pk=title)
        #dept_manager = EmployeeManagerForm()
        dept_manager = request.POST.get("dept_manager")

        #if form.is_valid() and title.is_valid():
        if form.is_valid():
            #department = Departments(dept_name=form.cleaned_data["dept_name"],dept_no=dept_no)

            #department.save()
            '''
            img = form.cleaned_data["img"]
            
            if type(img) is None:
                img = None
            '''

            employee = Employees.objects.create(birth_date=form.cleaned_data["birth_date"],
                                     first_name=form.cleaned_data["first_name"],
                                     last_name=form.cleaned_data["last_name"],
                                     gender=form.cleaned_data["gender"],
                                     hire_date=form.cleaned_data["hire_date"],
                                     email=form.cleaned_data["email"],
                                     number=form.cleaned_data["number"],
                                     img=form.cleaned_data["img"],
                                     emp_no=emp_no)

            Titles.objects.create(emp_no=employee,
                                  title_no=title,
                                  from_date=form.cleaned_data["hire_date"])
            #department = department_name.cleaned_data["dept_name"]
            #author = Departments.objects.get(dept_name=request.POST["dept_name"])

            DeptEmp.objects.create(emp_no = employee,
                                   dept_no = department,
                                   from_date=form.cleaned_data["hire_date"])
            if request.POST.get ("manager_check") == "clicked":
                DeptManager.objects.create(emp_no=employee,
                                       dept_no=department,
                                       from_date=form.cleaned_data["hire_date"])
            #form.save()

            return redirect('index')
            #return render(request, 'error.html', department)
        #return render(request, 'index.html')
    if request.method == "POST" and 'setTasks' in request.POST:
        today = date.today()
        today = today.strftime('%Y-%m-%d')
        if EmpTaskList.objects.filter(date=today).exists():
            pass
            #print("ttttttttt")
            EmpTaskList.objects.filter(date=today).delete()
        #print("YYYYYY")
        cur.execute("SELECT date FROM emp_task_list ORDER BY date DESC LIMIT 1")
        day = namedtuplefetchall(cur)
        #print(day)

        if day != []:
            if day[0].date!= today:
                emp_yesterdays_tasks = {}
                yesterdays_tasks = EmpTaskList.objects.filter(to_date__gte=today)

                for emp in yesterdays_tasks:
                    #if PresenceLog.objects.filter(emp_no = emp.emp_no).get(to_date__gte=today) == 0:
                    print("emp - ", emp.func_no, emp.emp_no)
                    if emp.emp_no in emp_yesterdays_tasks.keys():
                        print("emp.func_no - ", emp.func_no)
                        if emp.func_no in emp_yesterdays_tasks[emp.emp_no].keys():
                            emp_yesterdays_tasks[emp.emp_no][emp.func_no].append(emp.add_func)
                        else:
                            emp_yesterdays_tasks[emp.emp_no][emp.func_no] = [emp.new_func_assessment, emp.to_date, emp.add_func]

                    else:
                        emp_yesterdays_tasks[emp.emp_no] = {}
                        if emp.func_no in emp_yesterdays_tasks[emp.emp_no].keys():
                            emp_yesterdays_tasks[emp.emp_no][emp.func_no].append(emp.add_func)
                        else:
                            emp_yesterdays_tasks[emp.emp_no][emp.func_no] = [emp.new_func_assessment, emp.to_date,
                                                                             emp.add_func]

                    #emp_yesterdays_tasks[emp.emp_no][emp.func_no] = [emp.new_func_assessment, emp.to_date, emp.add_func]
                print("emp_yesterdays_tasks - ", emp_yesterdays_tasks)

                #cur.execute("SELECT DISTINCT emp_no FROM emp_functions")

                cur.execute("SELECT employees.emp_no FROM employees "
                            "INNER JOIN titles ON employees.emp_no = titles.emp_no "
                            "INNER JOIN dept_emp ON employees.emp_no = dept_emp.emp_no "
                            "WHERE titles.to_date='9999-01-01' and dept_emp.to_date='9999-01-01' "
                            "ORDER BY employees.emp_no DESC LIMIT 100  ")
                # які мають завдання
                employee_listt = namedtuplefetchall(cur)
                print("employee_listt", set(employee_listt))
                employee_list = []
                for emp in employee_listt:
                    try:
                        if EmployeeFunctions.objects.filter(emp_no=emp.emp_no) not in employee_list:
                            employee_list.append(EmployeeFunctions.objects.filter(emp_no=emp.emp_no)[0])
                    except:
                        pass
                print("employee_list - ", employee_list)
                employee_list_instance = []
                for i in employee_list:

                    cur.execute("SELECT emp_no, func_no, func_assessment FROM emp_functions "
                                "where emp_no = %s", (i.emp_no_id, ))
                    employee_function_list = namedtuplefetchall(cur)
                    employee = Employees.objects.get(pk=i.emp_no_id)

                    for j in employee_function_list:
                        func = Functions.objects.get(pk=j.func_no)
                        if employee in emp_yesterdays_tasks.keys():
                            if func in emp_yesterdays_tasks[employee].keys():
                                if 0 in emp_yesterdays_tasks[employee][func] and 1 in emp_yesterdays_tasks[employee][func]:
                                    EmpTaskList.objects.create(emp_no=employee,
                                                               func_no=func,
                                                               new_func_assessment=emp_yesterdays_tasks[employee][func][0],
                                                               date=today,
                                                               to_date=emp_yesterdays_tasks[employee][func][1],
                                                               add_func=emp_yesterdays_tasks[employee][func][2])
                                    EmpTaskList.objects.create(emp_no=employee,
                                                               func_no=func,
                                                               new_func_assessment=emp_yesterdays_tasks[employee][func][0],
                                                               date=today,
                                                               to_date=emp_yesterdays_tasks[employee][func][1],
                                                               add_func=emp_yesterdays_tasks[employee][func][3])
                                else:
                                    EmpTaskList.objects.create(emp_no=employee,
                                                               func_no=func,
                                                               new_func_assessment=emp_yesterdays_tasks[employee][func][
                                                                   0],
                                                               date=today,
                                                               to_date=emp_yesterdays_tasks[employee][func][1],
                                                               add_func=emp_yesterdays_tasks[employee][func][2])
                            else:
                                EmpTaskList.objects.create(emp_no=employee,
                                                           func_no=func,
                                                           new_func_assessment=j.func_assessment,
                                                           date=today,
                                                           to_date=today,
                                                           add_func=0)
                        else:
                            EmpTaskList.objects.create(emp_no=employee,
                                                       func_no=func,
                                                       new_func_assessment=j.func_assessment,
                                                       date=today,
                                                       to_date=today,
                                                       add_func=0)


                # managers = cur.fetchall()
                #managers = [item[0] for item in cur.fetchall()]
                #tasks_employees = namedtuplefetchall(cur)
                #print('!!!!', employee_list_instance)
        else:
            today = date.today()
            today = today.strftime('%Y-%m-%d')


            cur.execute("SELECT DISTINCT emp_functions.emp_no FROM emp_functions "
                        "INNER JOIN titles ON emp_functions.emp_no = titles.emp_no "
                        "INNER JOIN dept_emp ON emp_functions.emp_no = dept_emp.emp_no "
                        "WHERE titles.to_date='9999-01-01' and dept_emp.to_date='9999-01-01'")
            # які мають завдання
            employee_list = namedtuplefetchall(cur)
            employee_list_instance = []
            for i in employee_list:

                cur.execute("SELECT emp_no, func_no, func_assessment FROM emp_functions "
                            "where emp_no = %s", i)
                employee_function_list = namedtuplefetchall(cur)

                for j in employee_function_list:
                    EmpTaskList.objects.create(emp_no=Employees.objects.get(pk=i.emp_no),
                                               func_no=Functions.objects.get(pk=j.func_no),
                                               new_func_assessment=j.func_assessment,
                                               date=today,
                                               to_date=today,
                                               add_func = 0)

            # managers = cur.fetchall()
            # managers = [item[0] for item in cur.fetchall()]
            #tasks_employees = namedtuplefetchall(cur)
            #print('!!!!', employee_list_instance)

        return redirect('index')
        #return HttpResponseRedirect(request.path_info)

    else:
        new_department = NewDepartmentsForm()
        new_employee = NewEmployeeForm()
        new_title = EmployeeTitleForm()
        dept_manager = EmployeeManagerForm()

        today = date.today()
        today = today.strftime('%Y-%m-%d')
        cur.execute("SELECT emp_no FROM presence_log WHERE from_date <= %s AND to_date >= %s", (today,today))
        presence_emp = [item[0] for item in cur.fetchall()]
        print("prsencelog - ", presencelog)
        if EmpTaskList.objects.filter(date=today).exists():
            day_exist = 0
            day_exist = 1
        else:
            day_exist = 1

        print(type(day_exist))
        print(day_exist)
        return render(request, 'index.html',
                      {'employyes_info': results, 'departments': departments, 'titles': titles,
                       'new_department': new_department, 'new_employee': new_employee, 'new_title': new_title,
                       'dept_manager': dept_manager, 'managers': managers,
                       'presence': presence_emp, 'presencelog_emp': presencelog_emp,
                       'presencelog_emp_replaced': presencelog_emp_replaced,
                       'day_exist': day_exist})


def edit(request, employee_id):
    conn = mysql.connector.connect(
        user='root', password='qwerty8*', host='localhost', database='employees'
    )
    # Creating a cursor object using the cursor() method
    cur = conn.cursor()

    employee = Employees.objects.get(pk=employee_id)
    employee_title = Titles.objects.filter(pk=employee_id)
    #print(employee_title)
    employee_department = DeptEmp.objects.filter(pk=employee_id)
    employee_manager = DeptManager.objects.filter(pk=employee_id)
    image = employee.img
    department = Departments.objects.all()
    titles_name = TitlesName.objects.all()
    functions = Functions.objects.all()
    cur.execute("SELECT DISTINCT emp_no FROM dept_manager")

    managers = [item[0] for item in cur.fetchall()]
    if int(employee_id) in managers:
        dept_manager = DeptManager.objects.filter(pk=employee_id)
    else:
        dept_manager = None
    emp_function = EmployeeFunctions.objects.filter(pk=employee_id)
    #print('emp_function', emp_function)

    if request.method == "POST" and 'addManager' in request.POST:

        if request.POST.get("to_date_manager"):
            emp_to_date = dept_manager.get(to_date='9999-01-01')
            emp_to_date.to_date=request.POST.get("to_date_manager")
            emp_to_date.save()


        dept_no = request.POST.get("manager_option")
        dept_no = Departments.objects.get(dept_no=dept_no)


        DeptManager.objects.create(emp_no=employee,
                              dept_no=dept_no,
                              from_date=request.POST.get("new_manager-from_date"))

        return HttpResponseRedirect(request.path_info)
    if request.method == "POST" and 'deleteManager' in request.POST:

        dept_name = request.POST.get("delete_manager")
        dept_no = Departments.objects.get(dept_name=dept_name)
        employee_departments = DeptManager.objects.filter(pk=employee_id)
        employee_departments = employee_departments.filter(dept_no=dept_no)
        employee_departments.delete()
        return HttpResponseRedirect(request.path_info)

    if request.method == "POST" and 'deleteTitle' in request.POST:

        title_name = request.POST.get("delete_title")
        title_from_date = request.POST.get("delete_title_from_date")
        title_no = TitlesName.objects.get(title_name=title_name)

        employee_titles = Titles.objects.filter(pk=employee_id)
        employee_titles = employee_titles.filter(title_no=title_no)
        employee_titles = employee_titles.filter(from_date=title_from_date)
        employee_titles.delete()
        return HttpResponseRedirect(request.path_info)

    if request.method == "POST" and 'deleteDepartment' in request.POST:

        dept_name = request.POST.get("delete_departmentname")
        dept_no = Departments.objects.get(dept_name=dept_name)
        employee_departments = DeptEmp.objects.filter(pk=employee_id)
        employee_departments = employee_departments.filter(dept_no=dept_no)
        employee_departments.delete()
        return HttpResponseRedirect(request.path_info)

    if request.method == "POST" and 'addTitle' in request.POST:

        if request.POST.get("title_to_date"):
            title_to_date = employee_title.get(to_date='9999-01-01')
            title_to_date.to_date=request.POST.get("title_to_date")
            title_to_date.save(update_fields=['to_date'])

        if request.POST.get("new_title-to_date"):
            to_date = request.POST.get("new_title-to_date")
        else:
            to_date = '9999-01-01'
        title_name = request.POST.get("new_title")
        title_name = TitlesName.objects.get(pk=title_name)

        Titles.objects.create(emp_no=employee,
                              title_no=title_name,
                              from_date=request.POST.get("new_title-from_date"),
                              to_date=to_date)

        return HttpResponseRedirect(request.path_info)

    if request.method == "POST" and 'addDepartment' in request.POST:

        if request.POST.get("department-to_date"):
            emp_to_date = employee_department.get(to_date='9999-01-01')
            emp_to_date.to_date=request.POST.get("department-to_date")
            emp_to_date.save()

        dept_name = request.POST.get("department_option")
        department_name = Departments.objects.get(pk=dept_name)

        #from_date = date_str(request.POST.get("new_department-from_date"))
        if request.POST.get("new_department-to_date"):
            to_date = request.POST.get("new_department-to_date")
        else:
            to_date = '9999-01-01'

        DeptEmp.objects.create(emp_no=employee,
                              dept_no=department_name,
                              from_date= request.POST.get("new_department-from_date"),
                              to_date = to_date)
        return HttpResponseRedirect(request.path_info)
    if request.method == "POST" and 'addNewFunction' in request.POST:
        cur.execute("SELECT func_no FROM functions ORDER BY func_no DESC LIMIT 1")

        func_no = namedtuplefetchall(cur)

        Functions.objects.create(func_no=func_no[0][0] + 1,
                              func_name=request.POST.get("new_function"))
        return HttpResponseRedirect(request.path_info)
    if request.method == "POST" and 'addNewEmpFunction' in request.POST:
        func_name = request.POST.get("func_option")
        func_no = Functions.objects.get(pk=func_name)

        EmployeeFunctions.objects.create(emp_no=employee,
                              func_no=func_no,
                              func_assessment=request.POST.get("new_function_assessment"))
        return HttpResponseRedirect(request.path_info)
    if request.method == "POST" and 'editEmployee' in request.POST:
       # item = Employees.objects.get(pk=employee_id)
        #form = EditEmployeeForm(request.POST or None, request.FILES or None, instance=item)
        #if form.is_valid():

         #   form.save()
          #  messages.success(request, ('The item has been edited successfully!'))
           # return redirect('index')
        #return render(request, 'index.html')
       employee.emp_no  = request.POST.get("emp_no")
       employee.birth_date = request.POST.get("birth_date")
       employee.first_name = request.POST.get("first_name")
       employee.last_name = request.POST.get("last_name")
       employee.gender = request.POST.get("gender")
       employee.hire_date = request.POST.get("hire_date")
       employee.email = request.POST.get("email")
       employee.number = request.POST.get("number")
       if request.FILES:
           employee.img = request.FILES.get("img")
       else:
           employee.img = image
       employee.save()

       # return render(request, 'index.html', {'employee': employee, 'titles': titles})
       #return redirect('index')
       next = request.POST.get('next', '/')
       print('next - ', next)
       return HttpResponseRedirect(next)

    if request.method == "POST" and 'editPassword' in request.POST:

       password = request.POST.get("password")
       try:
           ManAcc.objects.get(emp_no=employee_id).delete()
           ManAcc.objects.create(emp_no=Employees.objects.get(emp_no=employee_id),
                                         password=password)
       except:
            ManAcc.objects.create(emp_no=Employees.objects.get(emp_no=employee_id),
                                     password=password)


   #return render(request, 'index.html', {'employee': employee, 'titles': titles})
       return HttpResponseRedirect(request.path_info)
    else:
        account = None
        if dept_manager != None:
            print("password - ", account)

            try:
                DeptManager.objects.filter(emp_no=employee_id).get(to_date='9999-01-01')
                print("password - ", account)
                try:
                    ManAcc.objects.get(emp_no=employee_id)
                    print("password - ", account)
                    account = ManAcc.objects.get(emp_no=employee_id)
                except:
                    account = None
            except:
                account = None
        print("password - ", account)
        birth_date = datee(employee.birth_date)
        hire_date = datee(employee.hire_date)
        return render(request, 'edit.html', {'employee': employee, "employee_title": employee_title,
                                             'employee_department': employee_department,
                                             'dept_manager': dept_manager,
                                             'departments': department,
                                             'titles': titles_name,
                                             'birth_date': birth_date,
                                             'hire_date': hire_date,
                                             'date': date,
                                             'functions': emp_function,
                                             'functions_all':functions,
                                             'account': account})

def func_stability(max_one_emp, emp_list, emp_func_stability, to_date, employee_id):
    today = date.today()
    today = today.strftime('%Y-%m-%d')
    v = {}
    func_stab = {}
    # просто індекс
    id = 0
    start = time.time()
    print("emp_list - ", emp_list)
    print("emp_func_stability - ", emp_func_stability)
    for j in emp_func_stability[Employees.objects.get(pk=max_one_emp.emp_no)]:
        for i in range(len(emp_list)):
        # перебираєм перший
        #for j in emp_func_stability[Employees.objects.get(pk=emp_list)]:
            for k in range(len(emp_list)):
                #print(j[0])
                # перебираєм другий
                next_emp_func = emp_func_stability[Employees.objects.get(pk=emp_list[k])]
                for next_emp_func_i in next_emp_func:
                    if type(j)==tuple and len(j) != 1:
                        if len(list(filter(lambda i: i in j, next_emp_func_i)))==0:
                            v[(id, max_one_emp, emp_list[k])] = {}
                            v[(id, max_one_emp,emp_list[k])] = (j, next_emp_func_i)
                            id += 1
                            #print(emp_list[i],emp_list[k], j, next_emp_func_i)

                    else:
                        if j != next_emp_func_i:
                            if j[0] not in next_emp_func_i:
                                v[(id, max_one_emp, emp_list[k])] = {}
                                #print(emp_list[i], emp_list[k], j, next_emp_func_i)
                                v[(id, max_one_emp, emp_list[k])] = (j, next_emp_func_i)
                                id += 1
    end = time.time()
    print("Two employee list time - ", str(end - start))

    start = time.time()
    emp_absent = Employees.objects.get(pk=employee_id)
    end = time.time()
    print("1 - ", str(end - start))
    start = time.time()
    print("vVV - ", v)
    for ind in list(v.keys()):
        help_dict = {}

        emp = ind

        for num_emp_key in range(1,len(emp)):

            for emp_func in v[emp][num_emp_key-1]:
                #print(emp_func)
                #print(emp[num_emp_key])
                u = EmployeeFunctions.objects.filter(emp_no=Employees.objects.get(pk=emp[num_emp_key])).get(func_no=emp_func.func_no)
                add = 0
                assessment = change(u, emp_absent, today)
                help_dict[(Employees.objects.get(pk=emp[num_emp_key]), Functions.objects.get(func_no=emp_func.func_no),
                           today, to_date, add)] = assessment
                add = 1
                help_dict[(Employees.objects.get(pk=emp[num_emp_key]), Functions.objects.get(func_no=emp_func.func_no),
                           today, to_date, add)] = assessment


        allemp = EmpTaskList.objects.filter(date=today)
        tup = ()

        for t in v[emp]:
            tup += t

        for cfunc in allemp:
            assessment = cfunc.new_func_assessment
            if cfunc.emp_no != emp_absent:
                if cfunc.emp_no_id not in emp:
                    add = 0
                    help_dict[
                        (cfunc.emp_no, cfunc.func_no_id,
                         today, cfunc.to_date, add)] = assessment

                else:
                    if cfunc.func_no not in v[emp][emp.index(cfunc.emp_no_id)-1]:
                        add = 0
                        help_dict[
                            (cfunc.emp_no, cfunc.func_no_id,
                             today, cfunc.to_date, add)] = assessment

            else:
                c = Functions.objects.get(func_no=cfunc.func_no_id)
                if c not in tup:
                    add = 0
                    help_dict[
                        (cfunc.emp_no, cfunc.func_no_id,
                         today, cfunc.to_date, add)] = 0


        #distinct_assessments = help.objects.values('assessment').distinct()
        distinct_assessments = list(help_dict.values())
        print("distinct_assessments - ", distinct_assessments)
        count_distinct_assessments = Counter(distinct_assessments)
        distinct_assessments = list(set(distinct_assessments))
        a = {}
        wam = 0
        sum = 0
        for i in distinct_assessments:
            a[i] = count_distinct_assessments[i]
            sum += a[i]
            wam += a[i] * i
        wam /= sum
        # print("WAAM",wam)
        # func_emp = (j.emp_no,(j.func_no, j.emp_no))
        func_emp = tuple(emp)+tuple(v[emp])
        # func_stab[func_emp] = wam

        func_stab[func_emp] = wam
    print('func_stab - ', func_stab)
    end = time.time()
    print("4 - ", str(end-start))

    max_key = max(func_stab, key=func_stab.get)

    max_func_stab = {}
    print("max_key", max_key)
    k = (max_key[0], Employees.objects.get(emp_no=max_key[1]), Employees.objects.get(emp_no=max_key[2]),  max_key[3:])
    print("k - ", k)
    max_func_stab[max_key] = func_stab[max_key]
    print("max_func_stab - ", max_func_stab)
    return max_func_stab

def employee_replacement(employee_id, emp_functions, all_employee_functions):
    func_stab = {}
    func_stab2 = {}
    today = date.today()
    today = today.strftime('%Y-%m-%d')
    # нікому не передавать функції
    task_list = EmpTaskList.objects.filter(emp_no=employee_id).filter(date=today)
    presence = PresenceLog.objects.filter(emp_no=employee_id)
    presence = presence.filter(to_date__gte=today)[0]

    # розділяємо функції

    func_list = Functions.objects.all()
    same_functions = {}

    emp_same_func = []
    for i in task_list:
        same_functions[i.func_no] = []

        emp_same_task = EmpTaskList.objects.filter(func_no=i.func_no).filter(date=today)
        emp_same_task_list = []
        for same_task in list(emp_same_task):
            if list(emp_same_task).count(same_task) < 2:
                emp_same_task_list.append(same_task)
        print("emp_same_task - ", emp_same_task)
        print("emp_same_task_list - ", emp_same_task_list)
        emp_same_task = emp_same_task_list
        for j in emp_same_task:
            #print(Employees.objects.get(emp_no=j.emp_no).value())
            if j.emp_no != i.emp_no:
                if j.new_func_assessment != 0.0 and  len(EmpTaskList.objects.filter(func_no=i.func_no).filter(date=today).filter(emp_no=j.emp_no_id)) < 2:
                    emp_no = Employees.objects.get(emp_no=j.emp_no_id).emp_no
                    #print(str(j.emp_no))
                    #EmpTaskList.objects.filter(emp_no=j.emp_no)
                    #emp = Employees.objects.get(emp_no=j.emp_no)
                    same_functions[i.func_no].append(j)
                    #emp_no = getattr(j,'emp_no')
                    if emp_no not in emp_same_func:
                        emp_same_func.append(emp_no)

    help.objects.all().delete()

    func_stab = {}
    for i in same_functions:
        for j in same_functions[i]:

            func_emp = (j.func_no)
            func_stab2 = {}
            func_stab2[j.func_no] = 0
            try:
                if not func_stab[j.emp_no]:
                    pass
            except:
                func_stab[j.emp_no] = {}
            func_stab[j.emp_no][func_emp] = func_stab2[func_emp]

    v = []
    start = time.time()
    for i in emp_same_func:

        v.append({(Employees.objects.get(pk=i)):subsets(list(func_stab[(Employees.objects.get(pk=i))].keys()))})

    end = time.time()
    print("recursion - ", str(end - start))
    func_stab = {}
    # всі функції 0
    all_emp = EmpTaskList.objects.filter(date=today)
    help_dict = {}
    for emp in all_emp:
        if emp.emp_no != Employees.objects.get(emp_no = employee_id):

            help_dict[(emp.emp_no, emp.func_no, today, presence.to_date, emp.add_func)] = emp.new_func_assessment


        else:

            help_dict[(emp.emp_no, emp.func_no, today, presence.to_date, emp.add_func)] = 0

    distinct_assessments = list(help_dict.values())
    count_distinct_assessments = Counter(distinct_assessments)
    distinct_assessments = list(set(distinct_assessments))
    a = {}
    wam = 0
    sum = 0
    for i in distinct_assessments:
        a[i] = count_distinct_assessments[i]
        sum += a[i]
        wam += a[i] * i
    wam /= sum

    func_zero = {}
    func_zero[employee_id] = wam
    #one_emp_func_stab(v, today, presence, func_stab)
    start = time.time()
    help_dict = {}
    emp_absent = Employees.objects.get(pk=employee_id)
    for i in v:
        #print('i  ', i)
        #print(i[Employees.objects.filter(emp_no=i.emp_no)])
        for j in i:
            #print("j  ", j)
            #for k in i[j]:
            help_dict = {}
            for k in i[j]:
                help_dict = {}
                #print('k  ', k)
                for e in k:
                    #print('e  ', e)
                    u = EmployeeFunctions.objects.filter(emp_no=j.emp_no).get(func_no=e.func_no)
                    add = 0
                    assessment = change(u, emp_absent, today)
                    help_dict[(j,e,today,presence.to_date, add)] = assessment

                    add = 1
                    help_dict[(j, e, today, presence.to_date, add)] = assessment

                allemp = EmpTaskList.objects.filter(date=today)
                if k!=[]:
                    for cfunc in allemp:

                        if cfunc.emp_no != emp_absent:
                            if cfunc.emp_no != j:
                                add = 0
                                help_dict[(cfunc.emp_no, cfunc.func_no, today, cfunc.to_date, add)] = cfunc.new_func_assessment

                            else:
                                if cfunc.func_no not in k:
                                    add = 0
                                    help_dict[(
                                    cfunc.emp_no, cfunc.func_no, today, cfunc.to_date, add)] = cfunc.new_func_assessment

                        else:
                            if cfunc.func_no not in k:
                                add = 0
                                help_dict[(
                                cfunc.emp_no, cfunc.func_no, today, cfunc.to_date, add)] = 0

                    distinct_assessments = list(help_dict.values())
                    count_distinct_assessments = Counter(distinct_assessments)
                    distinct_assessments = list(set(distinct_assessments))
                    a = {}

                    wam = 0
                    sum = 0
                    for i in distinct_assessments:
                        a[i] = count_distinct_assessments[i]
                        sum += a[i]
                        wam += a[i] * i
                    wam /= sum


                    func_emp = tuple(k)
                    # func_stab[func_emp] = wam
                    func_stab2 = {}
                    func_stab2[tuple(k)] = wam
                    try:
                        if not func_stab[j]:
                            pass
                    except:
                        func_stab[j] = {}
                    func_stab[j][func_emp] = func_stab2[func_emp]
    print("func_stab - ", func_stab)

    end = time.time()
    print("one employee time - ", str(end - start))
    max = 0
    max_one_emp = {}
    max_one_emp_f = 0
    for i in list(func_stab.keys()):
        for j in list(func_stab[i].keys()):
            #print(func_stab[i][j])
            if func_stab[i][j] > max:
                max = func_stab[i][j]
                max_one_emp = {}
                max_one_emp[(i, j)] = max
                max_one_emp_f = i

    print("max_one_emp_f - ", max_one_emp)
    start = time.time()
    max_func_stab = func_stability(max_one_emp_f, emp_same_func, func_stab, presence.to_date, employee_id)
    end = time.time()
    print("max_func_stab - ", max_func_stab)
    print("Two employee time - ", str(end - start))

    return task_list, wam, max_func_stab, max_one_emp, func_zero

def replacement(request, employee_id):
    today = date.today()
    today = today.strftime('%Y-%m-%d')
    presence = PresenceLog.objects.filter(emp_no=employee_id)
    presence = presence.filter(to_date__gte=today)[0]
    emp_absent = Employees.objects.get(pk=employee_id)
    if request.method == "POST" and 'zero_replacement' in request.POST:
        presence = PresenceLog.objects.filter(emp_no=employee_id)
        presence = presence.filter(to_date__gte=today)[0]
        EmpTaskList.objects.filter(emp_no=employee_id).filter(date=today).delete()
        for func in EmployeeFunctions.objects.filter(emp_no=Employees.objects.get(emp_no=employee_id)):
            EmpTaskList.objects.create(
                emp_no = Employees.objects.get(emp_no=employee_id),
                func_no = func.func_no,
                new_func_assessment = 0,
                date = today,
                to_date = presence.to_date,
                add_func = 0
            )

    if request.method == "POST" and 'one_replacement' in request.POST:
       one_emp = request.POST.get("one_emp")
       print(one_emp)

       counter = request.POST.get("one_emp_func")
       func_nos = re.findall('[0-9]+', counter)
       func_nos = [int(num) for num in func_nos]
       emp = Employees.objects.get(emp_no=int(one_emp))
       for func in func_nos:
           f = Functions.objects.get(func_no=func)
           EmpTaskList.objects.filter(emp_no=employee_id).filter(date=today).filter(func_no=f).delete()
           one_emp_func = EmpTaskList.objects.filter(emp_no=emp).filter(date=today).get(func_no=f)
           #one_emp_func = one_emp_func.get(add_func=0)
           a = EmployeeFunctions.objects.filter(emp_no=emp).get(func_no=f).func_assessment
           #print(a)
           b = change( EmployeeFunctions.objects.filter(emp_no=emp).get(func_no=f), emp_absent, today)
           print(type(b))


           EmpTaskList.objects.filter(emp_no=emp).filter(date=today).filter(func_no=f).delete()
           EmpTaskList.objects.create(emp_no=emp,
                                      func_no=f,
                                      new_func_assessment=b,
                                      date=today,
                                      to_date=presence.to_date,
                                      add_func=1
                                      )
           EmpTaskList.objects.create(emp_no=emp,
                                      func_no=f,
                                      new_func_assessment=b,
                                      date=today,
                                      to_date=presence.to_date,
                                      add_func=0
                                      )

       print(func_nos)
       zero_func = EmpTaskList.objects.filter(emp_no=employee_id).filter(date=today)
       emp = Employees.objects.get(emp_no=employee_id)
       for func in zero_func:
           EmpTaskList.objects.filter(emp_no=emp).filter(date=today).filter(func_no=func.func_no).delete()
           EmpTaskList.objects.create(emp_no=emp,
                                      func_no=func.func_no,
                                      new_func_assessment=0,
                                      date=today,
                                      to_date=presence.to_date,
                                      add_func=0)


    if request.method == "POST" and 'two_replacement' in request.POST:
       emp1 = request.POST.get("first_emp")
       print("emp1  --- ", emp1)
       print("emp1  --- ", type(emp1))
       emp1 = Employees.objects.get(emp_no=int(emp1))

       counter1 = request.POST.get("first_emp_func")
       func_nos1 = re.findall('[0-9]+', counter1)
       func_nos1 = [int(num) for num in func_nos1]
       emp2 = request.POST.get("second_emp")
       emp2 = Employees.objects.get(emp_no=int(emp2))
       counter2 = request.POST.get("second_emp_func")
       func_nos2 = re.findall('[0-9]+', counter2)
       func_nos2 = [int(num) for num in func_nos2]
       emp_list = [emp1, emp2]
       func_list = [func_nos1, func_nos2]
       for emp in range(len(emp_list)):
           for func in func_list[emp]:
               f = Functions.objects.get(func_no=func)
               EmpTaskList.objects.filter(emp_no=employee_id).filter(date=today).filter(func_no=f).delete()
               one_emp_func = EmpTaskList.objects.filter(emp_no=emp_list[emp]).filter(date=today).get(func_no=f)
               #one_emp_func = one_emp_func.get(add_func=0)
               a = EmployeeFunctions.objects.filter(emp_no=emp_list[emp]).get(func_no=f).func_assessment
               #print(a)
               b = change( EmployeeFunctions.objects.filter(emp_no=emp_list[emp]).get(func_no=f), emp_absent, today)
               print(type(b))


               EmpTaskList.objects.filter(emp_no=emp_list[emp]).filter(date=today).filter(func_no=f).delete()
               EmpTaskList.objects.create(emp_no=emp_list[emp],
                                          func_no=f,
                                          new_func_assessment=b,
                                          date=today,
                                          to_date=presence.to_date,
                                          add_func=1
                                          )
               EmpTaskList.objects.create(emp_no=emp_list[emp],
                                          func_no=f,
                                          new_func_assessment=b,
                                          date=today,
                                          to_date=presence.to_date,
                                          add_func=0
                                          )

           print(func_nos1)
       zero_func = EmpTaskList.objects.filter(emp_no=employee_id).filter(date=today)
       emp = Employees.objects.get(emp_no=employee_id)
       for func in zero_func:
           EmpTaskList.objects.filter(emp_no=emp).filter(date=today).filter(func_no = func.func_no).delete()
           EmpTaskList.objects.create(emp_no=emp,
                                      func_no=func.func_no,
                                      new_func_assessment=0,
                                      date=today,
                                      to_date=presence.to_date,
                                      add_func=0)

    if request.method == "POST" and 'one_replacement' in request.POST or \
            request.method == "POST" and 'two_replacement' in request.POST or \
            request.method == "POST" and 'zero_replacement' in request.POST:
       emp = Employees.objects.get(emp_no=employee_id)
       p = PresenceLog.objects.filter(emp_no=emp).get(to_date__gte=today)
       PresenceLog.objects.filter(emp_no=emp).filter(to_date__gte=today).delete()
       print("p", p)
       PresenceLog.objects.create(emp_no=emp,
                                  from_date = p.from_date,
                                  to_date = p.to_date,
                                  replaced = 0)




       return redirect('index')
    else:
        employee = Employees.objects.get(pk=employee_id)
        emp_function = EmployeeFunctions.objects.filter(pk=employee_id)
        employee_department = DeptEmp.objects.filter(pk=employee_id)
        employee_department = employee_department.get(to_date='9999-01-01')
        employee_title = Titles.objects.filter(pk=employee_id)
        employee_title = employee_title.get(to_date='9999-01-01')
        all_employee_functions = EmployeeFunctions.objects.all()

        result, wam, max_func_stab, max_one_emp, func_zero = employee_replacement(employee_id, emp_function,
                                                                                 all_employee_functions)
        #result, wam, max_one_emp, func_zero = employee_replacement(employee_id, emp_function,all_employee_functions)
        # Записать в журнал присутності
        #print('list(max_func_stab.keys())', list(max_func_stab.keys()))
        # функції не виконуються
        zero_emp = int(list(func_zero.keys())[0])
        zero_func_stab = {'emp': Employees.objects.get(emp_no=zero_emp),
                          'func_stab': func_zero[list(func_zero.keys())[0]]
                          }
        # функції одному працівнику
        one_emp = list(max_one_emp.keys())[0][0]
        print(one_emp)
        print(type(one_emp))
        one_emp_func = list(max_one_emp.keys())[0][1]
        one_employee_func_stab = {
            'emp': one_emp,
            #'funcs': [Functions.objects.get(func_name = one_emp_func[i].func_name).func_no for i in range(len(one_emp_func))],
            'funcs': one_emp_func,
            'func_stab': max_one_emp[ list(max_one_emp.keys())[0] ]
        }

        # функції на двох
        first_emp = list(max_func_stab.keys())[0][1]
        print("first_emp", first_emp)
        first_emp_func = list(max_func_stab.keys())[0][3]
        second_emp = list(max_func_stab.keys())[0][2]
        second_emp_func = list(max_func_stab.keys())[0][4]
        two_employee_func_stab = {'emp1': Employees.objects.get(emp_no=first_emp),
                                  #'emp1_func': [first_emp_func[i].func_name for i in range(len(first_emp_func))],
                                  'emp1_func': first_emp_func,
                                  'emp2': Employees.objects.get(emp_no=second_emp),
                                  'emp2_func': second_emp_func,
                                  'func_stub': max_func_stab[list(max_func_stab.keys())[0]],
                                  }

        return render(request, 'replacement.html',{'employee': employee,
                                               'functions': emp_function,
                                               'employee_department': employee_department,
                                               'employee_title': employee_title,
                                               'result': result,
                                               'max_func_stab': max_func_stab,
                                               'max_one_emp': max_one_emp,
                                               'func_zero': func_zero,
                                               'two_employee_func_stab': two_employee_func_stab,
                                               'zero_func_stab': zero_func_stab,
                                               'one_employee_func_stab': one_employee_func_stab})


def change(emp, emp_absent, day):
    emp_a_dept = DeptEmp.objects.filter(emp_no = emp_absent.emp_no).get(to_date='9999-01-01')
    e_dept = DeptEmp.objects.filter(emp_no = emp.emp_no).get(to_date='9999-01-01')
    emp_a_title = Titles.objects.filter(emp_no = emp_absent.emp_no).get(to_date='9999-01-01')
    e_title = Titles.objects.filter(emp_no = emp.emp_no).get(to_date='9999-01-01')

    new_assesment = emp.func_assessment - emp.func_assessment*0.05
    if  e_dept.dept_no != emp_a_dept.dept_no:
        new_assesment = new_assesment - new_assesment*0.1
    if e_title.title_no != emp_a_title.title_no:
        new_assesment = new_assesment - new_assesment * 0.07




    return new_assesment


def datee(date):
    if date.month < 10:
        month = '0' + str(date.month)
    else:
        month = str(date.month)
    if date.day < 10:
        day = '0' + str(date.day)
    else:
        day = str(date.day)

    new_date = str(date.year) + '-' + month + '-' + day

    return new_date

def date_str(date):
    x = date.split('.')
    return str(x[2])+'-'+str(x[1])+'-'+str(x[0])
def posts_edit(request, id=None):
    instance = get_object_or_404(DeptEmp, id=id)
    context={
        'instance': instance
    }
    return render(request, 'modal.html', context)

def subsets(nums):

    rslt = []

    def dfs(temp, idx):
        rslt.append(temp[:])
        for i in range(idx, len(nums)):
            temp.append(nums[i])
            # backtrack
            dfs(temp, i + 1)
            temp.pop()

    dfs([], 0)
    return rslt

