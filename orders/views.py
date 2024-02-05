import requests
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from rest_framework import viewsets, status
from rest_framework.response import Response

from orders.forms import OrderForm
from orders.models import Order
from orders.serializers import OrderSerializer


def get_random_cell_id():
    response = requests.get("https://csrng.net/csrng/csrng.php?min=1&max=50")
    data_list = response.json()
    if data_list:
        first_dict = data_list[0]
        cell_id = first_dict.get("random")
        return cell_id
    else:
        return Response(
            {"error": "Invalid response format"},
            status=status.HTTP_400_BAD_REQUEST,
        )


def validate_timestamps(start_timestamp, end_timestamp):
    if (
        int(end_timestamp) <= int(start_timestamp)
        or int(start_timestamp) <= timezone.now().timestamp()
    ):
        return Response(
            {"error": "Invalid timestamps"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return None


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
        cell_id = get_random_cell_id()
        validation_timestamps = validate_timestamps(
            start_timestamp, end_timestamp
        )
        if validation_timestamps:
            return validation_timestamps

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


class OrderView(View):
    def get(self, request):
        form = OrderForm()
        return render(request, "orders/order_form.html", {"form": form})

    def post(self, request):
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.cell_id = get_random_cell_id()
            order.save()
            return redirect(f"/orders/{order.slug}/")
        else:
            return render(
                request,
                "orders/order_form.html",
                {"form": form, "error": "Invalid form data"},
            )
