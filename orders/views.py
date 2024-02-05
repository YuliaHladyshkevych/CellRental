import requests
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response

from orders.models import Order
from orders.serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        start_timestamp = request.data.get("start_timestamp")
        end_timestamp = request.data.get("end_timestamp")
        user_data = request.data.get("user_data", {})

        # Validate input data
        if not (
            start_timestamp
            and end_timestamp
            and user_data.get("email")
            and user_data.get("name")
        ):
            return Response(
                {"error": "Invalid input data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get random cell_id
        response = requests.get(
            "https://csrng.net/csrng/csrng.php?min=1&max=50"
        )
        data_list = response.json()
        if data_list:
            first_dict = data_list[0]
            cell_id = first_dict.get("random")
        else:
            return Response(
                {"error": "Invalid response format"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate timestamps
        if (
            int(end_timestamp) <= int(start_timestamp)
            or int(end_timestamp) <= timezone.now().timestamp()
        ):
            return Response(
                {"error": "Invalid timestamps"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create Order object
        order_data = {
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp,
            "user_email": user_data["email"],
            "user_name": user_data["name"],
            "cell_id": cell_id,
        }
        serializer = OrderSerializer(data=order_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
