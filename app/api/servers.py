from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.database import get_db
from app.models.server import Server
from app.schemas.server import ServerCreate, ServerUpdate, ServerOut
from app.core.security import get_current_user, require_role

router = APIRouter(prefix="/servers", tags=["servers"])


@router.post("", response_model=ServerOut, status_code=status.HTTP_201_CREATED)
def create_server(server: ServerCreate, db: Session = Depends(get_db), _=Depends(require_role("admin"))):
    new_server = Server(**server.model_dump())
    db.add(new_server)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A server with this hostname already exists",
        )
    db.refresh(new_server)
    return new_server


@router.get("", response_model=list[ServerOut])
def list_servers(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    offset = (page - 1) * page_size
    return db.query(Server).offset(offset).limit(page_size).all()


@router.get("/{server_id}", response_model=ServerOut)
def get_server(server_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    server = db.get(Server, server_id)
    if not server:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Server not found")
    return server


@router.patch("/{server_id}", response_model=ServerOut)
def update_server(server_id: int, updates: ServerUpdate, db: Session = Depends(get_db), _=Depends(require_role("admin"))):
    server = db.get(Server, server_id)
    if not server:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Server not found")

    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(server, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A server with this hostname already exists",
        )
    db.refresh(server)
    return server


@router.delete("/{server_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_server(server_id: int, db: Session = Depends(get_db), _=Depends(require_role("admin"))):
    server = db.get(Server, server_id)
    if not server:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Server not found")
    db.delete(server)
    db.commit()