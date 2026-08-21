from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models.finding import Finding
from app.models.remediation import Remediation
from app.schemas.remediation import RemediationCreate, RemediationUpdate

ALLOWED_TRANSITIONS = {
    "open": {"in_progress", "resolved"},
    "in_progress": {"resolved"},
    "resolved": set(),
}


def create_remediation(db: Session, finding_id: int, data: RemediationCreate) -> Remediation:
    finding = db.get(Finding, finding_id)
    if not finding:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Finding not found")

    new_remediation = Remediation(finding_id=finding_id, description=data.description, status="open")
    db.add(new_remediation)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This finding already has a remediation record",
        )
    db.refresh(new_remediation)
    return new_remediation


def update_remediation(db: Session, remediation_id: int, data: RemediationUpdate) -> Remediation:
    remediation = db.get(Remediation, remediation_id)
    if not remediation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Remediation not found")

    allowed_next = ALLOWED_TRANSITIONS.get(remediation.status, set())
    if data.status not in allowed_next:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot change status from '{remediation.status}' to '{data.status}'",
        )

    remediation.status = data.status
    db.commit()
    db.refresh(remediation)
    return remediation