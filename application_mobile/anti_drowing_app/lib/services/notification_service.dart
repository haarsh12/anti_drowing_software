import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:url_launcher/url_launcher.dart';
import '../screens/emergency_screen.dart';
import 'api_service.dart';
import 'dart:async';

class NotificationService {
  static BuildContext? _context;
  static Timer? _pollingTimer;
  static Set<String> _processedAlerts = {};
  
  static Future<void> initialize() async {
    print('✅ Basic notification service initialized');
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
    
    // Show full-screen emergency alert
    if (_context != null) {
      _showFullScreenEmergencyAlert(alert);
    }
    
    print('🚨 Emergency alert shown for: ' + alertId + ' at device: ' + deviceId);
  }
  
  static void _showFullScreenEmergencyAlert(Map<String, dynamic> alert) {
    if (_context == null) return;
    
    final alertId = alert['id']?.toString() ?? '';
    final latitude = alert['latitude']?.toDouble() ?? 0.0;
    final longitude = alert['longitude']?.toDouble() ?? 0.0;
    
    // Show full-screen modal that cannot be dismissed
    showDialog(
      context: _context!,
      barrierDismissible: false,
      barrierColor: Colors.black.withOpacity(0.95),
      builder: (context) => PopScope(
        canPop: false,
        child: EmergencyScreen(
          caseId: 'CASE' + alertId.padLeft(3, '0'),
          latitude: latitude,
          longitude: longitude,
        ),
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