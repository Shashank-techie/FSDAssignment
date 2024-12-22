from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("create/", views.create_employee, name="create_employee"),
    path("show/", views.show_employees, name="show_employee"),
    path("edit/Employee - <int:f_no>/", views.edit_employees, name="edit_employee"),
     path('delete/Employee - <int:f_no>/', views.delete_employee, name='delete_employee'), 
]