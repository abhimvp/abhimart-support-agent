from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Customer, Order, OrderItem, Product

ASHA_ADDRESS = "12 Lake Rd, Austin, TX"
BEN_ADDRESS = "88 Pine St, Seattle, WA"


def days_ago(days: int) -> datetime:
    return datetime.now(timezone.utc) - timedelta(days=days)


def seed(session: Session) -> None:
    rows = [
        Customer(id=1001, name="Asha Rao", email="asha@example.com"),
        Customer(id=1002, name="Ben Carter", email="ben@example.com"),
        Product(
            id=1, name="Whirl 500 Blender", category="general", price=Decimal("89.00")
        ),
        Product(
            id=2,
            name="Nimbus 14 Laptop",
            category="electronics",
            price=Decimal("899.00"),
        ),
        Product(
            id=3,
            name="Ridge Trail Backpack",
            category="general",
            price=Decimal("59.00"),
        ),
        Order(
            id=1042,
            customer_id=1001,
            status="delivered",
            total=Decimal("89.00"),
            shipping_address=ASHA_ADDRESS,
            carrier="UPS",
            tracking_number="1Z999AA10001",
            placed_at=days_ago(6),
            shipped_at=days_ago(4),
            delivered_at=days_ago(2),
        ),
        Order(
            id=1043,
            customer_id=1001,
            status="shipped",
            total=Decimal("59.00"),
            shipping_address=ASHA_ADDRESS,
            carrier="FedEx",
            tracking_number="7700112233",
            placed_at=days_ago(3),
            shipped_at=days_ago(1),
        ),
        Order(
            id=1045,
            customer_id=1001,
            status="delivered",
            total=Decimal("899.00"),
            shipping_address=ASHA_ADDRESS,
            carrier="UPS",
            tracking_number="1Z999AA10045",
            placed_at=days_ago(30),
            shipped_at=days_ago(28),
            delivered_at=days_ago(25),
        ),
        Order(
            id=2001,
            customer_id=1002,
            status="delivered",
            total=Decimal("899.00"),
            shipping_address=BEN_ADDRESS,
            carrier="UPS",
            tracking_number="1Z999BB20001",
            placed_at=days_ago(9),
            shipped_at=days_ago(7),
            delivered_at=days_ago(5),
        ),
        OrderItem(order_id=1042, product_id=1, quantity=1, unit_price=Decimal("89.00")),
        OrderItem(order_id=1043, product_id=3, quantity=1, unit_price=Decimal("59.00")),
        OrderItem(
            order_id=1045, product_id=2, quantity=1, unit_price=Decimal("899.00")
        ),
        OrderItem(
            order_id=2001, product_id=2, quantity=1, unit_price=Decimal("899.00")
        ),
    ]
    for row in rows:
        session.merge(row)


if __name__ == "__main__":
    with SessionLocal.begin() as session:
        seed(session)
    print("Seeded sample data.")
