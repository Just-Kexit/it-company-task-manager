from django.shortcuts import render
from django.views import generic

from task_manager.models import Worker, Task, TaskType, Position


def index(request):

    num_workers = Worker.objects.count()
    num_task = Task.objects.count()
    num_task_completed =  Task.objects.filter(is_completed=True).count()

    context = {
        "num_workers": num_workers,
        "num_task": num_task,
        "num_task_completed": num_task_completed,
    }
    return render(request, "task_manager/index.html", context=context)


class WorkerListView(generic.ListView):
    model = Worker
