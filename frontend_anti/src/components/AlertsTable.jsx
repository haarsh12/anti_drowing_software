/**
 * Alerts Table Component - Clean table showing all alerts
 */
import React from 'react';
import { AlertTriangle, CheckCircle, Clock, MapPin, Smartphone } from 'lucide-react';

const AlertsTable = ({ alerts, isLoading }) => {
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
                Timestamp
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {alerts.map((alert, index) => (
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
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AlertsTable;