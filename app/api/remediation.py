from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.security import require_role
from app.schemas.remediation import RemediationCreate, RemediationUpdate, RemediationOut
from app.services.remediation_service import create_remediation, update_remediation

router = APIRouter(tags=["remediation"])


@router.post("/findings/{finding_id}/remediation", response_model=RemediationOut, status_code=status.HTTP_201_CREATED)
def create_finding_remediation(
    finding_id: int,
    data: RemediationCreate,
    db: Session = Depends(get_db),
    _=Depends(require_role("engineer", "admin")),
):
    return create_remediation(db, finding_id, data)


@router.patch("/remediation/{remediation_id}", response_model=RemediationOut)
def update_finding_remediation(
    remediation_id: int,
    data: RemediationUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_role("engineer", "admin")),
):
    return update_remediation(db, remediation_id, data)