/**
 * Alert Card Component - Shows latest alert and stats
 */
import React from 'react';
import { AlertTriangle, CheckCircle, Clock, MapPin, Activity, TrendingUp } from 'lucide-react';

const AlertCard = ({ latestAlert, stats, isLoading }) => {
  if (isLoading) {
    return (
      <div className="bg-white rounded-2xl shadow-soft p-6 animate-fade-in">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded-xl w-1/3 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded-xl w-1/2 mb-2"></div>
          <div className="h-4 bg-gray-200 rounded-xl w-2/3"></div>
        </div>
      </div>
    );
  }

  const isDanger = latestAlert?.danger;

  return (
    <div className="space-y-6">
      {/* Latest Alert Card */}
      <div className="bg-white rounded-2xl shadow-soft p-6 animate-slide-up">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-800">Latest Alert</h2>
          <div className={`px-3 py-1 rounded-full text-xs font-medium ${
            isDanger 
              ? 'bg-danger-100 text-danger-700' 
              : latestAlert 
                ? 'bg-success-100 text-success-700'
                : 'bg-gray-100 text-gray-600'
          }`}>
            {!latestAlert ? 'No Data' : isDanger ? 'DANGER' : 'SAFE'}
          </div>
        </div>

        {!latestAlert ? (
          <div className="text-center py-8">
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Activity className="w-8 h-8 text-gray-400" />
            </div>
            <p className="text-gray-500 mb-2">No alerts received yet</p>
            <p className="text-sm text-gray-400">Waiting for device data...</p>
          </div>
        ) : (
          <div className="space-y-4">
            {/* Status Icon and Message */}
            <div className="flex items-center space-x-3">
              {isDanger ? (
                <div className="w-12 h-12 bg-danger-100 rounded-xl flex items-center justify-center">
                  <AlertTriangle className="w-6 h-6 text-danger-600" />
                </div>
              ) : (
                <div className="w-12 h-12 bg-success-100 rounded-xl flex items-center justify-center">
                  <CheckCircle className="w-6 h-6 text-success-600" />
                </div>
              )}
              <div>
                <h3 className={`font-semibold ${isDanger ? 'text-danger-700' : 'text-success-700'}`}>
                  {isDanger ? 'Emergency Alert Active' : 'System Operating Normally'}
                </h3>
                <p className="text-sm text-gray-500">Device: {latestAlert.device_id}</p>
              </div>
            </div>

            {/* Location and Time */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t border-gray-100">
              <div className="flex items-center space-x-2">
                <MapPin className="w-4 h-4 text-gray-400" />
                <div>
                  <p className="text-xs text-gray-500">Location</p>
                  <p className="text-sm font-medium text-gray-700">
                    {latestAlert.latitude.toFixed(4)}, {latestAlert.longitude.toFixed(4)}
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <Clock className="w-4 h-4 text-gray-400" />
                <div>
                  <p className="text-xs text-gray-500">Timestamp</p>
                  <p className="text-sm font-medium text-gray-700">
                    {new Date(latestAlert.timestamp).toLocaleString()}
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-white rounded-2xl shadow-soft p-4 animate-slide-up">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Total Alerts</p>
              <p className="text-2xl font-bold text-gray-800">{stats?.total || 0}</p>
            </div>
            <div className="w-10 h-10 bg-primary-100 rounded-xl flex items-center justify-center">
              <Activity className="w-5 h-5 text-primary-600" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-soft p-4 animate-slide-up">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500">Danger Alerts</p>
              <p className="text-2xl font-bold text-danger-600">{stats?.danger || 0}</p>
            </div>
            <div className="w-10 h-10 bg-danger-100 rounded-xl flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-danger-600" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AlertCard;