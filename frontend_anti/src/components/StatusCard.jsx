/**
 * Status Card Component - Shows latest alert status
 */
import React from 'react';
import { AlertTriangle, CheckCircle, Clock, MapPin } from 'lucide-react';

const StatusCard = ({ latestAlert, isLoading }) => {
  if (isLoading) {
    return (
      <div className="bg-tesla-gray rounded-xl p-6 border border-gray-700">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-600 rounded w-1/3 mb-4"></div>
          <div className="h-4 bg-gray-600 rounded w-1/2 mb-2"></div>
          <div className="h-4 bg-gray-600 rounded w-2/3"></div>
        </div>
      </div>
    );
  }

  if (!latestAlert) {
    return (
      <div className="bg-tesla-gray rounded-xl p-6 border border-gray-700">
        <div className="flex items-center space-x-3 mb-4">
          <CheckCircle className="w-8 h-8 text-tesla-green" />
          <h2 className="text-xl font-semibold text-white">System Status</h2>
        </div>
        <p className="text-gray-300">No alerts received yet</p>
        <p className="text-sm text-gray-400 mt-2">Waiting for device data...</p>
      </div>
    );
  }

  const isDanger = latestAlert.danger;
  const statusColor = isDanger ? 'text-tesla-red' : 'text-tesla-green';
  const bgColor = isDanger ? 'bg-red-900/20' : 'bg-green-900/20';
  const borderColor = isDanger ? 'border-tesla-red' : 'border-tesla-green';

  return (
    <div className={`${bgColor} rounded-xl p-6 border ${borderColor}`}>
      <div className="flex items-center space-x-3 mb-4">
        {isDanger ? (
          <AlertTriangle className="w-8 h-8 text-tesla-red" />
        ) : (
          <CheckCircle className="w-8 h-8 text-tesla-green" />
        )}
        <h2 className="text-xl font-semibold text-white">
          {isDanger ? 'DANGER ALERT' : 'Safe Status'}
        </h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <div className="flex items-center space-x-2 mb-2">
            <MapPin className="w-4 h-4 text-gray-400" />
            <span className="text-sm text-gray-400">Location</span>
          </div>
          <p className="text-white font-mono">
            {latestAlert.latitude.toFixed(6)}, {latestAlert.longitude.toFixed(6)}
          </p>
        </div>

        <div>
          <div className="flex items-center space-x-2 mb-2">
            <Clock className="w-4 h-4 text-gray-400" />
            <span className="text-sm text-gray-400">Last Update</span>
          </div>
          <p className="text-white">
            {new Date(latestAlert.timestamp).toLocaleString()}
          </p>
        </div>
      </div>

      <div className="mt-4 pt-4 border-t border-gray-600">
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-400">Device ID</span>
          <span className="text-white font-mono">{latestAlert.device_id}</span>
        </div>
      </div>
    </div>
  );
};

export default StatusCard;