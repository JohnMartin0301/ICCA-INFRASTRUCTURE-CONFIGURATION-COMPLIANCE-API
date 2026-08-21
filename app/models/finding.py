from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index, text
from sqlalchemy.orm import relationship
from app.db.database import Base


class Finding(Base):
    __tablename__ = "findings"

    id = Column(Integer, primary_key=True, index=True)
    server_id = Column(Integer, ForeignKey("servers.id"), nullable=False)
    check_id = Column(Integer, ForeignKey("checks.id"), nullable=False)
    severity = Column(String, nullable=False)
    status = Column(String, nullable=False, default="open")
    first_detected_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_seen_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index(
            "ix_findings_open_server_check",
            "server_id",
            "check_id",
            unique=True,
            postgresql_where=text("status = 'open'"),
        ),
    )
    
    remediation = relationship("Remediation", back_populates="finding", uselist=False)