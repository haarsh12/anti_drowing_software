import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'dart:async';
import '../services/api_service.dart';
import '../services/notification_service.dart';

class MapScreen extends StatefulWidget {
  const MapScreen({super.key});

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  GoogleMapController? _mapController;
  List<Map<String, dynamic>> _alerts = [];
  Set<Marker> _markers = {};
  bool _isLoading = true;
  Timer? _refreshTimer;
  
  // Jalgaon, Maharashtra coordinates (exact match with web dashboard)
  static const CameraPosition _jalgaonPosition = CameraPosition(
    target: LatLng(20.947409, 75.554987),
    zoom: 13.0,
  );

  @override
  void initState() {
    super.initState();
    _loadAlerts();
    _startAutoRefresh();
  }

  @override
  void dispose() {
    _refreshTimer?.cancel();
    _mapController?.dispose();
    super.dispose();
  }

  void _startAutoRefresh() {
    _refreshTimer = Timer.periodic(const Duration(seconds: 5), (timer) {
      _loadAlerts();
    });
  }

  Future<void> _loadAlerts() async {
    try {
      final response = await ApiService.getAlerts();
      final alertsData = List<Map<String, dynamic>>.from(response['alerts'] ?? []);
      
      setState(() {
        _alerts = alertsData;
        _isLoading = false;
      });
      
      _updateMarkers();
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      print('Failed to load alerts: $e');
    }
  }

  void _updateMarkers() {
    final Set<Marker> markers = {};
    
    for (int i = 0; i < _alerts.length; i++) {
      final alert = _alerts[i];
      final alertId = alert['id']?.toString() ?? i.toString();
      final latitude = alert['latitude']?.toDouble() ?? 20.947409;
      final longitude = alert['longitude']?.toDouble() ?? 75.554987;
      final isDanger = alert['danger'] == true;
      final deviceId = alert['device_id'] ?? 'Unknown Device';
      
      // Create marker with red for danger, grey for safe (exact match with web dashboard)
      markers.add(
        Marker(
          markerId: MarkerId(alertId),
          position: LatLng(latitude, longitude),
          icon: isDanger 
            ? BitmapDescriptor.defaultMarkerWithHue(BitmapDescriptor.hueRed)
            : BitmapDescriptor.defaultMarkerWithHue(BitmapDescriptor.hueOrange), // Grey-ish
          infoWindow: InfoWindow(
            title: isDanger ? '🚨 CURRENT ALERT' : '✓ Previous Alert',
            snippet: '$deviceId\n${latitude.toStringAsFixed(6)}, ${longitude.toStringAsFixed(6)}',
            onTap: () => _showAlertDetails(alert),
          ),
          onTap: () => _showAlertDetails(alert),
        ),
      );
    }
    
    setState(() {
      _markers = markers;
    });
  }

