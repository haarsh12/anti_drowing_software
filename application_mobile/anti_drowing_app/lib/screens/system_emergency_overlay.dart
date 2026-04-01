import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'dart:async';
import '../services/api_service.dart';
import '../services/notification_service.dart';

class SystemEmergencyOverlay extends StatefulWidget {
  final String caseId;
  final double latitude;
  final double longitude;

  const SystemEmergencyOverlay({
    super.key,
    required this.caseId,
    required this.latitude,
    required this.longitude,
  });

  @override
  State<SystemEmergencyOverlay> createState() => _SystemEmergencyOverlayState();
}

class _SystemEmergencyOverlayState extends State<SystemEmergencyOverlay>
    with TickerProviderStateMixin {
  late AnimationController _pulseController;
  late Animation<double> _pulseAnimation;
  bool _isProcessing = false;
  Timer? _urgencyTimer;
  List<Map<String, dynamic>> _guardResponses = [];

  @override
  void initState() {
    super.initState();
    
    // Intense vibration pattern on screen open
    _performEmergencyVibration();
    
    // Setup animations
    _pulseController = AnimationController(
      duration: const Duration(milliseconds: 1000),
      vsync: this,
    );
    
    _pulseAnimation = Tween<double>(
      begin: 1.0,
      end: 1.08,
    ).animate(CurvedAnimation(
      parent: _pulseController,
      curve: Curves.easeInOut,
    ));
    
    // Start animations
    _pulseController.repeat(reverse: true);
    
    // Load guard responses
    _loadGuardResponses();
    
    // Continuous urgency reminders
    _urgencyTimer = Timer.periodic(const Duration(seconds: 3), (timer) {
      if (mounted && !_isProcessing) {
        HapticFeedback.mediumImpact();
      } else {
        timer.cancel();
      }
    });
  }

  Future<void> _performEmergencyVibration() async {
    // Intense vibration pattern for emergency
    for (int i = 0; i < 4; i++) {
      HapticFeedback.heavyImpact();
      await Future.delayed(const Duration(milliseconds: 150));
    }
  }

  Future<void> _loadGuardResponses() async {
    // Mock guard responses - replace with actual API call
    setState(() {
      _guardResponses = [
        {
          'guard_name': 'Rajesh Kumar',
          'action': 'accepted',
          'timestamp': DateTime.now().subtract(const Duration(minutes: 2)),
          'phone': '+91 98765 43210',
        },
        {
          'guard_name': 'Priya Sharma',
          'action': 'not_available',
          'timestamp': DateTime.now().subtract(const Duration(minutes: 1)),
          'phone': '+91 87654 32109',
        },
      ];
    });
  }

  @override
  void dispose() {
    _pulseController.dispose();
    _urgencyTimer?.cancel();
    super.dispose();
  }

  Future<void> _handleAction(String action) async {
    if (_isProcessing) return;
    
    setState(() {
      _isProcessing = true;
    });
    
    HapticFeedback.heavyImpact();
    
    try {
      final userData = await ApiService.getStoredUserData();
      final userName = userData['name'] ?? 'Unknown Guard';
      
      await ApiService.updateCaseAction(
        caseId: widget.caseId,
        action: action,
        actionBy: userName,
      );
      
      // Success feedback
      HapticFeedback.lightImpact();
      
      if (mounted) {
        // Close overlay after success
        Navigator.of(context).pop();
      }
    } catch (e) {
      setState(() {
        _isProcessing = false;
      });
      
      HapticFeedback.heavyImpact();
    }
  }

  Future<void> _openGoogleMaps() async {
    HapticFeedback.mediumImpact();
    await NotificationService.openGoogleMaps(widget.latitude, widget.longitude);
  }

  @override
  Widget build(BuildContext context) {
    // Get screen dimensions
    final screenSize = MediaQuery.of(context).size;
    final isLandscape = screenSize.width > screenSize.height;
    
    return PopScope(
      canPop: false, // Cannot be dismissed
      child: Scaffold(
        backgroundColor: Colors.black.withOpacity(0.95),
        body: SafeArea(
          child: Container(
            width: double.infinity,
            height: double.infinity,
            padding: EdgeInsets.all(isLandscape ? 16.0 : 24.0),
            child: SingleChildScrollView(
              child: ConstrainedBox(
                constraints: BoxConstraints(
                  minHeight: screenSize.height - MediaQuery.of(context).padding.top - MediaQuery.of(context).padding.bottom,
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    // Emergency Alert Header
                    AnimatedBuilder(
                      animation: _pulseAnimation,
                      builder: (context, child) {
                        return Transform.scale(
                          scale: _pulseAnimation.value,
                          child: Container(
                            padding: EdgeInsets.all(isLandscape ? 16 : 24),
                            decoration: BoxDecoration(
                              gradient: LinearGradient(
                                colors: [Colors.red.shade500, Colors.red.shade700],
                                begin: Alignment.topLeft,
                                end: Alignment.bottomRight,
                              ),
                              shape: BoxShape.circle,
                              boxShadow: [
                                BoxShadow(
                                  color: Colors.red.withOpacity(0.6),
                                  blurRadius: 30,
                                  spreadRadius: 10,
                                ),
                              ],
                            ),
                            child: Icon(
                              Icons.warning_rounded,
                              size: isLandscape ? 40 : 60,
                              color: Colors.white,
                            ),
                          ),
                        );
                      },
                    ),
                    
                    SizedBox(height: isLandscape ? 16 : 24),
                    
                    // Title
                    Text(
                      '🚨 EMERGENCY ALERT',
                      style: TextStyle(
                        fontSize: isLandscape ? 20 : 28,
                        fontWeight: FontWeight.bold,
                        color: Colors.red,
                        letterSpacing: 1.5,
                      ),
                      textAlign: TextAlign.center,
                    ),
                    
                    SizedBox(height: isLandscape ? 4 : 8),
                    
                    Text(
                      'DROWNING EMERGENCY',
                      style: TextStyle(
                        fontSize: isLandscape ? 16 : 20,
                        fontWeight: FontWeight.w600,
                        color: Colors.white,
                        letterSpacing: 1,
                      ),
                      textAlign: TextAlign.center,
                    ),
                    
                    SizedBox(height: isLandscape ? 16 : 32),
                    
                    // Case Information Card
                    Container(
                      width: double.infinity,
                      padding: EdgeInsets.all(isLandscape ? 16 : 24),
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(20),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black.withOpacity(0.3),
                            blurRadius: 20,
                            offset: const Offset(0, 4),
                          ),
                        ],
                      ),
                      child: Column(
                        children: [
                          // Case ID
                          Row(
                            children: [
                              Container(
                                padding: const EdgeInsets.all(8),
                                decoration: BoxDecoration(
                                  color: Colors.blue.shade100,
                                  borderRadius: BorderRadius.circular(8),
                                ),
                                child: Icon(
                                  Icons.confirmation_number_rounded,
                                  color: Colors.blue.shade700,
                                  size: 20,
                                ),
                              ),
                              const SizedBox(width: 12),
                              Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  const Text(
                                    'Case ID',
                                    style: TextStyle(
                                      fontSize: 12,
                                      color: Colors.grey,
                                      fontWeight: FontWeight.w500,
                                    ),
                                  ),
                                  Text(
                                    widget.caseId,
                                    style: TextStyle(
                                      fontSize: isLandscape ? 16 : 18,
                                      fontWeight: FontWeight.bold,
                                      color: Colors.black87,
                                    ),
                                  ),
                                ],
                              ),
                            ],
                          ),
                          
                          SizedBox(height: isLandscape ? 12 : 20),
                          
                          // Location
                          Row(
                            children: [
                              Container(
                                padding: const EdgeInsets.all(8),
                                decoration: BoxDecoration(
                                  color: Colors.red.shade100,
                                  borderRadius: BorderRadius.circular(8),
                                ),
                                child: Icon(
                                  Icons.location_on_rounded,
                                  color: Colors.red.shade700,
                                  size: 20,
                                ),
                              ),
                              const SizedBox(width: 12),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    const Text(
                                      'Emergency Location',
                                      style: TextStyle(
                                        fontSize: 12,
                                        color: Colors.grey,
                                        fontWeight: FontWeight.w500,
                                      ),
                                    ),
                                    Text(
                                      'Jalgaon, Maharashtra',
                                      style: TextStyle(
                                        fontSize: isLandscape ? 14 : 16,
                                        fontWeight: FontWeight.bold,
                                        color: Colors.black87,
                                      ),
                                    ),
                                    Text(
                                      '${widget.latitude.toStringAsFixed(6)}, ${widget.longitude.toStringAsFixed(6)}',
                                      style: TextStyle(
                                        fontSize: isLandscape ? 10 : 12,
                                        fontFamily: 'monospace',
                                        color: Colors.grey.shade600,
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ],
                          ),
                          
                          SizedBox(height: isLandscape ? 12 : 20),
                          
                          // Google Maps Button
                          SizedBox(
                            width: double.infinity,
                            child: ElevatedButton.icon(
                              onPressed: _openGoogleMaps,
                              icon: const Icon(Icons.map_rounded, size: 20),
                              label: Text(
                                'OPEN IN GOOGLE MAPS',
                                style: TextStyle(
                                  fontSize: isLandscape ? 12 : 14,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              style: ElevatedButton.styleFrom(
                                backgroundColor: Colors.blue.shade600,
                                foregroundColor: Colors.white,
                                padding: EdgeInsets.symmetric(vertical: isLandscape ? 10 : 14),
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(12),
                                ),
                                elevation: 2,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                    
                    SizedBox(height: isLandscape ? 16 : 24),
                    
                    // Action Buttons
                    if (_isProcessing)
                      Container(
                        padding: EdgeInsets.all(isLandscape ? 16 : 32),
                        child: Column(
                          children: [
                            SizedBox(
                              width: isLandscape ? 40 : 60,
                              height: isLandscape ? 40 : 60,
                              child: CircularProgressIndicator(
                                color: Colors.white,
                                strokeWidth: 4,
                              ),
                            ),
                            SizedBox(height: isLandscape ? 12 : 20),
                            Text(
                              'Recording your response...',
                              style: TextStyle(
                                fontSize: isLandscape ? 14 : 16,
                                fontWeight: FontWeight.w600,
                                color: Colors.white,
                              ),
                            ),
                          ],
                        ),
                      )
                    else
                      Column(
                        children: [
                          // Accept Button
                          SizedBox(
                            width: double.infinity,
                            height: isLandscape ? 48 : 56,
                            child: ElevatedButton.icon(
                              onPressed: () => _handleAction('accepted'),
                              icon: Icon(Icons.check_circle_rounded, size: isLandscape ? 20 : 24),
                              label: Text(
                                'ACCEPT - I\'M RESPONDING',
                                style: TextStyle(
                                  fontSize: isLandscape ? 14 : 16,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              style: ElevatedButton.styleFrom(
                                backgroundColor: Colors.green.shade600,
                                foregroundColor: Colors.white,
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(16),
                                ),
                                elevation: 4,
                              ),
                            ),
                          ),
                          
                          SizedBox(height: isLandscape ? 8 : 12),
                          
                          // Complete Button
                          SizedBox(
                            width: double.infinity,
                            height: isLandscape ? 48 : 56,
                            child: ElevatedButton.icon(
                              onPressed: () => _handleAction('completed'),
                              icon: Icon(Icons.done_all_rounded, size: isLandscape ? 20 : 24),
                              label: Text(
                                'COMPLETED - PERSON SAVED',
                                style: TextStyle(
                                  fontSize: isLandscape ? 14 : 16,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              style: ElevatedButton.styleFrom(
                                backgroundColor: Colors.blue.shade600,
                                foregroundColor: Colors.white,
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(16),
                                ),
                                elevation: 4,
                              ),
                            ),
                          ),
                          
                          SizedBox(height: isLandscape ? 8 : 12),
                          
                          // Not Available Button
                          SizedBox(
                            width: double.infinity,
                            height: isLandscape ? 48 : 56,
                            child: ElevatedButton.icon(
                              onPressed: () => _handleAction('not_available'),
                              icon: Icon(Icons.cancel_rounded, size: isLandscape ? 20 : 24),
                              label: Text(
                                'NOT AVAILABLE',
                                style: TextStyle(
                                  fontSize: isLandscape ? 14 : 16,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              style: ElevatedButton.styleFrom(
                                backgroundColor: Colors.orange.shade600,
                                foregroundColor: Colors.white,
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(16),
                                ),
                                elevation: 4,
                              ),
                            ),
                          ),
                        ],
                      ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}