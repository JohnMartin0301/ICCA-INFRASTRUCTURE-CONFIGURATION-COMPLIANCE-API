from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class ValidationRun(Base):
    __tablename__ = "validation_runs"

    id = Column(Integer, primary_key=True, index=True)
    server_id = Column(Integer, ForeignKey("servers.id"), nullable=False)
    run_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    server = relationship("Server", back_populates="validation_runs")
    results = relationship("ValidationResult", back_populates="validation_run")