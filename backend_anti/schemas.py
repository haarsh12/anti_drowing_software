"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

# User schemas
class UserCreate(BaseModel):
    """Schema for creating a new user"""
    name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., min_length=10, max_length=20)
    password: str = Field(..., min_length=6)
    role: str = Field(default="guard")

class UserLogin(BaseModel):
    """Schema for user login"""
    phone: str
    password: str

class UserResponse(BaseModel):
    """Schema for user response"""
    id: int
    name: str
    phone: str
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token: str
    token_type: str
    user: UserResponse

# Alert schemas
class AlertCreate(BaseModel):
    """Schema for creating a new alert (from ESP32)"""
    device_id: str = Field(..., description="Unique identifier for the IoT device")
    danger: bool = Field(..., description="Whether this is a danger alert")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate")
    location_name: Optional[str] = Field(None, description="Human readable location name")
    
    # Additional ESP32 fields for debugging and monitoring
    rssi: Optional[int] = Field(None, description="LoRa/NRF signal strength (dBm)")
    wifi_rssi: Optional[int] = Field(None, description="WiFi signal strength (dBm)")
    heartbeat: Optional[bool] = Field(None, description="Whether this is a heartbeat message")
    test: Optional[bool] = Field(None, description="Whether this is a test message")
    uptime: Optional[int] = Field(None, description="Device uptime in milliseconds")
    timestamp: Optional[int] = Field(None, description="Device timestamp in milliseconds")
    nrf_status: Optional[str] = Field(None, description="NRF24L01 module status")
    battery_level: Optional[int] = Field(None, description="Battery level percentage")
    temperature: Optional[float] = Field(None, description="Device temperature in Celsius")
    humidity: Optional[float] = Field(None, description="Environmental humidity percentage")
    
    class Config:
        # Allow extra fields that might be sent by ESP32
        extra = "allow"

class GuardResponseCreate(BaseModel):
    """Schema for creating a guard response"""
    alert_id: int = Field(..., description="Alert ID")
    action: str = Field(..., description="Action taken by guard")
    notes: Optional[str] = Field(None, description="Additional notes")

class GuardResponseResponse(BaseModel):
    """Schema for guard response"""
    id: int
    alert_id: int
    action: str
    notes: Optional[str]
    response_time: Optional[float]
    timestamp: datetime
    user: UserResponse
    
    class Config:
        from_attributes = True

class AlertResponse(BaseModel):
    """Schema for alert response"""
    id: int
    device_id: str
    danger: bool
    latitude: float
    longitude: float
    location_name: Optional[str]
    status: str
    priority: str
    timestamp: datetime
    resolved_at: Optional[datetime]
    guard_responses: List[GuardResponseResponse] = []
    
    class Config:
        from_attributes = True

class AlertListResponse(BaseModel):
    """Schema for list of alerts response"""
    alerts: List[AlertResponse]
    total: int

class DeviceResponse(BaseModel):
    """Schema for device response"""
    id: int
    device_id: str
    device_name: str
    location_name: str
    latitude: float
    longitude: float
    is_active: bool
    last_heartbeat: Optional[datetime]
    battery_level: Optional[int]
    signal_strength: Optional[int]
    
    class Config:
        from_attributes = True

class SuccessResponse(BaseModel):
    """Schema for success response"""
    message: str
    data: Optional[dict] = None