from app.models import Product, User
from app.core.security import hash_pw

def make_product(db_session, name="Item", price=10.50, stock=5) -> Product:
    p = Product(name=name, price=price, stock=stock)
    db_session.add(p); db_session.commit(); db_session.refresh(p)
    return p

def make_user(db_session, email: str = "u@test.com", password: str = "Passw0rd!") -> User:
    hashed = hash_pw(password)
    user = User(email=email, password_hash=hashed)
    db_session.add(user); db_session.commit(); db_session.refresh(user)
    return user

def auth_token_for(client, email="u@test.com", password="Passw0rd!"):
    client.post("/auth/register", json={"email": email, "password": password})
    res = client.post("/auth/login", json={"email": email, "password": password})
    assert res.status_code == 200, res.text
    return res.json()["access_token"]

def make_product_api(client, name="Item", price=10.50, stock=5):
    res = client.post("/products/", json={"name": name, "price": price, "stock": stock})
    assert res.status_code in (200, 201), res.text
    return res.json() 