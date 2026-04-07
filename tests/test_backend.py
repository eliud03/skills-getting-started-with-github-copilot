def test_get_activities_returns_activity_map(client):
    # Arrange
    endpoint = "/activities"

    # Act
    response = client.get(endpoint)
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert "Chess Club" in payload


def test_signup_success_for_new_student(client):
    # Arrange
    activity_name = "Chess Club"
    email = "aaa-signup-success@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(endpoint, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Signed up {email} for {activity_name}"


def test_signup_rejects_duplicate_student(client):
    # Arrange
    activity_name = "Programming Class"
    email = "aaa-signup-duplicate@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup"
    client.post(endpoint, params={"email": email})

    # Act
    response = client.post(endpoint, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Student already signed up for this activity"


def test_signup_rejects_unknown_activity(client):
    # Arrange
    endpoint = "/activities/Unknown Activity/signup"
    email = "aaa-signup-not-found@mergington.edu"

    # Act
    response = client.post(endpoint, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_unregister_success_for_existing_student(client):
    # Arrange
    activity_name = "Gym Class"
    email = "aaa-unregister-success@mergington.edu"
    signup_endpoint = f"/activities/{activity_name}/signup"
    client.post(signup_endpoint, params={"email": email})

    # Act
    response = client.delete(signup_endpoint, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Unregistered {email} from {activity_name}"


def test_unregister_rejects_missing_student(client):
    # Arrange
    endpoint = "/activities/Drama Club/signup"
    email = "aaa-unregister-missing@mergington.edu"

    # Act
    response = client.delete(endpoint, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Student is not signed up for this activity"


def test_unregister_rejects_unknown_activity(client):
    # Arrange
    endpoint = "/activities/Unknown Activity/signup"
    email = "aaa-unregister-activity-not-found@mergington.edu"

    # Act
    response = client.delete(endpoint, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_root_redirects_to_static_index(client):
    # Arrange
    endpoint = "/"

    # Act
    response = client.get(endpoint, follow_redirects=False)

    # Assert
    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/static/index.html"