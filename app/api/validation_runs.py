from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.validation import ValidationRunCreate, ValidationRunOut
from app.services.validation_service import submit_validation_run

router = APIRouter(prefix="/servers", tags=["validation-runs"])


@router.post("/{server_id}/validation-runs", response_model=ValidationRunOut, status_code=status.HTTP_201_CREATED)
def create_validation_run(server_id: int, run_data: ValidationRunCreate, db: Session = Depends(get_db)):
    return submit_validation_run(server_id, run_data, db)