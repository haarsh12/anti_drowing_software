/**
 * Map View Component - Interactive map showing alert locations
 */
import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import { MapPin, Clock, Smartphone } from 'lucide-react';

// Fix for default markers in react-leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Custom danger marker icon (red)
const dangerIcon = new L.Icon({
  iconUrl: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDJMMTMuMDkgOC4yNkwyMCA5TDEzLjA5IDE1Ljc0TDEyIDIyTDEwLjkxIDE1Ljc0TDQgOUwxMC45MSA4LjI2TDEyIDJaIiBmaWxsPSIjRUY0NDQ0Ii8+CjwvcGF0aD4KPC9zdmc+',
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
});

// Custom safe marker icon (green)
const safeIcon = new L.Icon({
  iconUrl: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDJMMTMuMDkgOC4yNkwyMCA5TDEzLjA5IDE1Ljc0TDEyIDIyTDEwLjkxIDE1Ljc0TDQgOUwxMC45MSA4LjI2TDEyIDJaIiBmaWxsPSIjMjJDNTVFIi8+CjwvcGF0aD4KPC9zdmc+',
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
});

const MapView = ({ alerts, latestAlert, isLoading }) => {
  // Default center (Pune, India as per ESP32 example)
  const defaultCenter = [18.52, 73.85];
  const mapCenter = latestAlert ? [latestAlert.latitude, latestAlert.longitude] : defaultCenter;

  if (isLoading) {
    return (
      <div className="bg-white rounded-2xl shadow-soft p-6 h-96 flex items-center justify-center animate-fade-in">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-primary-200 border-t-primary-500 rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-500">Loading map...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl shadow-soft overflow-hidden animate-slide-up">
      {/* Map Header */}
      <div className="px-6 py-4 border-b border-gray-100">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center">
              <MapPin className="w-4 h-4 text-primary-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-800">Alert Locations</h3>
              <p className="text-sm text-gray-500">
                {alerts?.length > 0 ? `Showing ${alerts.length} alerts` : 'No alerts to display'}
              </p>
            </div>
          </div>
          
          {/* Map Legend */}
          <div className="flex items-center space-x-4 text-xs">
            <div className="flex items-center space-x-1">
              <div className="w-3 h-3 bg-danger-500 rounded-full"></div>
              <span className="text-gray-600">Danger</span>
            </div>
            <div className="flex items-center space-x-1">
              <div className="w-3 h-3 bg-success-500 rounded-full"></div>
              <span className="text-gray-600">Safe</span>
            </div>
          </div>
        </div>
      </div>
      
      {/* Map Container */}
      <div className="h-96">
        <MapContainer
          center={mapCenter}
          zoom={13}
          style={{ height: '100%', width: '100%' }}
          className="z-0"
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />
          
          {alerts && alerts.map((alert) => (
            <Marker
              key={alert.id}
              position={[alert.latitude, alert.longitude]}
              icon={alert.danger ? dangerIcon : safeIcon}
            >
              <Popup className="custom-popup">
                <div className="p-2 min-w-[200px]">
                  {/* Status Header */}
                  <div className={`flex items-center space-x-2 mb-3 pb-2 border-b ${
                    alert.danger ? 'border-red-200' : 'border-green-200'
                  }`}>
                    {alert.danger ? (
                      <div className="w-6 h-6 bg-red-100 rounded-full flex items-center justify-center">
                        <span className="text-red-600 text-xs">⚠</span>
                      </div>
                    ) : (
                      <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center">
                        <span className="text-green-600 text-xs">✓</span>
                      </div>
                    )}
                    <span className={`font-semibold text-sm ${
                      alert.danger ? 'text-red-700' : 'text-green-700'
                    }`}>
                      {alert.danger ? 'DANGER ALERT' : 'Safe Status'}
                    </span>
                  </div>

                  {/* Alert Details */}
                  <div className="space-y-2 text-sm text-gray-700">
                    <div className="flex items-center space-x-2">
                      <Smartphone className="w-3 h-3 text-gray-400" />
                      <span className="font-medium">Device:</span>
                      <span className="font-mono text-xs">{alert.device_id}</span>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      <MapPin className="w-3 h-3 text-gray-400" />
                      <span className="font-medium">Location:</span>
                      <span className="font-mono text-xs">
                        {alert.latitude.toFixed(4)}, {alert.longitude.toFixed(4)}
                      </span>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      <Clock className="w-3 h-3 text-gray-400" />
                      <span className="font-medium">Time:</span>
                      <span className="text-xs">
                        {new Date(alert.timestamp).toLocaleString()}
                      </span>
                    </div>
                  </div>
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
};

export default MapView;