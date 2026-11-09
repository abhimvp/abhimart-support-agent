from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Order, OrderItem


class OrderNotFound(Exception):
    pass


def get_order(session: Session, order_id: int) -> Order:
    order = session.scalar(
        select(Order)
        .where(Order.id == order_id)
        .options(selectinload(Order.items).selectinload(OrderItem.product))
    )
    if order is None:
        raise OrderNotFound(order_id)
    return order
