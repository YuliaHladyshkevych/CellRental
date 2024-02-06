import unittest.mock

from django.test import TestCase, Client, RequestFactory
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from orders.models import Order
from orders.views import OrderView


class OrderViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    @unittest.mock.patch("orders.views.get_random_cell_id")
    def test_create_order_success(self, mock_get_random_cell_id):
        mock_get_random_cell_id.return_value = 1
        data = {
            "start_timestamp": int(
                (timezone.now() + timezone.timedelta(hours=1)).timestamp()
            ),
            "end_timestamp": int(
                (timezone.now() + timezone.timedelta(hours=4)).timestamp()
            ),
            "user_data": {"email": "test@example.com", "name": "User"},
        }
        response = self.client.post("/api/v1/orders/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

    def test_create_order_invalid_input_data(self):
        invalid_data = {
            "start_timestamp": int(
                (timezone.now() + timezone.timedelta(hours=1)).timestamp()
            ),
            "user_data": {
                "email": "test@example.com",
            },
        }
        response = self.client.post(
            "/api/v1/orders/", invalid_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_invalid_timestamps(self):
        invalid_timestamps_data = {
            "start_timestamp": int(
                (timezone.now() + timezone.timedelta(hours=1)).timestamp()
            ),
            "end_timestamp": int(
                (timezone.now() - timezone.timedelta(hours=1)).timestamp()
            ),
            "user_data": {
                "email": "test@example.com",
                "name": "John Doe",
            },
        }
        response = self.client.post(
            "/api/v1/orders/", invalid_timestamps_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OrderViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.view = OrderView.as_view()

    @unittest.mock.patch("orders.views.get_random_cell_id")
    def test_get_order_form(self, mock_get_random_cell_id):
        mock_get_random_cell_id.return_value = 1
        request = self.factory.get("/orders/")
        response = self.view(request)

        self.assertEqual(response.status_code, 200)

    @unittest.mock.patch("orders.views.get_random_cell_id")
    def test_post_valid_order_form(self, mock_get_random_cell_id):
        mock_get_random_cell_id.return_value = 1
        data = {
            "user_email": "test@example.com",
            "user_name": "User",
            "start_date": timezone.now() + timezone.timedelta(hours=1),
            "end_date": timezone.now() + timezone.timedelta(hours=4),
        }

        request = self.factory.post("/orders/", data)
        response = self.view(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.first().cell_id, 1)

    def test_post_invalid_order_form(self):
        data = {
            "user_email": "test@example.com",
            "user_name": "User",
            "start_date": timezone.now() + timezone.timedelta(hours=4),
            "end_date": timezone.now() + timezone.timedelta(hours=2),
        }

        request = self.factory.post("/orders/", data)
        response = self.view(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"alert-danger", response.content)
