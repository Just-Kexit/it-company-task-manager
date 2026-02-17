from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Worker, Task, TaskType, Position

TASK_URL = reverse("task_manager:task-list")
TASK_TYPE_URL = reverse("task_manager:task-type-list")
WORKER_URL = reverse("task_manager:worker-list")
POSITION_URL = reverse("task_manager:position-list")
INDEX_URL = reverse("task-manager:index")


class LoginMixin:

    def setUp(self):
        super().setUp()

        self.worker = get_user_model().objects.create_user(
            username="john_test",
            password="test123",

        )
        self.client.force_login(self.worker)


class LogoutIndexPageTests(TestCase):

    def test_login_required(self):
        login_url = settings.LOGIN_URL
        response = self.client.get(INDEX_URL)
        self.assertRedirects(
            response,
            f"{login_url}?next={INDEX_URL}"
        )


class LoginIndexPageTests(LoginMixin, TestCase):

    def test_index_for_displaying_context_and_counters(self):
        response = self.client.get(INDEX_URL)

        self.assertIn("num_workers", response.context)
        self.assertIn("num_task", response.context)
        self.assertIn("num_task_completed", response.context)
        self.assertIn("deadline_over", response.context)

        self.assertEqual(
            response.context["num_workers"],
            Worker.objects.count()
        )
        self.assertEqual(
            response.context["num_task"],
            Task.objects.count()
        )
        self.assertEqual(
            response.context["num_task_completed"],
            Task.objects.filter(is_completed=True).count()
        )
        self.assertEqual(
            list(response.context["deadline_over"]),
            list(Task.objects.filter(deadline__lt=datetime.now()))
        )


class LogoutPositionListTests(TestCase):

    def test_login_required(self):
        login_url = settings.LOGIN_URL
        response = self.client.get(POSITION_URL)
        self.assertRedirects(response, f"{login_url}?next={POSITION_URL}")


class LoginPositionListTest(LoginMixin, TestCase):

    def setUp(self):
        super().setUp()

        number_of_position = 7

        for position_id in range(number_of_position):
            Position.objects.create(
                name=f"Test - {position_id}",
            )

    def test_login_manufacturer(self):
        response = self.client.get(POSITION_URL)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "task_manager/position_list.html")

        self.assertEqual(len(response.context["position_list"]), 7)


class LogoutPositionCDUTest(TestCase):

    def test_login_required(self):
        login_url = settings.LOGIN_URL
        response = self.client.get(reverse("task-manager:position-create"))
        self.assertRedirects(
            response,
            f"{login_url}?next={reverse('task-manager:position-create')}"
        )


class LoginPositionCDUTest(LoginMixin, TestCase):

    def test_position_create(self):

        create_url = reverse("task-manager:position-create")
        data = {
            "name": "QA",
        }

        response = self.client.post(create_url, data=data)
        self.assertRedirects(response, POSITION_URL)

        position = Position.objects.get(name="QA")
        self.assertEqual(position.name, "QA")

    def test_position_update(self):

        position = Position.objects.create(
            name="Old",
        )
        data = {
            "name": "New",
        }
        update_url = reverse(
            "task-manager:position-update",
            args=[position.id]
        )
        response = self.client.post(update_url, data=data)

        position.refresh_from_db()
        self.assertEqual(position.name, "New")
        self.assertRedirects(response, POSITION_URL)

    def test_manufacturer_delete(self):

        position = Position.objects.create(
            name="DeleteMe",
        )
        delete_url = reverse(
            "task-manager:position-delete",
            args=[position.id]
        )
        response = self.client.post(delete_url)

        self.assertEqual(Position.objects.count(), 0)
        self.assertRedirects(response, POSITION_URL)


class LogoutTaskTypeListTests(TestCase):

    def test_login_required(self):
        login_url = settings.LOGIN_URL
        response = self.client.get(TASK_TYPE_URL)
        self.assertRedirects(response, f"{login_url}?next={TASK_TYPE_URL}")


class LoginTaskTypeListTest(LoginMixin, TestCase):

    def setUp(self):
        super().setUp()

        number_of_task_type = 7

        for task_type_id in range(number_of_task_type):
            TaskType.objects.create(
                name=f"Test - {task_type_id}",
            )

    def test_login_manufacturer(self):
        response = self.client.get(TASK_TYPE_URL)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "task_manager/task_type_list.html")

        self.assertEqual(len(response.context["task_type_list"]), 7)


