from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=schemas.ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(payload: schemas.ProductCreate, db: Session = Depends(get_db)):
    product = models.Product(
        name=payload.name,
        price=payload.price,
        stock=payload.stock,
    )
    db.add(product)
    db.commit()
    # db.refresh(product)  # GEREK YOK (expire_on_commit=False)
    return schemas.ProductOut.model_validate(product)  # <-- ORM yerine Pydantic döndür

@router.get("/", response_model=list[schemas.ProductOut])
def list_products(db: Session = Depends(get_db)):
    items = db.query(models.Product).all()
    # Doğrudan ORM listesi dönme → serialize sırasında session'a dokunabilir.
    # Güvenlisi: Pydantic'e çevirip dön.
    return [schemas.ProductOut.model_validate(it) for it in items]
