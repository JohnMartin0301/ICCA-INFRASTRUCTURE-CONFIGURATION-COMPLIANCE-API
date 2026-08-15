from pydantic import BaseModel
from typing import Optional


class ServerBase(BaseModel):
    hostname: str
    operating_system: str
    environment: str
    status: str = "active"


class ServerCreate(ServerBase):
    pass


class ServerUpdate(BaseModel):
    hostname: Optional[str] = None
    operating_system: Optional[str] = None
    environment: Optional[str] = None
    status: Optional[str] = None


class ServerOut(ServerBase):
    id: int