  void _showAlertDetails(Map<String, dynamic> alert) {
    final alertId = alert['id']?.toString() ?? 'Unknown';
    final latitude = alert['latitude']?.toDouble() ?? 0.0;
    final longitude = alert['longitude']?.toDouble() ?? 0.0;
    final isDanger = alert['danger'] == true;
    final deviceId = alert['device_id'] ?? 'Unknown Device';
    final timestamp = alert['timestamp'] ?? '';
    
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => Container(
        height: MediaQuery.of(context).size.height * 0.7,
        decoration: const BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.only(
            topLeft: Radius.circular(20),
            topRight: Radius.circular(20),
          ),
        ),
        child: Column(
          children: [
            // Handle bar
            Container(
              margin: const EdgeInsets.only(top: 12),
              width: 40,
              height: 4,
              decoration: BoxDecoration(
                color: Colors.grey.shade300,
                borderRadius: BorderRadius.circular(2),
              ),
            ),
            
            // Header
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: isDanger ? Colors.red.shade50 : Colors.grey.shade50,
                borderRadius: const BorderRadius.only(
                  topLeft: Radius.circular(20),
                  topRight: Radius.circular(20),
                ),
              ),
              child: Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: isDanger ? Colors.red : Colors.grey.shade600,
                      shape: BoxShape.circle,
                    ),
                    child: Icon(
                      isDanger ? Icons.warning_rounded : Icons.check_circle_rounded,
                      color: Colors.white,
                      size: 24,
                    ),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          isDanger ? '🚨 CURRENT ALERT' : '✓ Previous Alert',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: isDanger ? Colors.red.shade700 : Colors.grey.shade700,
                          ),
                        ),
                        Text(
                          'Alert ID: $alertId',
                          style: TextStyle(
                            fontSize: 14,
                            color: isDanger ? Colors.red.shade600 : Colors.grey.shade600,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
            
            // Details
            Expanded(
              child: Padding(
                padding: const EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    _buildDetailRow(Icons.smartphone_rounded, 'Device', deviceId),
                    const SizedBox(height: 16),
                    _buildDetailRow(Icons.location_on_rounded, 'Location', 
                      'Jalgaon, Maharashtra\n${latitude.toStringAsFixed(6)}, ${longitude.toStringAsFixed(6)}'),
                    const SizedBox(height: 16),
                    _buildDetailRow(Icons.access_time_rounded, 'Time', 
                      DateTime.tryParse(timestamp)?.toLocal().toString() ?? 'Unknown'),
                    const SizedBox(height: 32),
                    
                    // Action Buttons
                    Row(
                      children: [
                        Expanded(
                          child: ElevatedButton.icon(
                            onPressed: () async {
                              await NotificationService.openGoogleMaps(latitude, longitude);
                            },
                            icon: const Icon(Icons.map_rounded, size: 20),
                            label: const Text('Open in Google Maps'),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Colors.blue.shade600,
                              foregroundColor: Colors.white,
                              padding: const EdgeInsets.symmetric(vertical: 16),
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(12),
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                    
                    if (isDanger) ...[
                      const SizedBox(height: 16),
                      Container(
                        width: double.infinity,
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          color: Colors.red.shade50,
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(color: Colors.red.shade200),
                        ),
                        child: Column(
                          children: [
                            Icon(Icons.warning_rounded, color: Colors.red.shade600, size: 32),
                            const SizedBox(height: 8),
                            Text(
                              'EMERGENCY ACTIVE',
                              style: TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                                color: Colors.red.shade700,
                              ),
                            ),
                            const SizedBox(height: 4),
                            Text(
                              'Immediate response required!',
                              style: TextStyle(
                                fontSize: 14,
                                color: Colors.red.shade600,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDetailRow(IconData icon, String label, String value) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(
            color: Colors.blue.shade50,
            borderRadius: BorderRadius.circular(8),
          ),
          child: Icon(icon, color: Colors.blue.shade600, size: 20),
        ),
        const SizedBox(width: 16),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                label,
                style: const TextStyle(
                  fontSize: 12,
                  color: Colors.grey,
                  fontWeight: FontWeight.w500,
                ),
              ),
              const SizedBox(height: 4),
              Text(
                value,
                style: const TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w600,
                  color: Colors.black87,
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          // Google Map
          GoogleMap(
            onMapCreated: (GoogleMapController controller) {
              _mapController = controller;
            },
            initialCameraPosition: _jalgaonPosition,
            markers: _markers,
            mapType: MapType.normal,
            zoomControlsEnabled: true,
            myLocationButtonEnabled: false,
            compassEnabled: true,
            mapToolbarEnabled: false,
          ),
          
          // Top overlay with info
          Positioned(
            top: 0,
            left: 0,
            right: 0,
            child: Container(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [
                    const Color(0xFF2196F3),
                    const Color(0xFF2196F3).withOpacity(0.8),
                    Colors.transparent,
                  ],
                ),
              ),
              child: SafeArea(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    children: [
                      Row(
                        children: [
                          Container(
                            padding: const EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              color: Colors.white.withOpacity(0.2),
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: const Icon(
                              Icons.location_on_rounded,
                              color: Colors.white,
                              size: 24,
                            ),
                          ),
                          const SizedBox(width: 16),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const Text(
                                  'Emergency Map',
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 20,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                const Text(
                                  'Jalgaon, Maharashtra',
                                  style: TextStyle(
                                    color: Colors.white70,
                                    fontSize: 14,
                                  ),
                                ),
                              ],
                            ),
                          ),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                            decoration: BoxDecoration(
                              color: Colors.white.withOpacity(0.2),
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                if (_isLoading)
                                  const SizedBox(
                                    width: 16,
                                    height: 16,
                                    child: CircularProgressIndicator(
                                      strokeWidth: 2,
                                      color: Colors.white,
                                    ),
                                  )
                                else
                                  GestureDetector(
                                    onTap: _loadAlerts,
                                    child: const Icon(Icons.refresh, color: Colors.white, size: 16),
                                  ),
                                const SizedBox(width: 8),
                                Text(
                                  '${_alerts.length} Alerts',
                                  style: const TextStyle(
                                    color: Colors.white,
                                    fontSize: 12,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                      
                      const SizedBox(height: 16),
                      
                      // Legend (exact match with web dashboard)
                      Container(
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: Colors.white.withOpacity(0.15),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                          children: [
                            _buildLegendItem('🔴', 'Current Alert', Colors.red),
                            _buildLegendItem('🟠', 'Previous Alert', Colors.grey),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
          
          // Center on Jalgaon button
          Positioned(
            bottom: 100,
            right: 16,
            child: FloatingActionButton(
              onPressed: () {
                _mapController?.animateCamera(
                  CameraUpdate.newCameraPosition(_jalgaonPosition),
                );
              },
              backgroundColor: Colors.white,
              foregroundColor: const Color(0xFF2196F3),
              child: const Icon(Icons.my_location_rounded),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildLegendItem(String emoji, String label, Color color) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Text(emoji, style: const TextStyle(fontSize: 14)),
        const SizedBox(width: 6),
        Text(
          label,
          style: const TextStyle(
            fontSize: 11,
            color: Colors.white,
            fontWeight: FontWeight.w500,
          ),
        ),
      ],
    );
  }
}