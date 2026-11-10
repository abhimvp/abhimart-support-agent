from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime

from app.db import SessionLocal
from app.order_service import OrderNotFound, get_customer_order
from app.schemas import OrderRead


@tool
def lookup_order(order_id: int, runtime: ToolRuntime) -> str:
    """Look up one of the logged-in customer's orders by its number."""
    customer_id = runtime.config.get("configurable", {}).get("customer_id")
    if customer_id is None:
        return "The customer is not logged in, so order details are unavailable."
    with SessionLocal() as session:
        try:
            order = get_customer_order(session, order_id, customer_id)
        except OrderNotFound:
            return "This customer has no order with that number."
        return OrderRead.model_validate(order).model_dump_json()


TOOLS = [lookup_order]
