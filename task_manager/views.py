from django.http import HttpResponse
from django.shortcuts import render

from task_manager.models import Worker, Task


def index(request):

    num_workers = Worker.objects.count()
    num_task = Task.objects.count()
    num_task_in_process = Task.objects.filter(is_completed=False).count()
    num_task_is_done =  Task.objects.filter(is_completed=False).count()

    context = {
        "num_workers": num_workers,
        "num_task": num_task,
        "num_task_in_process": num_task_in_process,
        "num_task_is_done": num_task_is_done
    }
    return HttpResponse(f"<h1>IT task manager</h1> <p>Num Worker: {context["num_workers"]} </p>")