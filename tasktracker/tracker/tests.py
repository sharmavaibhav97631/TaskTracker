from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, timedelta

from .models import Project, Task

class BaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username="vaibhav",
            password="test123"
        )

        self.other_user = User.objects.create_user(
            username="rahul",
            password="test123"
        )

        self.client.login(
            username="vaibhav",
            password="test123"
        )


class ProjectTests(BaseTestCase):

    def test_duplicate_project_name_not_allowed(self):
        response1 = self.client.post(
            "/projects/",
            {"name": "Task", "description": "First"}
        )
        self.assertEqual(response1.status_code, 302)

        self.assertEqual(
            Project.objects.filter(owner=self.user, name="Task").count(),
            1
        )

        response2 = self.client.post(
            "/projects/",
            {"name": "Task", "description": "Duplicate"}
        )
        self.assertEqual(response2.status_code, 302)

        self.assertEqual(
            Project.objects.filter(owner=self.user, name="Task").count(),
            1
        )


class TaskValidationTests(BaseTestCase):

    def test_done_task_with_future_due_date_fails(self):
        project = Project.objects.create(
            name="Project A",
            owner=self.user
        )

        future_date = date.today() + timedelta(days=3)

        with self.assertRaises(Exception):
            Task.objects.create(
                project=project,
                title="Invalid Task",
                priority=1,
                status="done",
                due_date=future_date
            )



class TaskVisibilityTests(BaseTestCase):

    def test_tasks_visibility(self):
        my_project = Project.objects.create(
            name="My Project",
            owner=self.user
        )

        other_project = Project.objects.create(
            name="Other Project",
            owner=self.other_user
        )

        Task.objects.create(
            project=my_project,
            title="My Task",
            priority=1
        )

        Task.objects.create(
            project=other_project,
            title="Assigned Task",
            priority=2,
            assignee=self.user
        )

        Task.objects.create(
            project=other_project,
            title="Hidden Task",
            priority=3
        )

        response = self.client.get("/tasks/")
        self.assertEqual(response.status_code, 200)

        titles = [t["title"] for t in response.json()]

        self.assertIn("My Task", titles)
        self.assertIn("Assigned Task", titles)
        self.assertNotIn("Hidden Task", titles)
