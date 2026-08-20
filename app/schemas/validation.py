from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ValidationResultIn(BaseModel):
    check_id: int
    actual_value: str


class ValidationRunCreate(BaseModel):
    results: list[ValidationResultIn]


class ValidationResultOut(BaseModel):
    id: int
    check_id: int
    expected_value: str
    actual_value: str
    passed: bool

    model_config = ConfigDict(from_attributes=True)


class ValidationRunOut(BaseModel):
    id: int
    server_id: int
    submitted_by: Optional[int] = None
    run_at: datetime
    results: list[ValidationResultOut]

    model_config = ConfigDict(from_attributes=True)