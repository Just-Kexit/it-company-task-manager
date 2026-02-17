from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    class LevelPriority(models.TextChoices):
        URGENT = "UR", "Urgent"
        HIGH = "HG", "High"
        MEDIUM = "MD", "Medium"
        LOW = "LW", "Low"

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=2,
        choices=LevelPriority.choices,
        default=LevelPriority.LOW
    )
    task_type = models.ForeignKey(
        "TaskType",
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    assignees = models.ManyToManyField(
        "Worker",
        related_name="assigned_tasks",
        blank=True
    )

    def __str__(self):
        return (
            f"'{self.name}' - deadline: "
            f"{self.deadline.strftime("%d.%m.%Y %H:%M")}, "
            f"is completed: {self.is_completed}, "
            f"priority: {self.priority}."
        )

    def get_status_display(self):
        return "Completed" if self.is_completed else "Not completed"


class Worker(AbstractUser):
    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"

    position = models.ForeignKey(
        "Position",
        on_delete=models.CASCADE,
        related_name="workers",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("task-manager:worker-detail", kwargs={"pk": self.pk})


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
