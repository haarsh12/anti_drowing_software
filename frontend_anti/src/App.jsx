/**
 * Main App Component - IoT Alert Dashboard
 */
import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import StatusCard from './components/StatusCard';
import AlertMap from './components/AlertMap';
import AlertsTable from './components/AlertsTable';
import { alertsAPI } from './services/api';

function App() {
  const [alerts, setAlerts] = useState([]);
  const [latestAlert, setLatestAlert] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isConnected, setIsConnected] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(null);

  // Fetch all alerts
  const fetchAlerts = async () => {
    try {
      const response = await alertsAPI.getAllAlerts();
      setAlerts(response.alerts || []);
      setIsConnected(true);
      setLastUpdate(new Date());
    } catch (error) {
      console.error('Failed to fetch alerts:', error);
      setIsConnected(false);
    }
  };

  // Fetch latest alert
  const fetchLatestAlert = async () => {
    try {
      const latest = await alertsAPI.getLatestAlert();
      setLatestAlert(latest);
      setIsConnected(true);
    } catch (error) {
      console.error('Failed to fetch latest alert:', error);
      setIsConnected(false);
    }
  };

  // Initial data load
  useEffect(() => {
    const loadInitialData = async () => {
      setIsLoading(true);
      try {
        await Promise.all([fetchAlerts(), fetchLatestAlert()]);
      } catch (error) {
        console.error('Failed to load initial data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadInitialData();
  }, []);

  // Auto-refresh every 5 seconds
  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        await Promise.all([fetchAlerts(), fetchLatestAlert()]);
      } catch (error) {
        console.error('Auto-refresh failed:', error);
      }
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-tesla-dark font-tesla">
      <Header 
        isConnected={isConnected} 
        lastUpdate={lastUpdate} 
      />
      
      <main className="container mx-auto px-6 py-8 max-w-7xl">
        {/* Status Overview */}
        <div className="mb-8">
          <StatusCard 
            latestAlert={latestAlert} 
            isLoading={isLoading} 
          />
        </div>

        {/* Map and Table Grid */}
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-8 mb-8">
          <AlertMap 
            alerts={alerts} 
            latestAlert={latestAlert} 
            isLoading={isLoading} 
          />
          
          <div className="xl:col-span-1">
            <AlertsTable 
              alerts={alerts.slice(0, 10)} // Show latest 10 alerts
              isLoading={isLoading} 
            />
          </div>
        </div>

        {/* Footer */}
        <footer className="text-center text-gray-500 text-sm py-4 border-t border-gray-700">
          <p>IoT Alert Dashboard v1.0.0 - Emergency Monitoring System</p>
          <p className="mt-1">
            Auto-refresh: 5s | 
            Status: <span className={isConnected ? 'text-tesla-green' : 'text-tesla-red'}>
              {isConnected ? 'Online' : 'Offline'}
            </span>
          </p>
        </footer>
      </main>
    </div>
  );
}

export default App;