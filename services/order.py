import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order
from db.models import Ticket
from db.models import User


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime.date = None
) -> None:
    with transaction.atomic():
        order = Order.objects.create(user=User.objects.get(username=username))
        if date:
            Order.objects.filter(pk=order.id).update(created_at=date)

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(
        username: str = None
) -> QuerySet[Order]:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)

    return orders
