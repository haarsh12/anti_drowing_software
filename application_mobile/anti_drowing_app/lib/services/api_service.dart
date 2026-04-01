import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  static const String baseUrl = 'http://127.0.0.1:8000'; // Your backend URL
  
  // Get all cases (using alerts endpoint from your backend)
  static Future<Map<String, dynamic>> getCases() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/alerts'),
        headers: {'Content-Type': 'application/json'},
      ).timeout(const Duration(seconds: 10));
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        // Transform alerts to cases format
        return {
          'cases': data['alerts'] ?? [],
          'total': data['total'] ?? 0,
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
  
  // Update case action (placeholder - your backend doesn't have this endpoint yet)
  static Future<Map<String, dynamic>> updateCaseAction({
    required String caseId,
    required String action,
    required String actionBy,
  }) async {
    try {
      // For now, just return success since your backend doesn't have this endpoint
      print('Case action: $action by $actionBy for case $caseId');
      return {
        'success': true,
        'message': 'Action recorded successfully',
      };
    } catch (e) {
      throw Exception('Network error: $e');
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