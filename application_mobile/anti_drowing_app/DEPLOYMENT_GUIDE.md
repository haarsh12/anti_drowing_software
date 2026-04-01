# 🚀 Production Deployment Guide

## 📋 Pre-Deployment Checklist

### ✅ Backend Requirements
- [ ] FastAPI backend running and accessible
- [ ] Supabase database configured
- [ ] API endpoints working:
  - `GET /api/cases`
  - `POST /api/case-action`
  - `POST /api/register-device`
- [ ] Firebase server key configured in backend
- [ ] CORS configured for mobile app

### ✅ Firebase Configuration
- [ ] Firebase project created
- [ ] Cloud Messaging enabled
- [ ] Android app registered
- [ ] iOS app registered (if deploying to iOS)
- [ ] Configuration files in place
- [ ] Test notifications working

### ✅ App Configuration
- [ ] Backend URL updated in `api_service.dart`
- [ ] Firebase options configured
- [ ] App name and package ID set
- [ ] Permissions configured
- [ ] Icons and splash screen ready

## 🤖 Android Deployment

### 1. Prepare for Release

#### Update App Information
Edit `android/app/build.gradle.kts`:
```kotlin
android {
    defaultConfig {
        applicationId = "com.yourcompany.anti_drowing_app"  // Change this
        versionCode = 1
        versionName = "1.0.0"
    }
}
```

#### Create Signing Key
```bash
keytool -genkey -v -keystore ~/anti-drowing-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias anti-drowing
```

#### Configure Signing
Create `android/key.properties`:
```properties
storePassword=your_store_password
keyPassword=your_key_password
keyAlias=anti-drowing
storeFile=/path/to/anti-drowing-key.jks
```

Update `android/app/build.gradle.kts`:
```kotlin
// Add at top
val keystoreProperties = Properties()
val keystorePropertiesFile = rootProject.file("key.properties")
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(FileInputStream(keystorePropertiesFile))
}

android {
    signingConfigs {
        create("release") {
            keyAlias = keystoreProperties["keyAlias"] as String
            keyPassword = keystoreProperties["keyPassword"] as String
            storeFile = file(keystoreProperties["storeFile"] as String)
            storePassword = keystoreProperties["storePassword"] as String
        }
    }
    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("release")
        }
    }
}
```

### 2. Build Release APK
```bash
flutter build apk --release
```

### 3. Build App Bundle (for Play Store)
```bash
flutter build appbundle --release
```

### 4. Test Release Build
```bash
flutter install --release
```

## 🍎 iOS Deployment

### 1. Prepare for Release

#### Update iOS Configuration
Edit `ios/Runner/Info.plist`:
```xml
<key>CFBundleDisplayName</key>
<string>Anti Drowing</string>
<key>CFBundleVersion</key>
<string>1</string>
<key>CFBundleShortVersionString</key>
<string>1.0.0</string>
```

#### Configure App Store Connect
1. Create app in App Store Connect
2. Set bundle ID: `com.yourcompany.anti_drowing_app`
3. Configure app information

### 2. Build for iOS
```bash
flutter build ios --release
```

### 3. Archive and Upload
1. Open `ios/Runner.xcworkspace` in Xcode
2. Select "Any iOS Device" as target
3. Product → Archive
4. Upload to App Store Connect

## 🔧 Environment Configuration

### Production API Service
Update `lib/services/api_service.dart`:
```dart
class ApiService {
  // Production backend URL
  static const String baseUrl = 'https://your-production-backend.com';
  
  // Add error handling and retry logic
  static Future<Map<String, dynamic>> _makeRequest(
    String method,
    String endpoint,
    {Map<String, dynamic>? body}
  ) async {
    const maxRetries = 3;
    for (int i = 0; i < maxRetries; i++) {
      try {
        // Your request logic here
        break;
      } catch (e) {
        if (i == maxRetries - 1) rethrow;
        await Future.delayed(Duration(seconds: 2 * (i + 1)));
      }
    }
  }
}
```

### Production Firebase Config
Ensure `lib/firebase_options.dart` has production values:
```dart
static const FirebaseOptions android = FirebaseOptions(
  apiKey: 'your-production-android-api-key',
  appId: 'your-production-android-app-id',
  messagingSenderId: 'your-production-sender-id',
  projectId: 'your-production-project-id',
  storageBucket: 'your-production-project.appspot.com',
);
```

## 📱 App Store Submission

### Google Play Store

