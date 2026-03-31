/**
 * Alert Map Component - Shows alert location on map
 */
import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';

// Fix for default markers in react-leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Custom danger marker icon
const dangerIcon = new L.Icon({
  iconUrl: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDJMMTMuMDkgOC4yNkwyMCA5TDEzLjA5IDE1Ljc0TDEyIDIyTDEwLjkxIDE1Ljc0TDQgOUwxMC45MSA4LjI2TDEyIDJaIiBmaWxsPSIjRUY0NDQ0Ii8+CjwvcGF0aD4KPC9zdmc+',
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
});

// Custom safe marker icon
const safeIcon = new L.Icon({
  iconUrl: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDJMMTMuMDkgOC4yNkwyMCA5TDEzLjA5IDE1Ljc0TDEyIDIyTDEwLjkxIDE1Ljc0TDQgOUwxMC45MSA4LjI2TDEyIDJaIiBmaWxsPSIjMTBCOTgxIi8+CjwvcGF0aD4KPC9zdmc+',
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
});

const AlertMap = ({ alerts, latestAlert, isLoading }) => {
  // Default center (Pune, India as per ESP32 example)
  const defaultCenter = [18.52, 73.85];
  const mapCenter = latestAlert ? [latestAlert.latitude, latestAlert.longitude] : defaultCenter;

  if (isLoading) {
    return (
      <div className="bg-tesla-gray rounded-xl p-6 border border-gray-700 h-96 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-tesla-blue mx-auto mb-4"></div>
          <p className="text-gray-400">Loading map...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-tesla-gray rounded-xl border border-gray-700 overflow-hidden">
      <div className="p-4 border-b border-gray-700">
        <h3 className="text-lg font-semibold text-white">Alert Locations</h3>
        <p className="text-sm text-gray-400">
          {alerts?.length > 0 ? `Showing ${alerts.length} alerts` : 'No alerts to display'}
        </p>
      </div>
      
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
              <Popup>
                <div className="text-black">
                  <h4 className="font-semibold mb-2">
                    {alert.danger ? '⚠️ DANGER ALERT' : '✅ Safe Status'}
                  </h4>
                  <p><strong>Device:</strong> {alert.device_id}</p>
                  <p><strong>Location:</strong> {alert.latitude.toFixed(6)}, {alert.longitude.toFixed(6)}</p>
                  <p><strong>Time:</strong> {new Date(alert.timestamp).toLocaleString()}</p>
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
};

export default AlertMap;