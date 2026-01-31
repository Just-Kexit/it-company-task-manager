from django.urls import path

from .views import (
    index,
    WorkerListView,
    TaskListView,
)

urlpatterns = [
    path("", index, name="index"),
    path("worker/", WorkerListView.as_view(), name="worker-list"),
    path("task/", TaskListView.as_view(), name="task-list")
]

app_name = "task_manager"