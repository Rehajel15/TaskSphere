from django.urls import path
from home import views

urlpatterns = [
    path('', views.main, name='main'),
    path('employees', views.employees_page, name='employees_page')
]