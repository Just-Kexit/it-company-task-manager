from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Task, TaskType, Position


class ModelTest(TestCase):

    def setUp(self):
        self.worker = get_user_model().objects.create_user(
            username="Test",
            password="test123",
        )
        self.position = Position.objects.create(
            name="Test",
        )
        self.task_type = TaskType.objects.create(
            name="Test"
        )
        self.task = Task.objects.create(
            name="Test",
            task_type=self.task_type,
            deadline=datetime.now(),
        )

    def test_task_str(self):
        self.assertEqual(
            str(self.task), (
                f"'{self.task.name}' - deadline: "
                f"{self.task.deadline.strftime("%d.%m.%Y %H:%M")}, "
                f"is completed: {self.task.is_completed}, "
                f"priority: {self.task.priority}."
            )
        )

    def test_task_get_status_display_str(self):
        self.assertEqual(self.task.get_status_display(), "Not completed")

        self.task.is_completed = True

        self.assertEqual(self.task.get_status_display(), "Completed")

    def test_worker_str(self):
        self.assertEqual(
            str(self.worker),
            f"{self.worker.username} ({self.worker.first_name} "
            f"{self.worker.last_name})"
        )

    def test_worker_get_absolute_url(self):
        self.assertEqual(
            self.worker.get_absolute_url(),
            reverse(
                "task-manager:worker-detail", kwargs={"pk": self.worker.pk}
            )
        )

    def test_position_str(self):
        self.assertEqual(str(self.position), self.task.name)

    def test_task_type_str(self):
        self.assertEqual(str(self.task_type), self.task_type.name)
