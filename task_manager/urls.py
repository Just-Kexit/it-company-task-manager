from django.urls import path

from .views import (
    index,
    WorkerListView,
    TaskListView,
    TaskTypeListView,
    PositionListView,
    WorkerDetailView,
    TaskDetailView,
    WorkerCreateView,
    TaskCreateView,
    TaskTypeCreateView,
    PositionCreateView,
)

urlpatterns = [
    path("", index, name="index"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("workers/<int:pk>", WorkerDetailView.as_view(), name="worker-detail"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create", TaskCreateView.as_view(), name="task-create"),
    path("task-types/", TaskTypeListView.as_view(), name="task-type-list"),
    path("task-types/create", TaskTypeCreateView.as_view(), name="task-type-create"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("positions/create", PositionCreateView.as_view(), name="position-create"),
]

app_name = "task_manager"
