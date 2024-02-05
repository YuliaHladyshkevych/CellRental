from django import forms
from django.utils import timezone

from orders.models import Order


class OrderForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        input_formats=["%Y-%m-%dT%H:%M"],
    )
    end_date = forms.DateTimeField(
        input_formats=["%d.%m.%Y %H:%M"],
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )

    class Meta:
        model = Order
        fields = [
            "user_email",
            "user_name",
            "start_date",
            "end_date",
        ]

    def clean(self):
        cleaned_data = super().clean()
        end_date = self.cleaned_data.get("end_date")
        start_date = self.cleaned_data.get("start_date")

        if end_date and start_date:
            if start_date <= timezone.now():
                raise forms.ValidationError(
                    "Start date must be later than the current time."
                )

            if end_date <= start_date:
                raise forms.ValidationError(
                    "End date must be later than start date."
                )

            cleaned_data["start_timestamp"] = int(start_date.timestamp())
            cleaned_data["end_timestamp"] = int(end_date.timestamp())

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.start_timestamp = self.cleaned_data.get("start_timestamp")
        instance.end_timestamp = self.cleaned_data.get("end_timestamp")
        if commit:
            instance.save()
        return instance
