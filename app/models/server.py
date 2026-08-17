from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base


class Server(Base):
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String, unique=True, index=True, nullable=False)
    operating_system = Column(String, nullable=False)
    environment = Column(String, nullable=False)
    status = Column(String, nullable=False, default="active")
    
    validation_runs = relationship("ValidationRun", back_populates="server")