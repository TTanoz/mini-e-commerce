def test_create_product(client):
    payload = {"name": "Keyboard", "price": 100.0, "stock": 3}
    res = client.post("/products/", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["id"] > 0
    assert data["stock"] == 3
    assert data["name"] == "Keyboard"

def test_list_products_returns_created_item(client):
    client.post("/products/", json={"name": "Keyboard", "price": 100.0, "stock": 3})
    res = client.get("/products/")
    assert res.status_code == 200
    items = res.json()
    assert len(items) >= 1
    assert any(p["name"] == "Keyboard" for p in items)
