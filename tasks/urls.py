
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.logIn, name='login'),
    path('loggingin', views.loggingin, name='login'),
    path('signup', views.signup, name='signup'),
    path('register', views.register, name='register'),
    path('createForm', views.createForm, name='createForm'),
    path('createTask', views.createTask, name='createTask'),
    path('updateTask', views.updateTask, name='updateTask'),
    path('deleteTask', views.deleteTask, name='deleteTask'),
    path('task/edit/<int:id>/', views.taskEdit, name='task edit'),
    path('taskList', views.task_list, name='taskList'),
    path('userList', views.userList, name='userList'),
    path('viewUserTasks/<int:id>/', views.viewUserTasks, name='viewUserTasks'),
    path('logout', views.logout, name='logout'),
]
