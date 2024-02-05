from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from orders.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "user_email",
            "user_name",
            "start_timestamp",
            "end_timestamp",
        ]

    def clean(self):
        cleaned_data = super().clean()
        end_timestamp = self.cleaned_data.get("end_timestamp")
        start_timestamp = self.cleaned_data.get("start_timestamp")

        if end_timestamp and start_timestamp:
            if start_timestamp <= timezone.now().timestamp():
                raise ValidationError(
                    "Start timestamps must be later than the current time."
                )

            if end_timestamp <= start_timestamp:
                raise ValidationError(
                    "End timestamp must be later than start timestamp."
                )

        return cleaned_data
