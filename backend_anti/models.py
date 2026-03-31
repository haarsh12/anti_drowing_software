"""
Database models for the IoT alert system
"""
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.sql import func
from database import Base

class Alert(Base):
    """
    Alert model to store IoT device alerts
    """
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True, nullable=False)
    danger = Column(Boolean, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Alert(id={self.id}, device_id='{self.device_id}', danger={self.danger})>"