class LogoutTaskTypeCDUTest(TestCase):

    def test_login_required(self):
        login_url = settings.LOGIN_URL
        response = self.client.get(reverse("task-manager:task-type-create"))
        self.assertRedirects(
            response,
            f"{login_url}?next={reverse('task-manager:task-type-create')}"
        )


class LoginTaskTypeCDUTest(LoginMixin, TestCase):

    def test_task_type_create(self):

        create_url = reverse("task-manager:task-type-create")
        data = {
            "name": "Bug",
        }

        response = self.client.post(create_url, data=data)
        self.assertRedirects(response, TASK_TYPE_URL)

        task_type = TaskType.objects.get(name="Bug")
        self.assertEqual(task_type.name, "Bug")

    def test_task_type_update(self):

        task_type = TaskType.objects.create(
            name="Old",
        )
        data = {
            "name": "New",
        }
        update_url = reverse(
            "task-manager:task-type-update",
            args=[task_type.id]
        )
        response = self.client.post(update_url, data=data)

        task_type.refresh_from_db()
        self.assertEqual(task_type.name, "New")
        self.assertRedirects(response, TASK_TYPE_URL)

    def test_task_type_delete(self):

        task_type = TaskType.objects.create(
            name="DeleteMe",
        )
        delete_url = reverse(
            "task-manager:task-type-delete",
            args=[task_type.id]
        )
        response = self.client.post(delete_url)

        self.assertEqual(Position.objects.count(), 0)
        self.assertRedirects(response, TASK_TYPE_URL)


class LogoutTaskListTest(TestCase):

    def test_login_required(self):
        login_url = settings.LOGIN_URL
        response = self.client.get(TASK_URL)
        self.assertRedirects(response, f"{login_url}?next={TASK_URL}")


class LoginTaskListTest(LoginMixin, TestCase):
    def setUp(self):
        super().setUp()

        self.task_type = TaskType.objects.create(
            name="Bug",
        )

        number_of_task = 7
        for task_id in range(number_of_task):
            Task.objects.create(
                name=f"Fix - {task_id}",
                task_type=self.task_type,
                deadline=datetime.now(),
            )

    def test_login_task_list_and_pagination(self):
        response = self.client.get(TASK_URL)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "task_manager/task_list.html")

        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["task_list"]), 2)

        response2 = self.client.get(TASK_URL + "?page=4")
        self.assertEqual(len(response2.context["task_list"]), 1)

    def test_task_get_context_with_search_form(self):
        response = self.client.get(TASK_URL + "?name=Fix")

        self.assertIn("search_form", response.context)

        form = response.context["search_form"]
        self.assertEqual(form.initial["name"], "Fix")

    def test_task_get_queryset_filter(self):

        Task.objects.create(
            name="Feature",
            task_type=self.task_type,
            deadline=datetime.now(),
        )

        response = self.client.get(TASK_URL + "?name=Fea")
        qs = response.context["task_list"]
        name = [c.name for c in qs]

        self.assertEqual(len(qs), 1)
        self.assertIn("Feature", name)

    def test_toggle_assign_to_task(self):

        worker = Worker.objects.get(pk=self.worker.id)
        task = Task.objects.get(name="Fix - 0")

        self.assertNotIn(task, worker.assigned_tasks.all())
        response = self.client.post(
            reverse("task-manager:toggle-task-assign", args=[worker.id])
        )

        worker.refresh_from_db()
        self.assertIn(task, worker.assigned_tasks.all())
        self.assertRedirects(
            response,
            reverse("task-manager:task-detail", args=[task.id])
        )


class LogoutTaskCDUTest(TestCase):
    def test_login_required(self):
        login_url = settings.LOGIN_URL
        response = self.client.get(reverse("task-manager:task-create"))
        self.assertRedirects(
            response,
            f"{login_url}?next={reverse('task-manager:task-create')}"
        )


