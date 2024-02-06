from django.test import TestCase
from django.utils import timezone

from orders.forms import OrderForm


class OrderFormTest(TestCase):
    def test_valid_form_data(self):
        form_data = {
            "user_email": "test@example.com",
            "user_name": "User",
            "start_date": timezone.now() + timezone.timedelta(hours=1),
            "end_date": timezone.now() + timezone.timedelta(hours=4),
        }
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_start_date_in_past(self):
        form_data = {
            "user_email": "test@example.com",
            "user_name": "User",
            "start_date": timezone.now() - timezone.timedelta(hours=1),
            "end_date": timezone.now() + timezone.timedelta(hours=4),
        }
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Start date must be later than the current time.",
            form.errors["__all__"],
        )

    def test_end_date_before_start_date(self):
        form_data = {
            "user_email": "test@example.com",
            "user_name": "User",
            "start_date": timezone.now() + timezone.timedelta(hours=4),
            "end_date": timezone.now() + timezone.timedelta(hours=2),
        }
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "End date must be later than start date.", form.errors["__all__"]
        )

    def test_clean_method(self):
        form_data = {
            "user_email": "test@example.com",
            "user_name": "User",
            "start_date": timezone.now() + timezone.timedelta(hours=1),
            "end_date": timezone.now() + timezone.timedelta(hours=4),
        }
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())
        cleaned_data = form.clean()
        self.assertIn("start_timestamp", cleaned_data)
        self.assertIn("end_timestamp", cleaned_data)
        self.assertIsInstance(cleaned_data["start_timestamp"], int)
        self.assertIsInstance(cleaned_data["end_timestamp"], int)

    def test_save_method(self):
        form_data = {
            "user_email": "test@example.com",
            "user_name": "User",
            "start_date": timezone.now() + timezone.timedelta(hours=1),
            "end_date": timezone.now() + timezone.timedelta(hours=4),
        }
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())
        instance = form.save(commit=False)
        self.assertEqual(instance.user_email, "test@example.com")
        self.assertEqual(instance.user_name, "User")
        self.assertIsNotNone(instance.start_timestamp)
        self.assertIsNotNone(instance.end_timestamp)
