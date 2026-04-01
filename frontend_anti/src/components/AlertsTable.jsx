/**
 * Alerts Table Component - Clean table showing all alerts with guard responses and actions
 */
import React, { useState } from 'react';
import { AlertTriangle, CheckCircle, Clock, MapPin, Smartphone, Eye, Map, Users, ExternalLink } from 'lucide-react';

const AlertsTable = ({ alerts, isLoading }) => {
  const [selectedCase, setSelectedCase] = useState(null);

  const openGoogleMaps = (latitude, longitude) => {
    const url = `https://www.google.com/maps/search/?api=1&query=${latitude},${longitude}`;
    window.open(url, '_blank');
  };

  const viewCaseDetails = (alert) => {
    setSelectedCase(alert);
  };

  const closeCaseDetails = () => {
    setSelectedCase(null);
  };

  // Mock guard responses for demonstration
  const getGuardResponses = (alertId) => {
    return [
      {
        guard_name: 'Rajesh Kumar',
        action: 'accepted',
        timestamp: new Date(Date.now() - 2 * 60 * 1000),
        phone: '+91 98765 43210',
      },
      {
        guard_name: 'Priya Sharma',
        action: 'not_available',
        timestamp: new Date(Date.now() - 1 * 60 * 1000),
        phone: '+91 87654 32109',
      },
      {
        guard_name: 'Amit Patel',
        action: 'completed',
        timestamp: new Date(Date.now() - 30 * 1000),
        phone: '+91 76543 21098',
      },
    ];
  };

  const getActionColor = (action) => {
    switch (action.toLowerCase()) {
      case 'accepted':
        return 'text-green-600 bg-green-100';
      case 'completed':
        return 'text-blue-600 bg-blue-100';
      case 'not_available':
        return 'text-orange-600 bg-orange-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  if (isLoading) {
    return (
      <div className="bg-white rounded-2xl shadow-soft animate-fade-in">
        <div className="px-6 py-4 border-b border-gray-100">
          <h3 className="text-lg font-semibold text-gray-800">Recent Alerts</h3>
        </div>
        <div className="p-6">
          <div className="animate-pulse space-y-4">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="flex space-x-4">
                <div className="h-4 bg-gray-200 rounded-xl w-1/4"></div>
                <div className="h-4 bg-gray-200 rounded-xl w-1/4"></div>
                <div className="h-4 bg-gray-200 rounded-xl w-1/4"></div>
                <div className="h-4 bg-gray-200 rounded-xl w-1/4"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (!alerts || alerts.length === 0) {
    return (
      <div className="bg-white rounded-2xl shadow-soft animate-slide-up">
        <div className="px-6 py-4 border-b border-gray-100">
          <h3 className="text-lg font-semibold text-gray-800">Recent Alerts</h3>
        </div>
        <div className="p-12 text-center">
          <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Clock className="w-8 h-8 text-gray-400" />
          </div>
          <p className="text-gray-500 mb-2">No alerts available</p>
          <p className="text-sm text-gray-400">Alerts will appear here when received from devices</p>
        </div>
      </div>
    );
  }

  return (
    <>
      <div className="bg-white rounded-2xl shadow-soft animate-slide-up">
        {/* Table Header */}
        <div className="px-6 py-4 border-b border-gray-100">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-gray-800">Recent Alerts</h3>
              <p className="text-sm text-gray-500">Total: {alerts.length} alerts</p>
            </div>
            <div className="flex items-center space-x-2 text-xs text-gray-500">
              <div className="w-2 h-2 bg-success-500 rounded-full animate-pulse-soft"></div>
              <span>Live updates</span>
            </div>
          </div>
        </div>
        
        {/* Table */}
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-100 bg-gray-50">
                <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Device ID
                </th>
                <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Location
                </th>
                <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Guard Responses
                </th>
                <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Timestamp
                </th>
                <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {alerts.map((alert, index) => {
                const guardResponses = getGuardResponses(alert.id);
                const acceptedGuards = guardResponses.filter(g => g.action === 'accepted').length;
                const completedGuards = guardResponses.filter(g => g.action === 'completed').length;
                
                return (
                  <tr 
                    key={alert.id} 
                    className={`hover:bg-gray-50 transition-colors duration-150 ${
                      alert.danger ? 'bg-danger-50 hover:bg-danger-100' : ''
                    }`}
                  >
                    {/* Status Column */}
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center space-x-3">
                        {alert.danger ? (
                          <>
                            <div className="w-8 h-8 bg-danger-100 rounded-full flex items-center justify-center">
                              <AlertTriangle className="w-4 h-4 text-danger-600" />
                            </div>
                            <div>
                              <span className="text-sm font-medium text-danger-700">DANGER</span>
                              <p className="text-xs text-danger-600">Emergency Alert</p>
                            </div>
                          </>
                        ) : (
                          <>
                            <div className="w-8 h-8 bg-success-100 rounded-full flex items-center justify-center">
                              <CheckCircle className="w-4 h-4 text-success-600" />
                            </div>
                            <div>
                              <span className="text-sm font-medium text-success-700">SAFE</span>
                              <p className="text-xs text-success-600">Normal Status</p>
                            </div>
                          </>
                        )}
                      </div>
                    </td>
                    
                    {/* Device ID Column */}
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center space-x-2">
                        <Smartphone className="w-4 h-4 text-gray-400" />
                        <span className="text-sm font-medium text-gray-900 font-mono">
                          {alert.device_id}
                        </span>
                      </div>
                    </td>
                    
                    {/* Location Column */}
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center space-x-2">
                        <MapPin className="w-4 h-4 text-gray-400" />
                        <span className="text-sm text-gray-700 font-mono">
                          {alert.latitude.toFixed(4)}, {alert.longitude.toFixed(4)}
                        </span>
                      </div>
                    </td>
                    
                    {/* Guard Responses Column */}
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center space-x-2">
                        <Users className="w-4 h-4 text-gray-400" />
                        <div className="text-sm">
                          <div className="flex space-x-2">
                            {acceptedGuards > 0 && (
                              <span className="px-2 py-1 text-xs font-medium text-green-600 bg-green-100 rounded-full">
                                {acceptedGuards} Accepted
                              </span>
                            )}
                            {completedGuards > 0 && (
                              <span className="px-2 py-1 text-xs font-medium text-blue-600 bg-blue-100 rounded-full">
                                {completedGuards} Completed
                              </span>
                            )}
                            {acceptedGuards === 0 && completedGuards === 0 && (
                              <span className="px-2 py-1 text-xs font-medium text-gray-600 bg-gray-100 rounded-full">
                                No Response
                              </span>
                            )}
                          </div>
                          <div className="text-xs text-gray-500 mt-1">
                            {guardResponses.length} guards notified
                          </div>
                        </div>
                      </div>
                    </td>
                    
                    {/* Timestamp Column */}
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center space-x-2">
                        <Clock className="w-4 h-4 text-gray-400" />
                        <div className="text-sm">
                          <div className="text-gray-900 font-medium">
                            {new Date(alert.timestamp).toLocaleDateString()}
                          </div>
                          <div className="text-gray-500 text-xs">
                            {new Date(alert.timestamp).toLocaleTimeString()}
                          </div>
                        </div>
                      </div>
                    </td>
                    
                    {/* Actions Column */}
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center space-x-2">
                        <button
                          onClick={() => viewCaseDetails(alert)}
                          className="inline-flex items-center px-3 py-1.5 text-xs font-medium text-blue-600 bg-blue-100 rounded-lg hover:bg-blue-200 transition-colors duration-150"
                        >
                          <Eye className="w-3 h-3 mr-1" />
                          View Details
                        </button>
                        <button
                          onClick={() => openGoogleMaps(alert.latitude, alert.longitude)}
                          className="inline-flex items-center px-3 py-1.5 text-xs font-medium text-green-600 bg-green-100 rounded-lg hover:bg-green-200 transition-colors duration-150"
                        >
                          <Map className="w-3 h-3 mr-1" />
                          View Maps
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Case Details Modal */}
      {selectedCase && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            {/* Modal Header */}
            <div className="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-gray-800">Case Details</h3>
                <p className="text-sm text-gray-500">CASE{selectedCase.id.toString().padStart(3, '0')}</p>
              </div>
              <button
                onClick={closeCaseDetails}
                className="text-gray-400 hover:text-gray-600 transition-colors duration-150"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Modal Content */}
            <div className="px-6 py-6 space-y-6">
              {/* Alert Status */}
              <div className="flex items-center space-x-4">
                {selectedCase.danger ? (
                  <div className="w-12 h-12 bg-danger-100 rounded-full flex items-center justify-center">
                    <AlertTriangle className="w-6 h-6 text-danger-600" />
                  </div>
                ) : (
                  <div className="w-12 h-12 bg-success-100 rounded-full flex items-center justify-center">
                    <CheckCircle className="w-6 h-6 text-success-600" />
                  </div>
                )}
                <div>
                  <h4 className={`text-xl font-bold ${selectedCase.danger ? 'text-danger-700' : 'text-success-700'}`}>
                    {selectedCase.danger ? 'EMERGENCY ALERT' : 'NORMAL STATUS'}
                  </h4>
                  <p className="text-gray-600">
                    {selectedCase.danger ? 'Drowning emergency detected' : 'Device operating normally'}
                  </p>
                </div>
              </div>

              {/* Device Information */}
              <div className="bg-gray-50 rounded-xl p-4">
                <h5 className="font-semibold text-gray-800 mb-3">Device Information</h5>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-500">Device ID</p>
                    <p className="font-mono font-medium">{selectedCase.device_id}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">Timestamp</p>
                    <p className="font-medium">{new Date(selectedCase.timestamp).toLocaleString()}</p>
                  </div>
                </div>
              </div>

              {/* Location Information */}
              <div className="bg-blue-50 rounded-xl p-4">
                <h5 className="font-semibold text-gray-800 mb-3">Location Information</h5>
                <div className="space-y-3">
                  <div>
                    <p className="text-sm text-gray-500">Coordinates</p>
                    <p className="font-mono font-medium">
                      {selectedCase.latitude.toFixed(6)}, {selectedCase.longitude.toFixed(6)}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">Location</p>
                    <p className="font-medium">Jalgaon, Maharashtra, India</p>
                  </div>
                  <button
                    onClick={() => openGoogleMaps(selectedCase.latitude, selectedCase.longitude)}
                    className="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors duration-150"
                  >
                    <ExternalLink className="w-4 h-4 mr-2" />
                    Open in Google Maps
                  </button>
                </div>
              </div>

              {/* Guard Responses */}
              <div className="bg-green-50 rounded-xl p-4">
                <h5 className="font-semibold text-gray-800 mb-3">Guard Responses</h5>
                <div className="space-y-3">
                  {getGuardResponses(selectedCase.id).map((response, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-white rounded-lg">
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center">
                          <Users className="w-4 h-4 text-gray-600" />
                        </div>
                        <div>
                          <p className="font-medium text-gray-900">{response.guard_name}</p>
                          <p className="text-sm text-gray-500">{response.phone}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <span className={`px-3 py-1 text-xs font-medium rounded-full ${getActionColor(response.action)}`}>
                          {response.action.toUpperCase().replace('_', ' ')}
                        </span>
                        <p className="text-xs text-gray-500 mt-1">
                          {response.timestamp.toLocaleTimeString()}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default AlertsTable;