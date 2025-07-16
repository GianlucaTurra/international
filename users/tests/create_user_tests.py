import json

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class CreateUserTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.url = reverse("api-1.0.0:create_user")

    def test_missing_password(self):
        response = self.client.post(
            self.url,
            json.dumps({"username": "rob", "email": "yoyo@yahoo.com"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 422)

    def test_simple_user_creation(self):
        response = self.client.post(
            self.url,
            json.dumps(
                {
                    "username": "roborbio",
                    "password": "pasw123",
                    "email": "some@email.com",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
