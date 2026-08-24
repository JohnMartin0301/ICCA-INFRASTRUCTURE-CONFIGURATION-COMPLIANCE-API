def test_viewer_cannot_create_server(client, make_user):
    headers = make_user("viewer1", "password123", "viewer")
    response = client.post(
        "/servers",
        json={"hostname": "blocked-server", "operating_system": "Ubuntu 24.04", "environment": "test"},
        headers=headers,
    )
    assert response.status_code == 403


def test_admin_can_create_server(client, make_user):
    headers = make_user("admin1", "password123", "admin")
    response = client.post(
        "/servers",
        json={"hostname": "allowed-server", "operating_system": "Ubuntu 24.04", "environment": "test"},
        headers=headers,
    )
    assert response.status_code == 201


def test_viewer_can_read_servers(client, make_user):
    headers = make_user("viewer2", "password123", "viewer")
    response = client.get("/servers", headers=headers)
    assert response.status_code == 200


def test_engineer_can_submit_validation_run(client, make_user):
    admin_headers = make_user("admin2", "password123", "admin")
    engineer_headers = make_user("engineer1", "password123", "engineer")

    server_id = client.post(
        "/servers",
        json={"hostname": "engineer-test-server", "operating_system": "Ubuntu 24.04", "environment": "test"},
        headers=admin_headers,
    ).json()["id"]
    check_id = client.post(
        "/checks",
        json={"name": "SSH enabled", "expected_value": "true", "severity": "medium"},
        headers=admin_headers,
    ).json()["id"]

    response = client.post(
        f"/servers/{server_id}/validation-runs",
        json={"results": [{"check_id": check_id, "actual_value": "true"}]},
        headers=engineer_headers,
    )
    assert response.status_code == 201