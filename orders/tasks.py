from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string

from cell_rental import settings
from orders.models import Order


@shared_task
def send_email_task(order_id):
    order = Order.objects.get(pk=order_id)
    subject = f"Order #{order.id}"
    message = ""
    from_email = settings.EMAIL_HOST_USER
    to_email = [order.user_email]
    html_message = render_to_string(
        "orders/email_template.html", {"order": order}
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=to_email,
        html_message=html_message,
    )
