from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class RemediationCreate(BaseModel):
    description: str = Field(min_length=1)


class RemediationUpdate(BaseModel):
    status: str


class RemediationOut(BaseModel):
    id: int
    finding_id: int
    description: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)