from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models.server import Server
from app.models.check import Check
from app.models.validation_run import ValidationRun
from app.models.validation_result import ValidationResult
from app.schemas.validation import ValidationRunCreate
from app.services.finding_service import reconcile_finding


def submit_validation_run(server_id: int, run_data: ValidationRunCreate, db: Session, submitted_by: int) -> ValidationRun:
    server = db.get(Server, server_id)
    if not server:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Server not found")

    validation_run = ValidationRun(server_id=server_id, submitted_by=submitted_by)
    db.add(validation_run)
    db.flush()

    for result_in in run_data.results:
        check = db.get(Check, result_in.check_id)
        if not check:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Check with id {result_in.check_id} not found",
            )

        passed = result_in.actual_value.strip().lower() == check.expected_value.strip().lower()

        reconcile_finding(db, server_id, check.id, check.severity, passed)

        validation_result = ValidationResult(
            validation_run_id=validation_run.id,
            check_id=check.id,
            expected_value=check.expected_value,
            actual_value=result_in.actual_value,
            passed=passed,
        )
        db.add(validation_result)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A conflicting update occurred while recording this validation run. Please try again.",
        )
    db.refresh(validation_run)
    return validation_run