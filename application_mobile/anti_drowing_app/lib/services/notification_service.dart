import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:flutter/material.dart';
import '../screens/emergency_screen.dart';
import 'api_service.dart';

class NotificationService {
  static final FirebaseMessaging _firebaseMessaging = FirebaseMessaging.instance;
  static final FlutterLocalNotificationsPlugin _localNotifications = FlutterLocalNotificationsPlugin();
  static BuildContext? _context;
  
  static Future<void> initialize() async {
    // Request permission
    NotificationSettings settings = await _firebaseMessaging.requestPermission(
      alert: true,
      announcement: false,
      badge: true,
      carPlay: false,
      criticalAlert: true,
      provisional: false,
      sound: true,
    );
    
    if (settings.authorizationStatus == AuthorizationStatus.authorized) {
      print('User granted permission');
    } else {
      print('User declined or has not accepted permission');
    }
    
    // Initialize local notifications
    const AndroidInitializationSettings initializationSettingsAndroid =
        AndroidInitializationSettings('@mipmap/ic_launcher');
    
    const DarwinInitializationSettings initializationSettingsIOS =
        DarwinInitializationSettings(
      requestAlertPermission: true,
      requestBadgePermission: true,
      requestSoundPermission: true,
    );
    
    const InitializationSettings initializationSettings =
        InitializationSettings(
      android: initializationSettingsAndroid,
      iOS: initializationSettingsIOS,
    );
    
    await _localNotifications.initialize(
      initializationSettings,
      onDidReceiveNotificationResponse: _onNotificationTapped,
    );
    
    // Handle background messages
    FirebaseMessaging.onBackgroundMessage(_firebaseMessagingBackgroundHandler);
    
    // Handle foreground messages
    FirebaseMessaging.onMessage.listen(_handleForegroundMessage);
    
    // Handle notification opened app
    FirebaseMessaging.onMessageOpenedApp.listen(_handleMessageOpenedApp);
    
    // Get FCM token and register device
    await _registerDevice();
  }
  
  static void setContext(BuildContext context) {
    _context = context;
  }
  
  static Future<void> _registerDevice() async {
    try {
      final token = await _firebaseMessaging.getToken();
      if (token != null) {
        final userData = await ApiService.getStoredUserData();
        if (userData['name'] != null && userData['phone'] != null) {
          await ApiService.registerDevice(
            name: userData['name']!,
            phone: userData['phone']!,
            fcmToken: token,
          );
          print('Device registered with FCM token: $token');
        }
      }
    } catch (e) {
      print('Failed to register device: $e');
    }
  }
  
  static Future<void> _handleForegroundMessage(RemoteMessage message) async {
    print('Received foreground message: ${message.data}');
    
    if (message.data['type'] == 'emergency' && _context != null) {
      // Show emergency screen immediately
      Navigator.of(_context!).push(
        MaterialPageRoute(
          builder: (context) => EmergencyScreen(
            caseId: message.data['case_id'] ?? '',
            latitude: double.tryParse(message.data['latitude'] ?? '0') ?? 0.0,
            longitude: double.tryParse(message.data['longitude'] ?? '0') ?? 0.0,
          ),
          fullscreenDialog: true,
        ),
      );
    }
  }
  
  static Future<void> _handleMessageOpenedApp(RemoteMessage message) async {
    print('Message opened app: ${message.data}');
    
    if (message.data['type'] == 'emergency' && _context != null) {
      Navigator.of(_context!).push(
        MaterialPageRoute(
          builder: (context) => EmergencyScreen(
            caseId: message.data['case_id'] ?? '',
            latitude: double.tryParse(message.data['latitude'] ?? '0') ?? 0.0,
            longitude: double.tryParse(message.data['longitude'] ?? '0') ?? 0.0,
          ),
          fullscreenDialog: true,
        ),
      );
    }
  }
  
  static void _onNotificationTapped(NotificationResponse response) {
    print('Notification tapped: ${response.payload}');
    // Handle local notification tap if needed
  }
}

// Background message handler (must be top-level function)
@pragma('vm:entry-point')
Future<void> _firebaseMessagingBackgroundHandler(RemoteMessage message) async {
  print('Handling background message: ${message.data}');
  
  if (message.data['type'] == 'emergency') {
    // Show local notification for background emergency
    const AndroidNotificationDetails androidPlatformChannelSpecifics =
        AndroidNotificationDetails(
      'emergency_channel',
      'Emergency Alerts',
      channelDescription: 'Critical emergency notifications',
      importance: Importance.max,
      priority: Priority.high,
      showWhen: true,
      fullScreenIntent: true,
    );
    
    const DarwinNotificationDetails iOSPlatformChannelSpecifics =
        DarwinNotificationDetails(
      presentAlert: true,
      presentBadge: true,
      presentSound: true,
      interruptionLevel: InterruptionLevel.critical,
    );
    
    const NotificationDetails platformChannelSpecifics = NotificationDetails(
      android: androidPlatformChannelSpecifics,
      iOS: iOSPlatformChannelSpecifics,
    );
    
    await NotificationService._localNotifications.show(
      0,
      '🚨 EMERGENCY ALERT',
      'Emergency case requires immediate attention',
      platformChannelSpecifics,
      payload: message.data['case_id'],
    );
  }
}