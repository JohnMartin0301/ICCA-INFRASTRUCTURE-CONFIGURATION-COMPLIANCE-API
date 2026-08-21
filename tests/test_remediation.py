import pytest
from fastapi import HTTPException

from app.models.server import Server
from app.models.check import Check
from app.models.finding import Finding
from app.schemas.remediation import RemediationCreate, RemediationUpdate
from app.services.remediation_service import create_remediation, update_remediation


def _make_finding(db_session) -> Finding:
    server = Server(hostname="test-server", operating_system="Ubuntu 24.04", environment="test")
    check = Check(name="Firewall enabled", expected_value="true", severity="high")
    db_session.add_all([server, check])
    db_session.commit()

    finding = Finding(server_id=server.id, check_id=check.id, severity=check.severity, status="open")
    db_session.add(finding)
    db_session.commit()
    return finding


def test_create_remediation_succeeds(db_session):
    finding = _make_finding(db_session)
    remediation = create_remediation(db_session, finding.id, RemediationCreate(description="Enable firewall"))
    assert remediation.status == "open"
    assert remediation.finding_id == finding.id


def test_cannot_create_duplicate_remediation(db_session):
    finding = _make_finding(db_session)
    create_remediation(db_session, finding.id, RemediationCreate(description="Enable firewall"))

    with pytest.raises(HTTPException) as exc_info:
        create_remediation(db_session, finding.id, RemediationCreate(description="Second attempt"))
    assert exc_info.value.status_code == 400


def test_valid_transition_open_to_in_progress(db_session):
    finding = _make_finding(db_session)
    remediation = create_remediation(db_session, finding.id, RemediationCreate(description="Enable firewall"))

    updated = update_remediation(db_session, remediation.id, RemediationUpdate(status="in_progress"))
    assert updated.status == "in_progress"


def test_invalid_transition_resolved_to_open_rejected(db_session):
    finding = _make_finding(db_session)
    remediation = create_remediation(db_session, finding.id, RemediationCreate(description="Enable firewall"))
    update_remediation(db_session, remediation.id, RemediationUpdate(status="in_progress"))
    update_remediation(db_session, remediation.id, RemediationUpdate(status="resolved"))

    with pytest.raises(HTTPException) as exc_info:
        update_remediation(db_session, remediation.id, RemediationUpdate(status="open"))
    assert exc_info.value.status_code == 400