from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app.db import engine, get_session
from app.models import Order
from app.order_service import OrderNotFound, get_order
from app.schemas import OrderRead

app = FastAPI(title="abhimart support agent")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready")
def ready() -> dict[str, str]:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except OperationalError:
        raise HTTPException(status_code=503, detail="database unavailable")
    return {"status": "ready"}


@app.get("/orders/{order_id}", response_model=OrderRead)
def read_order(
    order_id: int, session: Annotated[Session, Depends(get_session)]
) -> Order:
    try:
        return get_order(session, order_id)
    except OrderNotFound:
        raise HTTPException(status_code=404, detail="order not found")
