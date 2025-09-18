from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas
from ..deps import get_current_user

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/add", response_model=schemas.CartItemOut, status_code=status.HTTP_201_CREATED)
def add_to_cart(
    payload: schemas.CartAdd,
    db: Session = Depends(get_db),
    user: Annotated[models.User, Depends(get_current_user)] = None,
):
    prod = db.get(models.Product, payload.product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")

    item = (
        db.query(models.CartItem)
        .filter_by(user_id=user.id, product_id=payload.product_id)
        .first()
    )
    if item:
        item.quantity += payload.quantity
    else:
        item = models.CartItem(
            user_id=user.id,
            product_id=payload.product_id,
            quantity=payload.quantity,
        )
        db.add(item)

    db.commit()
    db.refresh(item)
    return item

@router.get("/", response_model=list[schemas.CartItemOut])
def view_cart(
    db: Session = Depends(get_db),
    user: Annotated[models.User, Depends(get_current_user)] = None,
):
    items = db.query(models.CartItem).filter_by(user_id=user.id).all()
    return items
