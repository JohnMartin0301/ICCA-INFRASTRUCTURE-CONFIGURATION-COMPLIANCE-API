from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class ValidationResult(Base):
    __tablename__ = "validation_results"

    id = Column(Integer, primary_key=True, index=True)
    validation_run_id = Column(Integer, ForeignKey("validation_runs.id"), nullable=False)
    check_id = Column(Integer, ForeignKey("checks.id"), nullable=False)
    expected_value = Column(String, nullable=False)
    actual_value = Column(String, nullable=False)
    passed = Column(Boolean, nullable=False)

    validation_run = relationship("ValidationRun", back_populates="results")
    check = relationship("Check", back_populates="validation_results")