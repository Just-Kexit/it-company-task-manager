from datetime import datetime

from django.forms import CheckboxSelectMultiple, DateTimeInput
from django.forms.widgets import TextInput
from django.test import TestCase

from task_manager.forms import (
    WorkerCreationForm,
    TaskForm,
    WorkerPositionUpdateForm,
    WorkerSearchUsernameForm,
    TaskSearchNameForm,
)
from task_manager.models import Position, Task, TaskType


class TaskFormTest(TestCase):

    def test_field_assignees_deadline_and_widget_in_form(self):
        form = TaskForm()
        self.assertIn("assignees", form.fields)
        self.assertIsInstance(
            form.fields["assignees"].widget, CheckboxSelectMultiple
        )
        self.assertIn("deadline", form.fields)
        self.assertIsInstance(
            form.fields["deadline"].widget, DateTimeInput
        )

    def test_search_task_form(self):
        form = TaskSearchNameForm()
        self.assertIn("name", form.fields)
        self.assertIsInstance(form.fields["name"].widget, TextInput)

        widget = form.fields["name"].widget
        self.assertIn("placeholder", widget.attrs)
        self.assertEqual(widget.attrs["placeholder"], "Search by name")

    def test_task_form_behavior(self):

        task_type = TaskType.objects.create(
            name="Bug",
        )
        task = Task.objects.create(
                name="Fix",
                task_type=task_type,
                deadline=datetime.now(),
            )
        create_form = TaskForm()
        self.assertNotIn("is_completed", create_form.fields)

        update_form = TaskForm(instance=task)
        self.assertIn("is_completed", update_form.fields)


class WorkerFormTest(TestCase):

    def setUp(self):
        self.position = Position.objects.create(name="QA")

    def test_field_position_first_last_name(self):

        form_data = {
            "username": "john_test",
            "password1": "test123Strong",
            "password2": "test123Strong",
            "position": self.position,
            "first_name": "John",
            "last_name": "Carter"
        }
        form = WorkerCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["username"],
            form_data["username"]
        )
        self.assertEqual(
            form.cleaned_data["position"],
            form_data["position"]
        )
        self.assertEqual(
            form.cleaned_data["first_name"],
            form_data["first_name"]
        )
        self.assertEqual(
            form.cleaned_data["last_name"],
            form_data["last_name"]
        )

    def test_search_worker_form(self):
        form = WorkerSearchUsernameForm()
        self.assertIn("username", form.fields)
        self.assertIsInstance(form.fields["username"].widget, TextInput)

        widget = form.fields["username"].widget
        self.assertIn("placeholder", widget.attrs)
        self.assertEqual(widget.attrs["placeholder"], "Search by username")

    def test_update_position_form(self):
        form = WorkerPositionUpdateForm()
        self.assertIn("position", form.fields)
