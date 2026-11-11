from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import text, select
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import (
    CurrentCustomer,
    create_access_token,
    verify_password,
    create_access_token,
    verify_password,
)
from app.models import Customer, Order
from app.db import engine, get_session
from app.order_service import OrderNotFound, get_customer_order
from app.schemas import ChatRequest, ChatResponse, OrderRead, Token
from app.agent import graph, RECURSION_LIMIT

from langchain_core.messages import HumanMessage

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
    order_id: int,
    customer_id: CurrentCustomer,
    session: Annotated[Session, Depends(get_session)],
) -> Order:
    try:
        return get_customer_order(session, order_id, customer_id)
    except OrderNotFound:
        raise HTTPException(status_code=404, detail="order not found")


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, customer_id: CurrentCustomer) -> ChatResponse:
    result = graph.invoke(
        {"messages": [HumanMessage(request.message)]},
        {
            "recursion_limit": RECURSION_LIMIT,
            "configurable": {"customer_id": customer_id},
        },
    )
    return ChatResponse(reply=result["messages"][-1].text)


@app.post("/auth/login", response_model=Token)
def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_session)],
) -> Token:
    customer = session.scalar(select(Customer).where(Customer.email == form.username))
    hashed = customer.password_hash if customer else None
    if not verify_password(form.password, hashed):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=create_access_token(customer.id), token_type="bearer")
