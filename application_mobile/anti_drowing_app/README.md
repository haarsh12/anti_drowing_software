# Anti Drowing - Emergency Response Mobile App

A production-level Flutter mobile app for emergency response system that syncs with FastAPI + Supabase backend and React web dashboard.

## 🚨 System Overview

This mobile app is part of a complete emergency response system:
- **ESP32** sends emergency alerts → **Backend**
- **Backend** creates cases and sends Firebase notifications
- **Flutter App** receives notifications and shows full-screen emergency UI
- **User** selects action (ACCEPT/SAVE/OUT OF REACH)
- **Backend** updates case status
- **Web Dashboard** + **Mobile App** reflect same updates

## 🛠 Tech Stack

- **Flutter** - Mobile framework
- **Firebase Core** - Firebase initialization
- **Firebase Messaging** - Push notifications (FCM)
- **Flutter Local Notifications** - Local notification handling
- **HTTP** - API communication
- **SharedPreferences** - Local storage

## 📱 Features

### 1. Registration & OTP Verification
- User registration with name and phone
- OTP verification (Demo OTP: `567788`)
- Local storage of user credentials

### 2. Home Dashboard
- Real-time case list (auto-refresh every 5 seconds)
- Case status color coding:
  - 🔴 Red → Pending
  - 🟡 Yellow → Accepted/Saved
  - ⚫ Grey → Completed/Out of Reach
- Connection status indicator
- User profile display

### 3. Full-Screen Emergency Alert
- **CRITICAL FEATURE** - Cannot be dismissed without action
- Triggered by Firebase notification with `type: "emergency"`
- Shows case ID and GPS coordinates
- Vibration and visual alerts
- Three action buttons:
  - **ACCEPT** - I'm responding
  - **SAVE** - Person rescued
  - **OUT OF REACH** - Cannot reach location

### 4. Firebase Push Notifications
- Foreground: Direct emergency screen
- Background/Terminated: Local notification → Emergency screen on tap
- Automatic FCM token registration

## 🔧 Setup Instructions

### Prerequisites
- Flutter SDK (>=3.13.0)
- Android Studio / Xcode
- Firebase project
- Backend API running

### 1. Clone and Install Dependencies
```bash
cd application_mobile/anti_drowing_app
flutter pub get
```

### 2. Firebase Configuration

#### Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create new project: "anti-drowing-app"
3. Enable Cloud Messaging

#### Android Setup
1. Add Android app to Firebase project
2. Package name: `com.example.anti_drowing_app`
3. Download `google-services.json`
4. Place in `android/app/google-services.json`

#### iOS Setup
1. Add iOS app to Firebase project
2. Bundle ID: `com.example.antiDrowingApp`
3. Download `GoogleService-Info.plist`
4. Add to `ios/Runner/GoogleService-Info.plist`

#### Update Firebase Options
Edit `lib/firebase_options.dart` with your Firebase config:
```dart
static const FirebaseOptions android = FirebaseOptions(
  apiKey: 'YOUR_ANDROID_API_KEY',
  appId: 'YOUR_ANDROID_APP_ID',
  messagingSenderId: 'YOUR_MESSAGING_SENDER_ID',
  projectId: 'YOUR_PROJECT_ID',
  storageBucket: 'YOUR_STORAGE_BUCKET',
);
```

### 3. Backend Configuration

Update `lib/services/api_service.dart`:
```dart
static const String baseUrl = 'http://YOUR_BACKEND_URL'; // Replace with actual URL
```

### 4. Build and Run

#### Android
```bash
flutter build apk --release
# or for debug
flutter run
```

#### iOS
```bash
flutter build ios --release
# or for debug
flutter run
```

## 🔗 API Integration

The app consumes these backend endpoints:

### GET /api/cases
Fetch all emergency cases
```json
{
  "cases": [
    {
      "case_number": "CASE001",
      "latitude": 40.7128,
      "longitude": -74.0060,
      "status": "pending",
      "assigned_to": "John Doe",
      "timestamp": "2024-01-01T12:00:00Z"
    }
  ]
}
```

### POST /api/case-action
Update case with user action
```json
{
  "case_id": "CASE001",
  "action": "accepted", // "accepted" | "saved" | "out_of_reach"
  "action_by": "John Doe"
}
```

### POST /api/register-device
Register device for notifications
```json
{
  "name": "John Doe",
  "phone": "+1234567890",
  "fcm_token": "firebase_token_here"
}
```

## 🔔 Firebase Notification Format

Emergency notifications must have this structure:
```json
{
  "data": {
    "type": "emergency",
    "case_id": "CASE001",
    "latitude": "40.7128",
    "longitude": "-74.0060"
  }
}
```

## 🎨 UI Theme

- **Primary Color**: Orange (#F97316)
- **Background**: White (#FFFFFF)
- **Style**: Bright, glossy UI with rounded corners and soft shadows
- **Emergency UI**: Red gradient with pulsing animations

## 📁 Project Structure

```
lib/
├── main.dart                 # App entry point
├── firebase_options.dart     # Firebase configuration
├── services/
│   ├── api_service.dart      # Backend API calls
│   └── notification_service.dart # Firebase & local notifications
├── screens/
│   ├── register_screen.dart  # User registration
│   ├── otp_screen.dart      # OTP verification
│   ├── home_screen.dart     # Dashboard with cases
│   └── emergency_screen.dart # Full-screen emergency alert
└── widgets/
    └── case_card.dart       # Case display widget
```

## 🚀 Production Deployment

### Android
1. Generate signed APK:
```bash
flutter build apk --release
```

2. Upload to Google Play Store

### iOS
1. Build for App Store:
```bash
flutter build ios --release
```

2. Archive in Xcode and upload to App Store

## 🔒 Security Notes

- All API calls use HTTPS in production
- FCM tokens are securely managed
- User data stored locally with SharedPreferences
- Emergency notifications bypass Do Not Disturb

## 🧪 Testing

### Test Emergency Flow
1. Register with any name/phone
2. Use OTP: `567788`
3. Send test notification via Firebase Console:
   - Data: `{"type": "emergency", "case_id": "TEST001", "latitude": "40.7128", "longitude": "-74.0060"}`
4. Verify full-screen emergency alert appears
5. Test all three action buttons

### Test Auto-Refresh
- Cases list updates every 5 seconds
- Connection status shows online/offline
- Pull-to-refresh works

## 📞 Support

For issues or questions:
1. Check Firebase configuration
2. Verify backend API endpoints
3. Test notification permissions
4. Check device logs for errors

## 🔄 Sync with Web Dashboard

The mobile app maintains perfect sync with the web dashboard:
- Same case data structure
- Same status color coding
- Same real-time updates
- Consistent user experience

---

**Built for production emergency response systems** 🚨