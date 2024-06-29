from django.urls import path
from .views import CompletedTaskListView, TaskCreateView, TaskListView, get_task_result, post_task_result, task_form_view, register
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='task_page'),
    path('tasks/completed/', CompletedTaskListView.as_view(), name='task_page'),
    path('task/create/', TaskCreateView.as_view(), name='task-create'),
    path('task/get_result/<int:pk>/', get_task_result, name='task-result'),
    path('task/tag_result/<int:pk>/', post_task_result, name='task-result-post'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('', task_form_view, name='task_form'),
]
