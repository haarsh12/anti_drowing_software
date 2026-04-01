# 🚀 Quick Start Guide - Anti Drowing App

## ⚡ 5-Minute Setup

### 1. Install Dependencies
```bash
cd application_mobile/anti_drowing_app
flutter pub get
```

### 2. Configure Backend URL
Edit `lib/services/api_service.dart`:
```dart
static const String baseUrl = 'http://YOUR_BACKEND_URL'; // Replace with your backend
```

### 3. Firebase Setup (Essential)
1. Create Firebase project: [Firebase Console](https://console.firebase.google.com/)
2. Add Android app with package: `com.example.anti_drowing_app`
3. Download `google-services.json` → place in `android/app/`
4. Update `lib/firebase_options.dart` with your Firebase config

### 4. Run the App
```bash
flutter run
```

## 🧪 Test the Emergency Flow

### 1. Register User
- Open app → Enter name and phone
- Use OTP: `567788`

### 2. Test Emergency Notification
Send via Firebase Console → Cloud Messaging:
```json
{
  "data": {
    "type": "emergency",
    "case_id": "TEST001",
    "latitude": "40.7128",
    "longitude": "-74.0060"
  }
}
```

### 3. Expected Result
- Full-screen emergency alert appears
- Shows case ID and coordinates
- Three action buttons work

## 📱 Key Features Working

✅ **Registration & OTP** - Demo OTP: 567788  
✅ **Home Dashboard** - Auto-refresh every 5s  
✅ **Emergency Alert** - Full-screen, cannot dismiss  
✅ **Firebase Notifications** - Foreground & background  
✅ **API Integration** - Sync with backend  

## 🔧 Production Setup

For full production deployment, see:
- `README.md` - Complete setup guide
- `FIREBASE_SETUP.md` - Detailed Firebase configuration

## 🚨 Emergency System Flow

```
ESP32 Alert → Backend → Firebase → Mobile App → Full-Screen Alert → User Action → Backend Update
```

## 📞 Quick Troubleshooting

**App won't build?**
```bash
flutter clean
flutter pub get
flutter run
```

**No notifications?**
- Check Firebase configuration
- Verify notification permissions
- Test with Firebase Console first

**API errors?**
- Update backend URL in `api_service.dart`
- Check backend is running
- Verify API endpoints match

---

**Your emergency response app is ready!** 🚨