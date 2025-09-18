from .factories import auth_token_for, make_product_api

def test_create_order_from_cart_decrements_stock_and_empties_cart(client):
    token = auth_token_for(client)
    p1 = make_product_api(client, "Keyboard", 100.0, 5)
    p2 = make_product_api(client, "Mouse", 50.0, 10)
    headers = {"Authorization": f"Bearer {token}"}

    client.post("/cart/add", headers=headers, json={"product_id": p1["id"], "quantity": 2})
    client.post("/cart/add", headers=headers, json={"product_id": p2["id"], "quantity": 3})

    res = client.post("/orders/", headers=headers)
    assert res.status_code in (200, 201)
    order = res.json()

    assert order["status"] in ["CREATED", "PAID"]
    assert len(order["items"]) == 2
    expected_total = 2*100.0 + 3*50.0
    assert abs(order["total_amount"] - expected_total) < 1e-6
    products = client.get("/products/").json()
    p1_row = next(p for p in products if p["id"] == p1["id"])
    p2_row = next(p for p in products if p["id"] == p2["id"])
    assert p1_row["stock"] == 3
    assert p2_row["stock"] == 7

    cart = client.get("/cart/", headers=headers).json()
    assert cart == []

def test_insufficient_stock_returns_400_and_no_side_effects(client):
    token = auth_token_for(client)
    p = make_product_api(client, "Keyboard", 100.0, 1)
    headers = {"Authorization": f"Bearer {token}"}
    client.post("/cart/add", headers=headers, json={"product_id": p["id"], "quantity": 2})
    res = client.post("/orders/", headers=headers)
    assert res.status_code == 400
    products = client.get("/products/").json()
    prow = next(x for x in products if x["id"] == p["id"])
    assert prow["stock"] == 1

def test_two_orders_for_same_product_cannot_oversell(client):
    p = make_product_api(client, "GPU", 1000.0, stock=3)
    tokenA = auth_token_for(client, "a@a.com", "x")
    headersA = {"Authorization": f"Bearer {tokenA}"}
    client.post("/cart/add", headers=headersA, json={"product_id": p["id"], "quantity": 2})
    res1 = client.post("/orders/", headers=headersA)

    tokenB = auth_token_for(client, "b@b.com", "x")
    headersB = {"Authorization": f"Bearer {tokenB}"}
    client.post("/cart/add", headers=headersB, json={"product_id": p["id"], "quantity": 2})
    res2 = client.post("/orders/", headers=headersB)

    statuses = {res1.status_code, res2.status_code}
    assert statuses == {200, 400} or statuses == {201, 400}