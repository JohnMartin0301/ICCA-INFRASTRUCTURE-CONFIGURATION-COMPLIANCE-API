from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.schemas.remediation import RemediationOut


class FindingOut(BaseModel):
    id: int
    server_id: int
    check_id: int
    severity: str
    status: str
    first_detected_at: datetime
    last_seen_at: datetime
    resolved_at: Optional[datetime] = None
    remediation: Optional[RemediationOut] = None

    model_config = ConfigDict(from_attributes=True)