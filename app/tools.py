from langchain_core.tools import tool

from app.db import SessionLocal
from app.order_service import OrderNotFound, get_order
from app.schemas import OrderRead


@tool
def lookup_order(order_id: int) -> str:
    """Look up an order by its number. Returns its status, tracking and items."""
    with SessionLocal() as session:
        try:
            order = get_order(session, order_id)
        except OrderNotFound:
            return "No order exists with that number."
        return OrderRead.model_validate(order).model_dump_json()


TOOLS = [lookup_order]
