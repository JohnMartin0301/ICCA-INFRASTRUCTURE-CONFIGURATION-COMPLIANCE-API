from pydantic import BaseModel, ConfigDict
from typing import Optional


class CheckBase(BaseModel):
    name: str
    description: Optional[str] = None
    expected_value: str
    severity: str


class CheckCreate(CheckBase):
    pass


class CheckOut(CheckBase):
    id: int

    model_config = ConfigDict(from_attributes=True)