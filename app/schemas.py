from pydantic import BaseModel, EmailStr, conint, ConfigDict

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ProductCreate(BaseModel):
    name: str
    price: float
    stock: conint(ge=0)

class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    model_config = ConfigDict(from_attributes=True)

class CartAdd(BaseModel):
    product_id: int
    quantity: conint(ge=1)

class CartItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    model_config = ConfigDict(from_attributes=True)

class OrderOutItem(BaseModel):
    product_id: int
    unit_price: float
    quantity: int
    model_config = ConfigDict(from_attributes=True)

class OrderOut(BaseModel):
    id: int
    total_amount: float
    status: str
    items: list[OrderOutItem]
    model_config = ConfigDict(from_attributes=True)
