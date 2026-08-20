from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.database import get_db
from app.models.check import Check
from app.schemas.check import CheckCreate, CheckOut
from app.core.security import get_current_user, require_role

router = APIRouter(prefix="/checks", tags=["checks"])


@router.post("", response_model=CheckOut, status_code=status.HTTP_201_CREATED)
def create_check(check: CheckCreate, db: Session = Depends(get_db), _=Depends(require_role("admin"))):
    new_check = Check(**check.model_dump())
    db.add(new_check)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A check with this name already exists",
        )
    db.refresh(new_check)
    return new_check


@router.get("", response_model=list[CheckOut])
def list_checks(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Check).all()


@router.get("/{check_id}", response_model=CheckOut)
def get_check(check_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    check = db.get(Check, check_id)
    if not check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Check not found")
    return check