from django.conf.urls.static import static
from django.urls import path

from .views import *
from django.conf import settings

urlpatterns = [
    # ex: /polls/
    path('', login, name='login'),
    path('replacement/<employee_id>', replacement, name='replacement'),
    path('manager_page/<employee_id>/edit', edit, name='edit'),
    path('manager_page/<employee_id>', manager_page, name='manager_page'),
    path('manager_page/edit/', edit, name='edit'),
    path('edit/<employee_id>', edit, name='edit'),
    path('edit/', edit, name='edit'),

    path('index', index, name='index')
]