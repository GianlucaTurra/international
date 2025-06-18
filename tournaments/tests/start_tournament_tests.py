from django.test import Client, TestCase
from django.urls import reverse_lazy


# class StartTournamentTestCase(TestCase):
#     def setUp(self) -> None:
#         self.client = Client()
#         self.url = reverse_lazy("api-1.0.0:create_tournament")

#     def test_round_start(self):
#         response = self.client.post(self.url)
#         self.assertEqual(response.status_code, 201)
