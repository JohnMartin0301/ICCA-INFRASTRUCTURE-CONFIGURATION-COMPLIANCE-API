def test_full_reconciliation_workflow(client, make_user):
    admin_headers = make_user("admin3", "password123", "admin")
    engineer_headers = make_user("engineer2", "password123", "engineer")

    server_id = client.post(
        "/servers",
        json={"hostname": "workflow-server", "operating_system": "Ubuntu 24.04", "environment": "test"},
        headers=admin_headers,
    ).json()["id"]
    check_id = client.post(
        "/checks",
        json={"name": "Firewall enabled", "expected_value": "true", "severity": "high"},
        headers=admin_headers,
    ).json()["id"]

    # First failure — opens a finding
    run1 = client.post(
        f"/servers/{server_id}/validation-runs",
        json={"results": [{"check_id": check_id, "actual_value": "false"}]},
        headers=engineer_headers,
    )
    assert run1.status_code == 201

    open_findings = client.get("/findings?status=open", headers=engineer_headers).json()
    matching = [f for f in open_findings if f["server_id"] == server_id and f["check_id"] == check_id]
    assert len(matching) == 1
    finding_id = matching[0]["id"]
    first_last_seen = matching[0]["last_seen_at"]

    # Second failure — updates the same finding, does not duplicate it
    run2 = client.post(
        f"/servers/{server_id}/validation-runs",
        json={"results": [{"check_id": check_id, "actual_value": "false"}]},
        headers=engineer_headers,
    )
    assert run2.status_code == 201

    open_findings_again = client.get("/findings?status=open", headers=engineer_headers).json()
    matching_again = [f for f in open_findings_again if f["server_id"] == server_id and f["check_id"] == check_id]
    assert len(matching_again) == 1
    assert matching_again[0]["id"] == finding_id
    assert matching_again[0]["last_seen_at"] != first_last_seen

    # Passing result — resolves the finding
    run3 = client.post(
        f"/servers/{server_id}/validation-runs",
        json={"results": [{"check_id": check_id, "actual_value": "true"}]},
        headers=engineer_headers,
    )
    assert run3.status_code == 201

    resolved = client.get(f"/findings/{finding_id}", headers=engineer_headers).json()
    assert resolved["status"] == "resolved"
    assert resolved["resolved_at"] is not None