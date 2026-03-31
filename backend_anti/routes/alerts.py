"""
Alert routes for the IoT dashboard API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from database import get_db
from models import Alert
from schemas import AlertCreate, AlertResponse, AlertListResponse, SuccessResponse

router = APIRouter(prefix="/api", tags=["alerts"])

@router.post("/alert", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
async def create_alert(alert_data: AlertCreate, db: Session = Depends(get_db)):
    """
    Create a new alert from ESP32 device
    """
    try:
        # Create new alert instance
        new_alert = Alert(
            device_id=alert_data.device_id,
            danger=alert_data.danger,
            latitude=alert_data.latitude,
            longitude=alert_data.longitude
        )
        
        # Add to database
        db.add(new_alert)
        db.commit()
        db.refresh(new_alert)
        
        return SuccessResponse(
            message="Alert created successfully",
            alert_id=new_alert.id
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create alert: {str(e)}"
        )

@router.get("/alerts", response_model=AlertListResponse)
async def get_all_alerts(db: Session = Depends(get_db)):
    """
    Get all alerts ordered by timestamp (newest first)
    """
    try:
        alerts = db.query(Alert).order_by(desc(Alert.timestamp)).all()
        
        return AlertListResponse(
            alerts=[AlertResponse.model_validate(alert) for alert in alerts],
            total=len(alerts)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch alerts: {str(e)}"
        )

@router.get("/alerts/latest", response_model=AlertResponse)
async def get_latest_alert(db: Session = Depends(get_db)):
    """
    Get the most recent alert
    """
    try:
        latest_alert = db.query(Alert).order_by(desc(Alert.timestamp)).first()
        
        if not latest_alert:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No alerts found"
            )
        
        return AlertResponse.model_validate(latest_alert)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch latest alert: {str(e)}"
        )

@router.get("/alerts/{device_id}", response_model=AlertListResponse)
async def get_alerts_by_device(device_id: str, db: Session = Depends(get_db)):
    """
    Get all alerts for a specific device
    """
    try:
        alerts = db.query(Alert).filter(
            Alert.device_id == device_id
        ).order_by(desc(Alert.timestamp)).all()
        
        return AlertListResponse(
            alerts=[AlertResponse.model_validate(alert) for alert in alerts],
            total=len(alerts)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch alerts for device {device_id}: {str(e)}"
        )