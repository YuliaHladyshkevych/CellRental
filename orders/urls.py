from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderView

router = DefaultRouter()
router.register(r"api/v1/orders", OrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("orders/", OrderView.as_view(), name="order_form"),
]

app_name = "orders"
