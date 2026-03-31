"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class AlertCreate(BaseModel):
    """
    Schema for creating a new alert (from ESP32)
    """
    device_id: str = Field(..., description="Unique identifier for the IoT device")
    danger: bool = Field(..., description="Whether this is a danger alert")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate")

class AlertResponse(BaseModel):
    """
    Schema for alert response
    """
    id: int
    device_id: str
    danger: bool
    latitude: float
    longitude: float
    timestamp: datetime
    
    class Config:
        from_attributes = True

class AlertListResponse(BaseModel):
    """
    Schema for list of alerts response
    """
    alerts: List[AlertResponse]
    total: int

class SuccessResponse(BaseModel):
    """
    Schema for success response
    """
    message: str
    alert_id: int