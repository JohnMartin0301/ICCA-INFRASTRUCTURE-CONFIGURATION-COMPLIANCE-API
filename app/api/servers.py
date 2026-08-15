from fastapi import APIRouter, HTTPException, status
from app.schemas.server import ServerCreate, ServerUpdate, ServerOut

router = APIRouter(prefix="/servers", tags=["servers"])

# Temporary in-memory storage
servers_db: dict[int, dict] = {}
next_id = 1


@router.post("", response_model=ServerOut, status_code=status.HTTP_201_CREATED)
def create_server(server: ServerCreate):
    global next_id
    for existing in servers_db.values():
        if existing["hostname"] == server.hostname:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A server with this hostname already exists",
            )
    new_server = server.model_dump()
    new_server["id"] = next_id
    servers_db[next_id] = new_server
    next_id += 1
    return new_server


@router.get("", response_model=list[ServerOut])
def list_servers():
    return list(servers_db.values())


@router.get("/{server_id}", response_model=ServerOut)
def get_server(server_id: int):
    server = servers_db.get(server_id)
    if not server:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Server not found")
    return server


@router.patch("/{server_id}", response_model=ServerOut)
def update_server(server_id: int, updates: ServerUpdate):
    server = servers_db.get(server_id)
    if not server:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Server not found")
    update_data = updates.model_dump(exclude_unset=True)
    server.update(update_data)
    return server


@router.delete("/{server_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_server(server_id: int):
    if server_id not in servers_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Server not found")
    del servers_db[server_id]