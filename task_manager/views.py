import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic

from task_manager.forms import WorkerCreationForm, TaskCreationForm, WorkerPositionUpdateForm
from task_manager.models import Worker, Task, TaskType, Position


def index(request):

    num_workers = Worker.objects.count()
    num_task = Task.objects.count()
    num_task_completed = Task.objects.filter(is_completed=True).count()
    deadline_over = Task.objects.filter(deadline__lt=datetime.datetime.now())

    context = {
        "num_workers": num_workers,
        "num_task": num_task,
        "num_task_completed": num_task_completed,
        "deadline_over": deadline_over
    }
    return render(request, "task_manager/index.html", context=context)


class WorkerListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 2
    model = Worker


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.all().select_related("position").prefetch_related("assigned_tasks")


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm


class WorkerPositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerPositionUpdateForm


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("task-manager:worker-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 2
    model = Task


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.select_related(
        "task_type"
    ).prefetch_related("assignees")


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreationForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    template_name = "task_manager/task_type_list.html"
    context_object_name = "task_type_list"


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    template_name =  "task_manager/task_type_form.html"
    success_url = reverse_lazy("task-manager:task-type-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task-manager:position-list")
