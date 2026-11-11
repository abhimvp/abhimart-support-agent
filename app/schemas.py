# Models describe the database, and schemas describe the API.
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    category: str


class OrderItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product: ProductRead
    quantity: int
    unit_price: Decimal


class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    status: str
    total: Decimal
    shipping_address: str
    carrier: str | None
    tracking_number: str | None
    placed_at: datetime
    shipped_at: datetime | None
    delivered_at: datetime | None
    items: list[OrderItemRead]


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)


# The length limit stops someone sending a huge message that you’d pay tokens for.


class ChatResponse(BaseModel):
    reply: str


class Token(BaseModel):
    access_token: str
    token_type: str
