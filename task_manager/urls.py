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
    WorkerPositionUpdateView,
    WorkerDeleteView,
    TaskUpdateView,
    TaskDeleteView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
    PositionUpdateView,
    PositionDeleteView,
    toggle_assign_to_task
)


urlpatterns = [
    path("", index, name="index"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path(
        "workers/<int:pk>/",
        WorkerDetailView.as_view(),
        name="worker-detail"
    ),
    path(
        "workers/update/<int:pk>/",
        WorkerPositionUpdateView.as_view(),
        name="worker-update"
    ),
    path(
        "workers/delete/<int:pk>/",
        WorkerDeleteView.as_view(),
        name="worker-delete"
    ),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path(
        "tasks/update/<int:pk>/",
        TaskUpdateView.as_view(),
        name="task-update"),
    path(
        "tasks/delete/<int:pk>/",
        TaskDeleteView.as_view(),
        name="task-delete"
    ),
    path(
        "task-types/",
        TaskTypeListView.as_view(),
        name="task-type-list"
    ),
    path(
        "task-types/create/",
        TaskTypeCreateView.as_view(),
        name="task-type-create"
    ),
    path(
        "task-types/update/<int:pk>/",
        TaskTypeUpdateView.as_view(),
        name="task-type-update"
    ),
    path(
        "task-types/delete/<int:pk>/",
        TaskTypeDeleteView.as_view(),
        name="task-type-delete"
    ),
    path(
        "positions/",
        PositionListView.as_view(),
        name="position-list"
    ),
    path(
        "positions/create/",
        PositionCreateView.as_view(),
        name="position-create"
    ),
    path(
        "positions/update/<int:pk>/",
        PositionUpdateView.as_view(),
        name="position-update"
    ),
    path(
        "positions/delete/<int:pk>",
        PositionDeleteView.as_view(),
        name="position-delete"
    ),
    path(
        "positions/toggle_assing/<int:pk>",
        toggle_assign_to_task,
        name="toggle-task-assign"
    ),
]

app_name = "task_manager"