class LoginTaskCDUTest(LoginMixin, TestCase):
    def setUp(self):
        super().setUp()

        self.task_type = TaskType.objects.create(
            name="Bug",
        )

    def test_task_create(self):

        create_url = reverse("task-manager:task-create")

        data = {
            "name": "Fix",
            "task_type": self.task_type.id,
            "assignees": self.worker.id,
            "is_completed": False,
            "deadline": datetime.now(),
            "priority": "LW"
        }

        response = self.client.post(create_url, data=data)
        if response.status_code != 302:
            print(response.context['form'].errors)
        self.assertRedirects(response, TASK_URL)

        task = Task.objects.get(name="Fix")
        self.assertEqual(task.task_type.name, "Bug")

    def test_task_update(self):

        task = Task.objects.create(
            name="Feature",
            task_type=self.task_type,
            deadline=datetime.now(),
        )

        data = {
            "name": "NewFeature",
            "task_type": self.task_type.id,
            "assignees": self.worker.id,
            "is_completed": False,
            "deadline": datetime.now(),
            "priority": "LW"
        }

        update_url = reverse(
            "task-manager:task-update",
            args=[task.id]
        )
        response = self.client.post(update_url, data=data)

        task.refresh_from_db()
        self.assertEqual(task.name, "NewFeature")
        self.assertRedirects(response, TASK_URL)

    def test_task_delete(self):
        task = Task.objects.create(
            name="DeleteMe",
            task_type=self.task_type,
            deadline=datetime.now(),
        )
        delete_url = reverse("task-manager:task-delete", args=[task.id])
        response = self.client.post(delete_url)

        self.assertEqual(Task.objects.count(), 0)
        self.assertRedirects(response, TASK_URL)


class LogoutWorkerListTest(TestCase):
    def test_login_required(self):
        login_url = settings.LOGIN_URL
        response = self.client.get(reverse("task-manager:worker-list"))
        self.assertRedirects(
            response,
            f"{login_url}?next={reverse('task-manager:worker-list')}"
        )


class LoginWorkerListTest(LoginMixin, TestCase):

    def setUp(self):
        super().setUp()

        self.position = Position.objects.create(
            name="Test"
        )

        for i in range(6):
            Worker.objects.create_user(
                username=f"user{i}",
                password="12345test",
                position=self.position
            )

    def test_login_worker_list_and_pagination(self):
        response = self.client.get(WORKER_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/worker_list.html")

        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["worker_list"]), 2)

        response2 = self.client.get(WORKER_URL + "?page=4")
        self.assertEqual(len(response2.context["worker_list"]), 1)

    def test_worker_get_context_with_search_form(self):
        response = self.client.get(WORKER_URL + "?username=adm")

        self.assertIn("search_form", response.context)
        form = response.context["search_form"]
        self.assertEqual(form.initial["username"], "adm")

    def test_worker_get_queryset_filter(self):

        response = self.client.get(WORKER_URL + "?username=user1")
        qs = response.context["worker_list"]

        usernames = [d.username for d in qs]

        self.assertEqual(len(qs), 1)
        self.assertIn("user1", usernames)


class LogoutWorkerCDUTest(TestCase):
    def test_login_required(self):
        login_url = settings.LOGIN_URL
        url = reverse("task-manager:worker-create")

        response = self.client.get(url)

        self.assertRedirects(
            response,
            f"{login_url}?next={url}"
        )


class LoginWorkerCDUTest(LoginMixin, TestCase):

    def test_worker_create(self):
        position = Position.objects.create(
            name="QA"
        )
        url = reverse("task-manager:worker-create")

        data = {
            "username": "New_user",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "position": position.id
        }

        response = self.client.post(url, data=data)
        worker = Worker.objects.get(username="New_user")
        self.assertRedirects(
            response, reverse("task-manager:worker-detail", args=[worker.id])
        )
        self.assertIn(
            worker,
            Worker.objects.all()
        )

    def test_worker_update_position(self):
        position = Position.objects.create(
            name="PH"
        )
        position2 = Position.objects.create(
            name="QA"
        )

        worker = Worker.objects.create_user(
            username="Test_worker",
            password="12345",
            position=position
        )

        url = reverse("task-manager:worker-update", args=[worker.id])

        data = {
            "position": position2.id
        }

        response = self.client.post(url, data=data)

        worker.refresh_from_db()
        self.assertEqual(worker.position.name, "QA")
        self.assertRedirects(
            response,
            reverse("task-manager:worker-detail", args=[worker.id])
        )

    def test_worker_delete(self):
        position = Position.objects.create(
            name="PH"
        )
        worker = Worker.objects.create_user(
            username="Test_worker",
            password="12345",
            position=position
        )

        url = reverse("task-manager:worker-delete", args=[worker.id])

        response = self.client.post(url)

        self.assertFalse(Worker.objects.filter(id=worker.id).exists())
        self.assertRedirects(response, reverse("task-manager:worker-list"))
