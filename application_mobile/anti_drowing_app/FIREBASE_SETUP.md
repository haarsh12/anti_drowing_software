# Firebase Setup Guide for Anti Drowing App

## 🔥 Firebase Project Setup

### 1. Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a project"
3. Project name: `anti-drowing-emergency`
4. Enable Google Analytics (optional)
5. Click "Create project"

### 2. Enable Cloud Messaging
1. In Firebase Console, go to **Project Settings** (gear icon)
2. Go to **Cloud Messaging** tab
3. Note down the **Server Key** (needed for backend)

## 📱 Android Configuration

### 1. Add Android App
1. In Firebase Console, click "Add app" → Android
2. **Package name**: `com.example.anti_drowing_app`
3. **App nickname**: `Anti Drowing Android`
4. **Debug signing certificate SHA-1**: (optional for now)
5. Click "Register app"

### 2. Download Configuration File
1. Download `google-services.json`
2. Place it in: `android/app/google-services.json`

### 3. Update Android Build Files

#### android/build.gradle
Add to dependencies:
```gradle
dependencies {
    classpath 'com.google.gms:google-services:4.3.15'
}
```

#### android/app/build.gradle
Add at the top:
```gradle
apply plugin: 'com.google.gms.google-services'
```

Add to dependencies:
```gradle
dependencies {
    implementation 'com.google.firebase:firebase-messaging:23.2.1'
}
```

## 🍎 iOS Configuration

### 1. Add iOS App
1. In Firebase Console, click "Add app" → iOS
2. **Bundle ID**: `com.example.antiDrowingApp`
3. **App nickname**: `Anti Drowing iOS`
4. Click "Register app"

### 2. Download Configuration File
1. Download `GoogleService-Info.plist`
2. Add to Xcode project: `ios/Runner/GoogleService-Info.plist`

### 3. Update iOS Configuration

#### ios/Runner/Info.plist
Add before `</dict>`:
```xml
<key>FirebaseAppDelegateProxyEnabled</key>
<false/>
```

## 🔧 Flutter Configuration

### 1. Update firebase_options.dart
Replace the placeholder values in `lib/firebase_options.dart`:

```dart
class DefaultFirebaseOptions {
  static FirebaseOptions get currentPlatform {
    switch (defaultTargetPlatform) {
      case TargetPlatform.android:
        return android;
      case TargetPlatform.iOS:
        return ios;
      default:
        throw UnsupportedError('Platform not supported');
    }
  }

  static const FirebaseOptions android = FirebaseOptions(
    apiKey: 'YOUR_ANDROID_API_KEY',           // From google-services.json
    appId: 'YOUR_ANDROID_APP_ID',             // From google-services.json
    messagingSenderId: 'YOUR_MESSAGING_SENDER_ID', // From Firebase Console
    projectId: 'anti-drowing-emergency',      // Your project ID
    storageBucket: 'anti-drowing-emergency.appspot.com',
  );

  static const FirebaseOptions ios = FirebaseOptions(
    apiKey: 'YOUR_IOS_API_KEY',               // From GoogleService-Info.plist
    appId: 'YOUR_IOS_APP_ID',                 // From GoogleService-Info.plist
    messagingSenderId: 'YOUR_MESSAGING_SENDER_ID', // Same as Android
    projectId: 'anti-drowing-emergency',      // Your project ID
    storageBucket: 'anti-drowing-emergency.appspot.com',
    iosBundleId: 'com.example.antiDrowingApp',
  );
}
```

### 2. Find Your Configuration Values

#### From google-services.json (Android):
```json
{
  "project_info": {
    "project_id": "anti-drowing-emergency",
    "storage_bucket": "anti-drowing-emergency.appspot.com"
  },
  "client": [
    {
      "client_info": {
        "mobilesdk_app_id": "YOUR_ANDROID_APP_ID"
      },
      "api_key": [
        {
          "current_key": "YOUR_ANDROID_API_KEY"
        }
      ]
    }
  ]
}
```

#### From GoogleService-Info.plist (iOS):
```xml
<key>API_KEY</key>
<string>YOUR_IOS_API_KEY</string>
<key>GOOGLE_APP_ID</key>
<string>YOUR_IOS_APP_ID</string>
<key>PROJECT_ID</key>
<string>anti-drowing-emergency</string>
```

## 🧪 Test Firebase Setup

### 1. Test Basic Connection
Run the app and check logs for:
```
Firebase initialized successfully
FCM token: [long_token_string]
```

### 2. Test Notifications via Firebase Console
1. Go to Firebase Console → **Cloud Messaging**
2. Click "Send your first message"
3. **Notification title**: "Test Emergency"
4. **Notification text**: "Testing emergency notification"
5. Click "Next" → Select your app → "Next"
6. **Additional options** → **Custom data**:
   - Key: `type`, Value: `emergency`
   - Key: `case_id`, Value: `TEST001`
   - Key: `latitude`, Value: `40.7128`
   - Key: `longitude`, Value: `-74.0060`
7. Click "Review" → "Publish"

### 3. Expected Behavior
- App should show full-screen emergency alert
- Alert should display case ID and coordinates
- Three action buttons should be visible

## 🔐 Backend Integration

### Server Key for Backend
1. Go to Firebase Console → **Project Settings** → **Cloud Messaging**
2. Copy the **Server Key**
3. Add to your backend environment variables:
```env
FIREBASE_SERVER_KEY=your_server_key_here
```

### Backend Notification Format
Your backend should send notifications like this:
```python
import requests

def send_emergency_notification(fcm_token, case_id, latitude, longitude):
    url = "https://fcm.googleapis.com/fcm/send"
    headers = {
        "Authorization": f"key={FIREBASE_SERVER_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "to": fcm_token,
        "data": {
            "type": "emergency",
            "case_id": case_id,
            "latitude": str(latitude),
            "longitude": str(longitude)
        }
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()
```

## 🚨 Production Checklist

- [ ] Firebase project created
- [ ] Cloud Messaging enabled
- [ ] Android app registered
- [ ] iOS app registered
- [ ] Configuration files downloaded and placed
- [ ] firebase_options.dart updated with real values
- [ ] Test notification sent and received
- [ ] Backend has Firebase server key
- [ ] Emergency alert screen works correctly

## 🔧 Troubleshooting

### Common Issues

#### "Firebase not initialized"
- Check firebase_options.dart has correct values
- Ensure Firebase.initializeApp() is called in main()

#### "No FCM token received"
- Check internet connection
- Verify Firebase configuration files are in correct locations
- Check app permissions for notifications

#### "Emergency screen not showing"
- Verify notification data has `type: "emergency"`
- Check notification service is properly initialized
- Ensure app has notification permissions

#### "Build errors"
- Run `flutter clean && flutter pub get`
- Check all configuration files are in place
- Verify gradle/podfile configurations

### Debug Commands
```bash
# Check Firebase connection
flutter run --verbose

# Check notification permissions
adb logcat | grep -i firebase  # Android
# iOS: Check Xcode console

# Test FCM token
flutter run --debug
# Look for "FCM token: ..." in logs
```

---

**Firebase setup complete! Your app is ready for emergency notifications.** 🚨