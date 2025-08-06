def test_restaurant_not_found(client, login_user, owner_a):
    login_user(owner_a)
    response = client.get("/restaurants/unknown-restaurant-90", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/restaurants/dashboard"
    assert b"Restaurant not found" in response.data


def test_cannot_access_others_restaurant(
    client, login_user, owner_a, owner_b, restaurant_a
):
    login_user(owner_b)
    response = client.get(f"/restaurants/{restaurant_a.slug}", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/restaurants/dashboard"
    assert b"Restaurant not found" in response.data


def test_add_restaurant_success(client, login_user, owner_a):
    login_user(owner_a)
    response = client.post(
        "/restaurants/new",
        data={
            "name": "New Restaurant",
            "location": "New City",
            "opening_time": "10:00",
            "closing_time": "22:00",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Restaurant created successfully" in response.data
    assert response.request.path == "/restaurants/new-restaurant-1/cuisines"


def test_update_restaurant_details(client, login_user, owner_a, restaurant_a):
    login_user(owner_a)
    response = client.post(
        f"/restaurants/{restaurant_a.slug}/settings",
        data={
            "name": "Updated Restaurant",
            "location": "Updated City",
            "opening_time": "11:00",
            "closing_time": "23:00",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Restaurant details updated successfully" in response.data
    # assert response.request.path == f"/restaurants/{restaurant_a.slug}/cuisines"
