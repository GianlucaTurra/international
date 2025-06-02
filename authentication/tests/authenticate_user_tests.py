import json
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse_lazy

from authentication.models import Token


class AuthenticateUserTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="Roborbio", password="123")
        self.client = Client()
        self.url = reverse_lazy("api-1.0.0:bearer")

    def test_successful_user_authentication(self):
        response = self.client.post(
            self.url,
            json.dumps({"username": "Roborbio", "password": "123"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Token.objects.count(), 1)
