from django.urls import path
from .views import TaskCreateView, TaskListView, get_task_result, post_task_result, task_form_view

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='task_page'),
    path('task/create/', TaskCreateView.as_view(), name='task-create'),
    path('task/get_result/<int:pk>/', get_task_result, name='task-result'),
    path('task/tag_result/<int:pk>/', post_task_result, name='task-result-post'),
    path('', task_form_view, name='task_form'),
]
