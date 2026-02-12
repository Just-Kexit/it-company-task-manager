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

#
# class LogoutCarListTest(TestCase):
#
#     def test_login_required(self):
#         login_url = settings.LOGIN_URL
#         response = self.client.get(CAR_URL)
#         self.assertRedirects(response, f"{login_url}?next={CAR_URL}")
#
#
# class LoginCarListTest(LoginMixin, TestCase):
#     def setUp(self):
#         super().setUp()
#
#         self.manufacturer = Manufacturer.objects.create(
#             name="Toyota",
#             country="DU"
#         )
#
#         number_of_car = 7
#         for car_id in range(number_of_car):
#             Car.objects.create(
#                 model=f"Test - {car_id}",
#                 manufacturer=self.manufacturer,
#             )
#
#     def test_login_car_list_and_pagination(self):
#         response = self.client.get(CAR_URL)
#
#         self.assertEqual(response.status_code, 200)
#
#         self.assertTemplateUsed(response, "taxi/car_list.html")
#
#         self.assertTrue("is_paginated" in response.context)
#         self.assertTrue(response.context["is_paginated"])
#         self.assertEqual(len(response.context["car_list"]), 5)
#
#         response2 = self.client.get(CAR_URL + "?page=2")
#         self.assertEqual(len(response2.context["car_list"]), 2)
#
#     def test_car_get_context_with_search_form(self):
#         response = self.client.get(CAR_URL + "?model=BMW")
#
#         self.assertIn("search_form", response.context)
#
#         form = response.context["search_form"]
#         self.assertEqual(form.initial["model"], "BMW")
#
#     def test_car_get_queryset_filter(self):
#
#         Car.objects.create(model="Toyota", manufacturer=self.manufacturer)
#
#         response = self.client.get(CAR_URL + "?model=Toy")
#         qs = response.context["car_list"]
#         models = [c.model for c in qs]
#
#         self.assertEqual(len(qs), 1)
#         self.assertIn("Toyota", models)
#
#     def test_toggle_assign_to_car(self):
#
#         driver = Driver.objects.get(pk=self.driver.id)
#         car = Car.objects.get(model="Test - 0")
#
#         self.assertNotIn(car, driver.cars.all())
#         response = self.client.post(
#             reverse("taxi:toggle-car-assign", args=[car.id])
#         )
#
#         driver.refresh_from_db()
#         self.assertIn(car, driver.cars.all())
#         self.assertRedirects(
#             response,
#             reverse("taxi:car-detail", args=[car.id])
#         )
#
#
# class LogoutCarCDUTest(TestCase):
#     def test_login_required(self):
#         login_url = settings.LOGIN_URL
#         response = self.client.get(reverse("taxi:car-create"))
#         self.assertRedirects(
#             response,
#             f"{login_url}?next={reverse('taxi:car-create')}"
#         )
#
#
# class LoginCarCDUTest(LoginMixin, TestCase):
#     def setUp(self):
#         super().setUp()
#
#         self.manufacturer = Manufacturer.objects.create(
#             name="BMW",
#             country="DL"
#         )
#
#     def test_car_create(self):
#
#         create_url = reverse("taxi:car-create")
#
#         data = {
#             "model": "BMW",
#             "manufacturer": self.manufacturer.id,
#             "drivers": self.driver.id
#         }
#
#         response = self.client.post(create_url, data=data)
#         self.assertRedirects(response, CAR_URL)
#
#         car = Car.objects.get(model="BMW")
#         self.assertEqual(car.manufacturer.country, "DL")
#
#     def test_car_update(self):
#
#         car = Car.objects.create(
#             model="BMW", manufacturer=self.manufacturer
#         )
#
#         data = {
#             "model": "NewBMW",
#             "manufacturer": self.manufacturer.id,
#             "drivers": self.driver.id
#         }
#
#         update_url = reverse(
#             "taxi:car-update",
#             args=[car.id]
#         )
#         response = self.client.post(update_url, data=data)
#
#         car.refresh_from_db()
#         self.assertEqual(car.model, "NewBMW")
#         self.assertRedirects(response, CAR_URL)
#
#     def test_car_delete(self):
#         car = Car.objects.create(
#             model="DeleteMe", manufacturer=self.manufacturer
#         )
#         delete_url = reverse("taxi:car-delete", args=[car.id])
#         response = self.client.post(delete_url)
#
#         self.assertEqual(Car.objects.count(), 0)
#         self.assertRedirects(response, CAR_URL)
#
#
# class LogoutDriverListTest(TestCase):
#     def test_login_required(self):
#         login_url = settings.LOGIN_URL
#         response = self.client.get(reverse("taxi:driver-list"))
#         self.assertRedirects(
#             response,
#             f"{login_url}?next={reverse('taxi:driver-list')}"
#         )
#
#
# class LoginDriverListTest(LoginMixin, TestCase):
#
#     def setUp(self):
#         super().setUp()
#
#         for i in range(7):
#             Driver.objects.create_user(
#                 username=f"user{i}",
#                 password="12345test",
#                 license_number=f"ABG1111{i}"
#             )
#
#     def test_login_driver_list_and_pagination(self):
#         response = self.client.get(DRIVER_URL)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "taxi/driver_list.html")
#
#         self.assertTrue(response.context["is_paginated"])
#         self.assertEqual(len(response.context["driver_list"]), 5)
#
#         response2 = self.client.get(DRIVER_URL + "?page=2")
#         self.assertEqual(len(response2.context["driver_list"]), 3)
#
#     def test_driver_get_context_with_search_form(self):
#         response = self.client.get(DRIVER_URL + "?username=adm")
#
#         self.assertIn("search_form", response.context)
#         form = response.context["search_form"]
#         self.assertEqual(form.initial["username"], "adm")
#
#     def test_driver_get_queryset_filter(self):
#
#         response = self.client.get(DRIVER_URL + "?username=user1")
#         qs = response.context["driver_list"]
#
#         usernames = [d.username for d in qs]
#
#         self.assertEqual(len(qs), 1)
#         self.assertIn("user1", usernames)
#
#
# class LogoutDriverCDUTest(TestCase):
#     def test_login_required(self):
#         login_url = settings.LOGIN_URL
#         url = reverse("taxi:driver-create")
#
#         response = self.client.get(url)
#
#         self.assertRedirects(
#             response,
#             f"{login_url}?next={url}"
#         )
#
#
# class LoginDriverCDUTest(LoginMixin, TestCase):
#
#     def test_driver_create(self):
#         url = reverse("taxi:driver-create")
#
#         data = {
#             "username": "newuser",
#             "password1": "StrongPass123!",
#             "password2": "StrongPass123!",
#             "license_number": "AAA00000"
#         }
#
#         response = self.client.post(url, data=data)
#         driver = Driver.objects.get(username="newuser")
#         self.assertRedirects(
#             response, reverse("taxi:driver-detail", args=[driver.id])
#         )
#         self.assertIn(
#             driver,
#             Driver.objects.all()
#         )
#
#     def test_driver_update_license(self):
#         driver = Driver.objects.create_user(
#             username="testdriver",
#             password="12345"
#         )
#
#         url = reverse("taxi:driver-update", args=[driver.id])
#
#         data = {
#             "license_number": "ABC12345"
#         }
#
#         response = self.client.post(url, data=data)
#
#         driver.refresh_from_db()
#
#         self.assertEqual(driver.license_number, "ABC12345")
#         self.assertRedirects(response, reverse("taxi:driver-list"))
#
#     def test_driver_delete(self):
#         driver = Driver.objects.create_user(
#             username="todelete",
#             password="12345",
#             license_number="DLT00012"
#         )
#
#         url = reverse("taxi:driver-delete", args=[driver.id])
#
#         response = self.client.post(url)
#
#         self.assertFalse(Driver.objects.filter(id=driver.id).exists())
#         self.assertRedirects(response, reverse("taxi:driver-list"))
