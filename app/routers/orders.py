# app/routers/orders.py
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from ..database import get_db
from .. import models, schemas
from ..deps import get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=schemas.OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(
    db: Session = Depends(get_db),
    user: Annotated[models.User, Depends(get_current_user)] = None,
):
    cart_items: list[models.CartItem] = (
        db.execute(
            select(models.CartItem).where(models.CartItem.user_id == user.id)
        ).scalars().all()
    )
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    product_ids = [ci.product_id for ci in cart_items]
    products = {
        p.id: p for p in db.execute(
            select(models.Product).where(models.Product.id.in_(product_ids))
        ).scalars().all()
    }
    for ci in cart_items:
        p = products.get(ci.product_id)
        if not p:
            raise HTTPException(status_code=404, detail=f"Product {ci.product_id} not found")
        if p.stock < ci.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {p.id}")

    order = models.Order(user_id=user.id, status="CREATED", total_amount=0)
    db.add(order)
    db.flush()
    total = 0.0
    for ci in cart_items:
        p = products[ci.product_id]
        line_total = float(p.price) * ci.quantity
        total += line_total

        db.add(models.OrderItem(
            order_id=order.id,
            product_id=p.id,
            unit_price=float(p.price),
            quantity=ci.quantity,
        ))
        p.stock -= ci.quantity

    order.total_amount = total

    for ci in cart_items:
        db.delete(ci)

    db.commit()

    order = db.execute(
        select(models.Order)
        .options(selectinload(models.Order.items))
        .where(models.Order.id == order.id)
    ).scalar_one()

    return schemas.OrderOut.model_validate(order)
