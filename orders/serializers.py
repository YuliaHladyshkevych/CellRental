from rest_framework import serializers

from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "id",
            "slug",
            "start_timestamp",
            "end_timestamp",
            "user_email",
            "user_name",
            "cell_id",
            "reminded",
            "created_at",
        )
