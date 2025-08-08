def test_menu_items_route(client, login_user, owner_a, restaurant_a, menu_a):
    login_user(owner_a)
    response = client.get(
        f"/restaurants/{restaurant_a.slug}/menu", follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Menu" in response.data
    assert b"Pizza" in response.data
    assert b"Burger" in response.data
    assert response.request.path == f"/restaurants/{restaurant_a.slug}/menu"
