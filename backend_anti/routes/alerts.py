"""
Alert routes for the IoT dashboard API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from datetime import datetime
from database import get_db
from models import Alert, GuardResponse, User, Device
from schemas import AlertCreate, AlertResponse, AlertListResponse, SuccessResponse, GuardResponseCreate, DeviceResponse
from auth import get_current_user

router = APIRouter(prefix="/api", tags=["alerts"])

@router.post("/alert", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
async def create_alert(alert_data: AlertCreate, db: Session = Depends(get_db)):
    """Create a new alert from ESP32 device"""
    
    # 🚨 ESP32 DEBUG LOGGING - Show all incoming data
    print("\n" + "="*80)
    print("📡 ESP32 COMMUNICATION RECEIVED")
    print("="*80)
    print(f"🕐 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📱 Device ID: {alert_data.device_id}")
    print(f"🚨 Danger Status: {'🔴 EMERGENCY!' if alert_data.danger else '🟢 SAFE'}")
    print(f"📍 Latitude: {alert_data.latitude:.6f}")
    print(f"📍 Longitude: {alert_data.longitude:.6f}")
    print(f"📍 Location: {alert_data.location_name or 'Not specified'}")
    
    # Show additional fields if present - use getattr to avoid errors
    if hasattr(alert_data, 'rssi') and alert_data.rssi is not None:
        print(f"📶 RSSI: {alert_data.rssi} dBm")
    if hasattr(alert_data, 'wifi_rssi') and alert_data.wifi_rssi is not None:
        print(f"📶 WiFi RSSI: {alert_data.wifi_rssi} dBm")
    if hasattr(alert_data, 'heartbeat') and alert_data.heartbeat is not None:
        print(f"💓 Heartbeat: {alert_data.heartbeat}")
    if hasattr(alert_data, 'test') and alert_data.test is not None:
        print(f"🧪 Test Mode: {alert_data.test}")
    if hasattr(alert_data, 'uptime') and alert_data.uptime is not None:
        uptime_sec = alert_data.uptime / 1000
        print(f"⏱️  Device Uptime: {uptime_sec:.1f} seconds")
    if hasattr(alert_data, 'timestamp') and alert_data.timestamp is not None:
        print(f"🕐 Device Timestamp: {alert_data.timestamp}")
    if hasattr(alert_data, 'nrf_status') and alert_data.nrf_status is not None:
        print(f"📻 NRF Status: {alert_data.nrf_status}")
    
    # Show any extra fields that might be present
    if hasattr(alert_data, '__dict__'):
        extra_fields = {}
        for key, value in alert_data.__dict__.items():
            if key not in ['device_id', 'danger', 'latitude', 'longitude', 'location_name']:
                if value is not None:
                    extra_fields[key] = value
        if extra_fields:
            print("📊 Additional Fields:")
            for key, value in extra_fields.items():
                print(f"   {key}: {value}")
    
    print("="*80)
    
    try:
        # Verify device exists
        device = db.query(Device).filter(Device.device_id == alert_data.device_id).first()
        if not device:
            print(f"🆕 Creating new device: {alert_data.device_id}")
            # Create device if it doesn't exist
            device = Device(
                device_id=alert_data.device_id,
                device_name=f"Auto-created device {alert_data.device_id}",
                location_name=alert_data.location_name or "Unknown Location",
                latitude=alert_data.latitude,
                longitude=alert_data.longitude
            )
            db.add(device)
            db.commit()
            print(f"✅ Device created successfully")
        else:
            print(f"📱 Using existing device: {alert_data.device_id}")
        
        # Create new alert
        new_alert = Alert(
            device_id=alert_data.device_id,
            danger=alert_data.danger,
            latitude=alert_data.latitude,
            longitude=alert_data.longitude,
            location_name=alert_data.location_name or device.location_name,
            status="active" if alert_data.danger else "resolved",
            priority="critical" if alert_data.danger else "low"
        )
        
        db.add(new_alert)
        db.commit()
        db.refresh(new_alert)
        
        print(f"💾 Alert saved to database with ID: {new_alert.id}")
        
        if alert_data.danger:
            print("🚨 EMERGENCY ALERT CREATED - Mobile notifications will be triggered!")
        else:
            print("✅ Safe status recorded")
        
        print("="*80 + "\n")
        
        return SuccessResponse(
            message="Alert created successfully",
            data={
                "id": new_alert.id,
                "alert_id": new_alert.id,
                "device_id": new_alert.device_id,
                "danger": new_alert.danger,
                "latitude": new_alert.latitude,
                "longitude": new_alert.longitude,
                "timestamp": new_alert.timestamp.isoformat() if new_alert.timestamp else None
            }
        )
        
    except Exception as e:
        db.rollback()
        print(f"❌ ERROR processing ESP32 data: {str(e)}")
        print(f"❌ Error type: {type(e).__name__}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")
        print("="*80 + "\n")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create alert: {str(e)}"
        )

@router.get("/alerts", response_model=AlertListResponse)
async def get_all_alerts(db: Session = Depends(get_db)):
    """Get all alerts ordered by timestamp (newest first)"""
    try:
        alerts = db.query(Alert).order_by(desc(Alert.timestamp)).all()
        
        # Load guard responses for each alert
        alert_responses = []
        for alert in alerts:
            guard_responses = db.query(GuardResponse).filter(
                GuardResponse.alert_id == alert.id
            ).order_by(GuardResponse.timestamp).all()
            
            alert_dict = AlertResponse.model_validate(alert).model_dump()
            alert_dict['guard_responses'] = [
                {
                    **response.__dict__,
                    'user': response.user.__dict__ if response.user else None
                }
                for response in guard_responses
            ]
            alert_responses.append(AlertResponse(**alert_dict))
        
        return AlertListResponse(
            alerts=alert_responses,
            total=len(alert_responses)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch alerts: {str(e)}"
        )

@router.get("/alerts/latest", response_model=AlertResponse)
async def get_latest_alert(db: Session = Depends(get_db)):
    """Get the most recent alert"""
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

@router.post("/guard-response", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
async def create_guard_response(
    response_data: GuardResponseCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Record a guard's response to an emergency alert"""
    try:
        # Verify alert exists
        alert = db.query(Alert).filter(Alert.id == response_data.alert_id).first()
        if not alert:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alert not found"
            )
        
        # Check if user already responded to this alert
        existing_response = db.query(GuardResponse).filter(
            GuardResponse.alert_id == response_data.alert_id,
            GuardResponse.user_id == current_user.id
        ).first()
        
        if existing_response:
            # Update existing response
            existing_response.action = response_data.action
            existing_response.notes = response_data.notes
            existing_response.timestamp = datetime.utcnow()
        else:
            # Create new response
            # Calculate response time
            response_time = (datetime.utcnow() - alert.timestamp).total_seconds()
            
            new_response = GuardResponse(
                alert_id=response_data.alert_id,
                user_id=current_user.id,
                action=response_data.action,
                notes=response_data.notes,
                response_time=response_time
            )
            db.add(new_response)
        
        # Update alert status if completed
        if response_data.action == "completed":
            alert.status = "resolved"
            alert.resolved_at = datetime.utcnow()
        
        db.commit()
        
        return SuccessResponse(
            message=f"Guard response recorded: {response_data.action} by {current_user.name}"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to record guard response: {str(e)}"
        )

@router.delete("/alerts/clear-all", response_model=SuccessResponse)
async def clear_all_alerts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Clear all alerts from the database (admin only)"""
    try:
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can clear all alerts"
            )
        
        # Count alerts before deletion
        deleted_count = db.query(Alert).count()
        
        # Delete all guard responses first (foreign key constraint)
        db.query(GuardResponse).delete()
        
        # Delete all alerts
        db.query(Alert).delete()
        db.commit()
        
        return SuccessResponse(
            message=f"All alerts cleared successfully. Deleted {deleted_count} alerts."
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear alerts: {str(e)}"
        )

@router.get("/devices", response_model=List[DeviceResponse])
async def get_all_devices(db: Session = Depends(get_db)):
    """Get all registered devices"""
    try:
        devices = db.query(Device).filter(Device.is_active == True).all()
        return [DeviceResponse.model_validate(device) for device in devices]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch devices: {str(e)}"
        )

@router.get("/alerts/{device_id}", response_model=AlertListResponse)
async def get_alerts_by_device(device_id: str, db: Session = Depends(get_db)):
    """Get all alerts for a specific device"""
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