#### 1. Prepare Store Listing
- **App name**: Anti Drowing - Emergency Response
- **Short description**: Emergency response app for drowning incidents
- **Full description**: Detailed description of features
- **Screenshots**: Take screenshots of all key screens
- **Feature graphic**: Create 1024x500 banner
- **App icon**: 512x512 high-res icon

#### 2. Upload APK/Bundle
1. Go to Google Play Console
2. Create new app
3. Upload app bundle
4. Fill out store listing
5. Set content rating
6. Set pricing (Free)
7. Submit for review

### Apple App Store

#### 1. App Store Connect Setup
- **App Information**: Name, bundle ID, SKU
- **Pricing**: Free
- **App Review Information**: Contact details
- **Version Information**: What's new, screenshots
- **Build**: Select uploaded build

#### 2. Submit for Review
1. Complete all required fields
2. Submit for App Store review
3. Wait for approval (typically 1-7 days)

## 🔒 Security Considerations

### API Security
```dart
class ApiService {
  static const String baseUrl = 'https://your-backend.com';
  
  // Add API key authentication
  static Map<String, String> get _headers => {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ${_getApiKey()}',
    'User-Agent': 'AntiDrowingApp/1.0.0',
  };
  
  static String _getApiKey() {
    // Implement secure API key storage
    return 'your-api-key';
  }
}
```

### Certificate Pinning (Advanced)
```dart
// Add certificate pinning for production
class SecureApiService {
  static final HttpClient _httpClient = HttpClient()
    ..badCertificateCallback = (cert, host, port) {
      // Implement certificate validation
      return _validateCertificate(cert, host);
    };
}
```

## 📊 Monitoring & Analytics

### Crash Reporting
Add Firebase Crashlytics:
```yaml
dependencies:
  firebase_crashlytics: ^3.4.8
```

```dart
// In main.dart
import 'package:firebase_crashlytics/firebase_crashlytics.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  
  // Set up Crashlytics
  FlutterError.onError = FirebaseCrashlytics.instance.recordFlutterFatalError;
  PlatformDispatcher.instance.onError = (error, stack) {
    FirebaseCrashlytics.instance.recordError(error, stack, fatal: true);
    return true;
  };
  
  runApp(AntiDrowingApp());
}
```

### Performance Monitoring
```yaml
dependencies:
  firebase_performance: ^0.9.3+8
```

## 🧪 Testing Strategy

### Pre-Release Testing
1. **Unit Tests**: Test API service methods
2. **Widget Tests**: Test UI components
3. **Integration Tests**: Test complete flows
4. **Device Testing**: Test on multiple devices
5. **Network Testing**: Test offline scenarios

### Test Emergency Flow
```bash
# Test script for emergency notifications
flutter test test/emergency_flow_test.dart
```

## 📈 Post-Launch Monitoring

### Key Metrics to Track
- **App crashes**: Monitor via Firebase Crashlytics
- **Notification delivery**: Track FCM success rates
- **API response times**: Monitor backend performance
- **User engagement**: Track emergency response times
- **App store ratings**: Monitor user feedback

### Performance Monitoring
```dart
// Add performance tracking
class PerformanceService {
  static void trackEmergencyResponseTime(String caseId, Duration responseTime) {
    FirebasePerformance.instance
      .newTrace('emergency_response')
      .putAttribute('case_id', caseId)
      .putMetric('response_time_ms', responseTime.inMilliseconds)
      .stop();
  }
}
```

## 🔄 Update Strategy

### Over-the-Air Updates
Consider using:
- **CodePush** for React Native-like updates
- **Firebase Remote Config** for feature flags
- **App Store/Play Store** for major updates

### Version Management
```dart
// In pubspec.yaml
version: 1.0.0+1  # version+build_number

// Increment for updates:
// 1.0.1+2  # Bug fix
// 1.1.0+3  # New features
// 2.0.0+4  # Major changes
```

## 🚨 Emergency Rollback Plan

### If Critical Issues Occur
1. **Immediate**: Disable emergency notifications via Firebase
2. **Short-term**: Roll back to previous app version
3. **Long-term**: Fix issues and redeploy

### Rollback Commands
```bash
# Disable notifications via Firebase Console
# Or via API:
curl -X POST "https://fcm.googleapis.com/fcm/send" \
  -H "Authorization: key=YOUR_SERVER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"to":"/topics/emergency","data":{"disable":"true"}}'
```

---

**Your Anti Drowing app is ready for production deployment!** 🚀

Remember to test thoroughly in a staging environment before going live with emergency response functionality.