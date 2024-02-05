import uuid

from django.db import models
from django.utils import timezone


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    start_timestamp = models.BigIntegerField()
    end_timestamp = models.BigIntegerField()
    user_email = models.EmailField()
    user_name = models.CharField(max_length=255)
    cell_id = models.PositiveIntegerField()
    reminded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def start_datetime(self):
        return timezone.datetime.fromtimestamp(self.start_timestamp).strftime(
            "%d.%m.%y %H:%M"
        )

    @property
    def end_datetime(self):
        return timezone.datetime.fromtimestamp(self.end_timestamp).strftime(
            "%d.%m.%y %H:%M"
        )

    def __str__(self):
        return f"Order №{self.id} - {self.user_email}"

    class Meta:
        ordering = ["-created_at"]
