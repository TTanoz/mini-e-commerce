from .factories import auth_token_for, make_product_api

def test_add_to_cart_requires_auth(client):
    payload = {"product_id":1,"quantity":1}
    res = client.post("/cart/add", json = payload)
    assert res.status_code == 401

def test_add_to_cart_creates_new_item_or_increments(client):
    token = auth_token_for(client)
    p = make_product_api(client, name="USB", price=50.0, stock=7)

    headers = {"Authorization": f"Bearer {token}"}

    res1 = client.post("/cart/add", headers=headers,
                       json={"product_id": p["id"], "quantity": 2})
    assert res1.status_code == 201
    assert res1.json()["quantity"] == 2

    res2 = client.post("/cart/add", headers=headers,
                       json={"product_id": p["id"], "quantity": 3})
    assert res2.status_code == 201
    assert res2.json()["quantity"] == 5

def test_view_cart_shows_user_items(client):
    token = auth_token_for(client=client)
    p = make_product_api(client, "HDMI", 30.0, 5)
    headers = {"Authorization": f"Bearer {token}"}
    client.post("/cart/add", headers=headers, json={"product_id": p["id"], "quantity": 1})
    res = client.get("/cart/", headers=headers)
    assert res.status_code==200
    data = res.json()
    assert any(item["product_id"] == p["id"] for item in data)
