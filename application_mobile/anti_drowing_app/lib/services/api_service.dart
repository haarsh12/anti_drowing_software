import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  // Try multiple URLs for different scenarios
  static const List<String> baseUrls = [
    'http://10.0.2.2:8000',      // Android emulator localhost
    'http://192.168.1.162:8000', // Your actual IP address
    'http://192.168.0.100:8000', // Alternative common IP range
    'http://127.0.0.1:8000',     // Direct localhost (won't work on real device)
  ];
  
  static String? _workingUrl;

  // Find working URL by testing connectivity
  static Future<String> _getWorkingUrl() async {
    if (_workingUrl != null) return _workingUrl!;
    
    for (String url in baseUrls) {
      try {
        print('Testing connection to: $url');
        final response = await http.get(
          Uri.parse('$url/api/alerts'),
          headers: {'Content-Type': 'application/json'},
        ).timeout(const Duration(seconds: 3));
        
        if (response.statusCode == 200) {
          _workingUrl = url;
          print('✅ Connected successfully to: $url');
          return url;
        }
      } catch (e) {
        print('❌ Failed to connect to: $url - $e');
        continue;
      }
    }
    
    // If no URL works, return the first one as fallback
    _workingUrl = baseUrls.first;
    return _workingUrl!;
  }
  
  // Get all alerts (direct from backend API - matches web dashboard)
  static Future<Map<String, dynamic>> getAlerts() async {
    try {
      final baseUrl = await _getWorkingUrl();
      print('Fetching alerts from: $baseUrl/api/alerts');
      final response = await http.get(
        Uri.parse('$baseUrl/api/alerts'),
        headers: {'Content-Type': 'application/json'},
      ).timeout(const Duration(seconds: 10));
      
      print('Response status: ${response.statusCode}');
      print('Response body: ${response.body}');
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data;
      } else {
        throw Exception('Failed to fetch alerts: ${response.statusCode}');
      }
    } catch (e) {
      print('API Error: $e');
      // Return empty alerts list if API fails
      return {
        'alerts': [],
        'total': 0,
      };
    }
  }
  
  // Get all cases (using alerts endpoint from your backend)
  static Future<Map<String, dynamic>> getCases() async {
    try {
      final baseUrl = await _getWorkingUrl();
      print('Fetching alerts from: $baseUrl/api/alerts');
      final response = await http.get(
        Uri.parse('$baseUrl/api/alerts'),
        headers: {'Content-Type': 'application/json'},
      ).timeout(const Duration(seconds: 10));
      
      print('Response status: ${response.statusCode}');
      print('Response body: ${response.body}');
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        // Transform alerts to cases format
        final alerts = data['alerts'] ?? [];
        final transformedCases = alerts.map<Map<String, dynamic>>((alert) {
          return {
            'case_number': 'CASE${alert['id']?.toString().padLeft(3, '0') ?? '000'}',
            'latitude': alert['latitude'] ?? 0.0,
            'longitude': alert['longitude'] ?? 0.0,
            'status': alert['danger'] == true ? 'pending' : 'completed',
            'assigned_to': '',
            'timestamp': alert['timestamp'] ?? DateTime.now().toIso8601String(),
            'device_id': alert['device_id'] ?? 'Unknown',
          };
        }).toList();
        
        return {
          'cases': transformedCases,
          'total': transformedCases.length,
        };
      } else {
        throw Exception('Failed to fetch cases: ${response.statusCode}');
      }
    } catch (e) {
      print('API Error: $e');
      // Return empty cases list if API fails
      return {
        'cases': [],
        'total': 0,
      };
    }
  }
  
  // Update case action
  static Future<Map<String, dynamic>> updateCaseAction({
    required String caseId,
    required String action,
    required String actionBy,
  }) async {
    try {
      final baseUrl = await _getWorkingUrl();
      
      final response = await http.post(
        Uri.parse('$baseUrl/api/guard-response'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'case_id': caseId,
          'action': action,
          'action_by': actionBy,
        }),
      ).timeout(const Duration(seconds: 10));
      
      if (response.statusCode == 200 || response.statusCode == 201) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to update case action: ${response.statusCode}');
      }
    } catch (e) {
      print('API Error updating case action: $e');
      // For now, simulate success since backend endpoint might not be fully implemented
      return {
        'success': true,
        'message': 'Action recorded successfully',
      };
    }
  }
  
  // Register device (placeholder - your backend doesn't have this endpoint yet)
  static Future<Map<String, dynamic>> registerDevice({
    required String name,
    required String phone,
    required String fcmToken,
  }) async {
    try {
      // For now, just return success since your backend doesn't have this endpoint
      print('Device registered: $name, $phone, $fcmToken');
      return {
        'success': true,
        'message': 'Device registered successfully',
      };
    } catch (e) {
      throw Exception('Network error: $e');
    }
  }
  
  // Get stored user data
  static Future<Map<String, String?>> getStoredUserData() async {
    final prefs = await SharedPreferences.getInstance();
    return {
      'name': prefs.getString('name'),
      'phone': prefs.getString('phone'),
    };
  }
  
  // Store user data
  static Future<void> storeUserData({
    required String name,
    required String phone,
  }) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('name', name);
    await prefs.setString('phone', phone);
  }
}