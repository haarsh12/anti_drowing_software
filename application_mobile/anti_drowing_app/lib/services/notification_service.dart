import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import '../screens/system_emergency_overlay.dart';
import 'api_service.dart';
import 'dart:async';
import 'dart:io';
import 'dart:typed_data';

class NotificationService {
  static BuildContext? _context;
  static Timer? _pollingTimer;
  static Set<String> _processedAlerts = {};
  static FlutterLocalNotificationsPlugin? _flutterLocalNotificationsPlugin;
  
  static Future<void> initialize() async {
    _flutterLocalNotificationsPlugin = FlutterLocalNotificationsPlugin();
    
    // Android initialization
    const AndroidInitializationSettings initializationSettingsAndroid =
        AndroidInitializationSettings('@mipmap/ic_launcher');
    
    // iOS initialization
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
    
    await _flutterLocalNotificationsPlugin?.initialize(
      initializationSettings,
      onDidReceiveNotificationResponse: _onNotificationTapped,
    );
    
    // Request permissions for Android 13+
    if (Platform.isAndroid) {
      await _flutterLocalNotificationsPlugin
          ?.resolvePlatformSpecificImplementation<
              AndroidFlutterLocalNotificationsPlugin>()
          ?.requestNotificationsPermission();
    }
    
    print('✅ System-level notification service initialized');
  }
  
  static void _onNotificationTapped(NotificationResponse response) {
    // Handle notification tap - open emergency screen
    final payload = response.payload;
    if (payload != null && _context != null) {
      final parts = payload.split('|');
      if (parts.length >= 3) {
        final caseId = parts[0];
        final latitude = double.tryParse(parts[1]) ?? 0.0;
        final longitude = double.tryParse(parts[2]) ?? 0.0;
        
        _showFullScreenEmergencyAlert({
          'id': caseId,
          'latitude': latitude,
          'longitude': longitude,
        });
      }
    }
  }
  
  static void setContext(BuildContext context) {
    _context = context;
    _startPollingForAlerts();
  }
  
  static void _startPollingForAlerts() {
    _pollingTimer?.cancel();
    _pollingTimer = Timer.periodic(const Duration(seconds: 3), (timer) async {
      await _checkForNewAlerts();
    });
    print('✅ Started polling for new alerts every 3 seconds');
  }
  
  static Future<void> _checkForNewAlerts() async {
    try {
      final response = await ApiService.getAlerts();
      final alerts = List<Map<String, dynamic>>.from(response['alerts'] ?? []);
      
      for (final alert in alerts) {
        final alertId = alert['id']?.toString() ?? '';
        final isDanger = alert['danger'] == true;
        
        // Only show notifications for danger alerts that haven't been processed
        if (isDanger && !_processedAlerts.contains(alertId)) {
          _processedAlerts.add(alertId);
          await _showEmergencyAlert(alert);
        }
      }
    } catch (e) {
      print('Error checking for alerts: $e');
    }
  }
  
  static Future<void> _showEmergencyAlert(Map<String, dynamic> alert) async {
    final alertId = alert['id']?.toString() ?? '';
    final latitude = alert['latitude']?.toDouble() ?? 0.0;
    final longitude = alert['longitude']?.toDouble() ?? 0.0;
    final deviceId = alert['device_id'] ?? 'Unknown Device';
    
    // Intense vibration pattern
    HapticFeedback.heavyImpact();
    await Future.delayed(const Duration(milliseconds: 200));
    HapticFeedback.heavyImpact();
    await Future.delayed(const Duration(milliseconds: 200));
    HapticFeedback.heavyImpact();
    
    // Show system-level notification (works even when app is closed)
    await _showSystemNotification(alert);
    
    // Show full-screen emergency alert only if app is active
    if (_context != null) {
      _showFullScreenEmergencyAlert(alert);
    }
    
    print('🚨 Emergency alert shown for: $alertId at device: $deviceId');
  }
  
  static Future<void> _showSystemNotification(Map<String, dynamic> alert) async {
    if (_flutterLocalNotificationsPlugin == null) return;
    
    final alertId = alert['id']?.toString() ?? '';
    final latitude = alert['latitude']?.toDouble() ?? 0.0;
    final longitude = alert['longitude']?.toDouble() ?? 0.0;
    final deviceId = alert['device_id'] ?? 'Unknown Device';
    
    // Create notification payload
    final payload = '$alertId|$latitude|$longitude';
    
    // Android notification details - simplified for compatibility
    const AndroidNotificationDetails androidPlatformChannelSpecifics =
        AndroidNotificationDetails(
      'emergency_channel',
      'Emergency Alerts',
      channelDescription: 'Critical emergency drowning alerts',
      importance: Importance.max,
      priority: Priority.high,
      showWhen: true,
      enableVibration: true,
      enableLights: true,
      color: Color.fromARGB(255, 255, 0, 0),
      ticker: '🚨 DROWNING EMERGENCY',
      category: AndroidNotificationCategory.alarm,
      visibility: NotificationVisibility.public,
      ongoing: true,
      autoCancel: false,
    );
    
    // iOS notification details
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
    
    await _flutterLocalNotificationsPlugin!.show(
      int.parse(alertId.replaceAll(RegExp(r'[^0-9]'), '').padLeft(1, '1')),
      '🚨 DROWNING EMERGENCY',
      'Case: CASE${alertId.padLeft(3, '0')} - Device: $deviceId\nLocation: ${latitude.toStringAsFixed(4)}, ${longitude.toStringAsFixed(4)}\nTap to respond immediately!',
      platformChannelSpecifics,
      payload: payload,
    );
  }
  
  static void _showFullScreenEmergencyAlert(Map<String, dynamic> alert) {
    if (_context == null) return;
    
    final alertId = alert['id']?.toString() ?? '';
    final latitude = alert['latitude']?.toDouble() ?? 0.0;
    final longitude = alert['longitude']?.toDouble() ?? 0.0;
    
    // Show system-level overlay that works even when phone is locked
    Navigator.of(_context!).push(
      PageRouteBuilder(
        opaque: false,
        barrierDismissible: false,
        barrierColor: Colors.transparent,
        pageBuilder: (context, animation, secondaryAnimation) => SystemEmergencyOverlay(
          caseId: 'CASE${alertId.padLeft(3, '0')}',
          latitude: latitude,
          longitude: longitude,
        ),
        transitionsBuilder: (context, animation, secondaryAnimation, child) {
          return FadeTransition(
            opacity: animation,
            child: child,
          );
        },
      ),
    );
  }
  
  static Future<void> openGoogleMaps(double latitude, double longitude) async {
    final url = 'https://www.google.com/maps/search/?api=1&query=' + latitude.toString() + ',' + longitude.toString();
    if (await canLaunchUrl(Uri.parse(url))) {
      await launchUrl(Uri.parse(url), mode: LaunchMode.externalApplication);
    } else {
      print('Could not launch Google Maps');
    }
  }
  
  static void dispose() {
    _pollingTimer?.cancel();
    _processedAlerts.clear();
  }
}