from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from task_manager.models import Worker, Task, TaskType, Position


def index(request):

    num_workers = Worker.objects.count()
    num_task = Task.objects.count()
    num_task_completed = Task.objects.filter(is_completed=True).count()

    context = {
        "num_workers": num_workers,
        "num_task": num_task,
        "num_task_completed": num_task_completed,
    }
    return render(request, "task_manager/index.html", context=context)


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.all().select_related("position").prefetch_related("assigned_tasks")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    queryset = Task.objects.select_related(
        "task_type"
    ).prefetch_related("assignees")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    template_name = "task_manager/task_type_list.html"
    context_object_name = "task_type_list"


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
