from django.test import TestCase
from django.utils import timezone
from orders.models import Order


class OrderModelTestCase(TestCase):
    def setUp(self):
        self.order_data = {
            "user_email": "test@example.com",
            "user_name": "User",
            "start_timestamp": int(
                (timezone.now() + timezone.timedelta(hours=1)).timestamp()
            ),
            "end_timestamp": int(
                (timezone.now() + timezone.timedelta(hours=4)).timestamp()
            ),
            "cell_id": 1,
        }

    def test_order_creation(self):
        order = Order.objects.create(**self.order_data)
        self.assertIsInstance(order, Order)
        self.assertEqual(
            order.start_timestamp, self.order_data["start_timestamp"]
        )
        self.assertEqual(order.end_timestamp, self.order_data["end_timestamp"])
        self.assertEqual(order.user_email, self.order_data["user_email"])
        self.assertEqual(order.user_name, self.order_data["user_name"])
        self.assertEqual(order.cell_id, self.order_data["cell_id"])
        self.assertFalse(order.reminded)
        self.assertIsNotNone(order.created_at)

    def test_order_str_method(self):
        order = Order.objects.create(**self.order_data)
        self.assertEqual(str(order), f"Order №{order.id} - {order.user_email}")

    def test_order_start_end_datetime_properties(self):
        order = Order.objects.create(**self.order_data)
        expected_start_datetime = timezone.datetime.fromtimestamp(
            order.start_timestamp
        ).strftime("%d.%m.%y %H:%M")
        expected_end_datetime = timezone.datetime.fromtimestamp(
            order.end_timestamp
        ).strftime("%d.%m.%y %H:%M")

        self.assertEqual(order.start_datetime, expected_start_datetime)
        self.assertEqual(order.end_datetime, expected_end_datetime)
