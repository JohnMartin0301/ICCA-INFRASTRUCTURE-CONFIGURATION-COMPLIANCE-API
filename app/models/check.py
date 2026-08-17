from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base


class Check(Base):
    __tablename__ = "checks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    expected_value = Column(String, nullable=False)
    severity = Column(String, nullable=False)

    validation_results = relationship("ValidationResult", back_populates="check")