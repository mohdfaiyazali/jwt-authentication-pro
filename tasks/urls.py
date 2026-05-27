from django.urls import path
from .views import (
    TaskListCreateView,
    AdminTaskListView,
    TaskDetailView
)

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='tasks'),
    path('admin/tasks/', AdminTaskListView.as_view(), name='admin-tasks'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
]