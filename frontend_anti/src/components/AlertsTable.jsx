/**
 * Alerts Table Component - Shows all alerts in a table format
 */
import React from 'react';
import { AlertTriangle, CheckCircle, Clock, MapPin, Smartphone } from 'lucide-react';

const AlertsTable = ({ alerts, isLoading }) => {
  if (isLoading) {
    return (
      <div className="bg-tesla-gray rounded-xl border border-gray-700">
        <div className="p-4 border-b border-gray-700">
          <h3 className="text-lg font-semibold text-white">Recent Alerts</h3>
        </div>
        <div className="p-6">
          <div className="animate-pulse space-y-4">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="flex space-x-4">
                <div className="h-4 bg-gray-600 rounded w-1/4"></div>
                <div className="h-4 bg-gray-600 rounded w-1/4"></div>
                <div className="h-4 bg-gray-600 rounded w-1/4"></div>
                <div className="h-4 bg-gray-600 rounded w-1/4"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (!alerts || alerts.length === 0) {
    return (
      <div className="bg-tesla-gray rounded-xl border border-gray-700">
        <div className="p-4 border-b border-gray-700">
          <h3 className="text-lg font-semibold text-white">Recent Alerts</h3>
        </div>
        <div className="p-6 text-center">
          <div className="text-gray-400 mb-4">
            <Clock className="w-12 h-12 mx-auto mb-2 opacity-50" />
            <p>No alerts available</p>
            <p className="text-sm">Alerts will appear here when received from devices</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-tesla-gray rounded-xl border border-gray-700">
      <div className="p-4 border-b border-gray-700">
        <h3 className="text-lg font-semibold text-white">Recent Alerts</h3>
        <p className="text-sm text-gray-400">Total: {alerts.length} alerts</p>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-700">
              <th className="text-left p-4 text-sm font-medium text-gray-400">Status</th>
              <th className="text-left p-4 text-sm font-medium text-gray-400">Device</th>
              <th className="text-left p-4 text-sm font-medium text-gray-400">Location</th>
              <th className="text-left p-4 text-sm font-medium text-gray-400">Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {alerts.map((alert, index) => (
              <tr 
                key={alert.id} 
                className={`border-b border-gray-700 hover:bg-gray-800/50 transition-colors ${
                  alert.danger ? 'bg-red-900/10' : ''
                }`}
              >
                <td className="p-4">
                  <div className="flex items-center space-x-2">
                    {alert.danger ? (
                      <>
                        <AlertTriangle className="w-5 h-5 text-tesla-red" />
                        <span className="text-tesla-red font-medium">DANGER</span>
                      </>
                    ) : (
                      <>
                        <CheckCircle className="w-5 h-5 text-tesla-green" />
                        <span className="text-tesla-green font-medium">SAFE</span>
                      </>
                    )}
                  </div>
                </td>
                
                <td className="p-4">
                  <div className="flex items-center space-x-2">
                    <Smartphone className="w-4 h-4 text-gray-400" />
                    <span className="text-white font-mono text-sm">{alert.device_id}</span>
                  </div>
                </td>
                
                <td className="p-4">
                  <div className="flex items-center space-x-2">
                    <MapPin className="w-4 h-4 text-gray-400" />
                    <span className="text-white font-mono text-sm">
                      {alert.latitude.toFixed(4)}, {alert.longitude.toFixed(4)}
                    </span>
                  </div>
                </td>
                
                <td className="p-4">
                  <div className="flex items-center space-x-2">
                    <Clock className="w-4 h-4 text-gray-400" />
                    <div className="text-sm">
                      <div className="text-white">
                        {new Date(alert.timestamp).toLocaleDateString()}
                      </div>
                      <div className="text-gray-400">
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