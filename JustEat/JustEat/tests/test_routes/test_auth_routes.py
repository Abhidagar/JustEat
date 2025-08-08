def test_login_customer_success(client, customer_a):
    response = client.post(
        "/login",
        data={"email": "test@example.com", "password": "password"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"alert-success" in response.data
    assert response.request.path == "/home"


def test_login_owner_success(client, owner_a):
    response = client.post(
        "/login",
        data={"email": "owner_1@example.com", "password": "password"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"alert-success" in response.data
    assert response.request.path == "/restaurants/dashboard"


def test_login_customer_failure(client, customer_a):
    response = client.post(
        "/login",
        data={"email": "test@example.com", "password": "wrongpassword"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"alert-danger" in response.data
    assert b"Invalid credentials" in response.data


def test_unauthenticated_access(client):
    response = client.get("/restaurants/dashboard", follow_redirects=True)
    assert response.status_code == 200
    assert b"alert-danger" in response.data
    assert b"Please login to access this page" in response.data


def test_customer_role(client, login_user, customer_a):
    login_user(customer_a)

    # Test that a customer cannot access the restaurant dashboard
    response = client.get("/restaurants/dashboard", follow_redirects=True)
    assert response.status_code == 200
    assert b"alert-danger" in response.data
    assert b"Access restricted to restaurant owners" in response.data
    assert response.request.path == "/home"

    # Test that a customer can access their own profile page
    response = client.get("/profile", follow_redirects=True)
    assert response.status_code == 200
    assert b"Profile" in response.data


def test_owner_role(client, login_user, owner_a):
    login_user(owner_a)

    # Test that an owner can access the restaurant dashboard
    response = client.get("/restaurants/dashboard", follow_redirects=True)
    assert response.status_code == 200
    assert b"My Restaurants" in response.data
    assert response.request.path == "/restaurants/dashboard"

    # Test that an owner can access their own profile page
    response = client.get("/profile", follow_redirects=True)
    assert response.status_code == 200
    assert b"Profile" in response.data

    # Test that an owner cannot access the customer routes - they get redirected to their dashboard
    response = client.get("/home", follow_redirects=True)
    assert response.status_code == 200
    assert b"alert-danger" in response.data
    assert b"This section is only available for customers" in response.data
    assert response.request.path == "/restaurants/dashboard"


def test_logout(client, login_user, customer_a):
    login_user(customer_a)
    response = client.post("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/login"
