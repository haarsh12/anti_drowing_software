/**
 * Dashboard Page - Main dashboard layout
 */
import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import AlertCard from '../components/AlertCard';
import MapView from '../components/MapView';
import AlertsTable from '../components/AlertsTable';
import { alertsAPI } from '../services/api';

const Dashboard = () => {
  const [alerts, setAlerts] = useState([]);
  const [latestAlert, setLatestAlert] = useState(null);
  const [stats, setStats] = useState({ total: 0, danger: 0 });
  const [isLoading, setIsLoading] = useState(true);
  const [isConnected, setIsConnected] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(null);

  // Calculate stats from alerts
  const calculateStats = (alertsData) => {
    const total = alertsData.length;
    const danger = alertsData.filter(alert => alert.danger).length;
    return { total, danger };
  };

  // Fetch all alerts
  const fetchAlerts = async () => {
    try {
      const response = await alertsAPI.getAllAlerts();
      const alertsData = response.alerts || [];
      setAlerts(alertsData);
      setStats(calculateStats(alertsData));
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
    <div className="min-h-screen bg-gray-100">
      {/* Navigation */}
      <Navbar 
        isConnected={isConnected} 
        lastUpdate={lastUpdate} 
      />
      
      {/* Main Content */}
      <main className="px-6 py-6">
        <div className="max-w-7xl mx-auto">
          {/* Top Section - Alert Card and Map */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
            {/* Left Side - Alert Card and Stats */}
            <div className="lg:col-span-1">
              <AlertCard 
                latestAlert={latestAlert} 
                stats={stats}
                isLoading={isLoading} 
              />
            </div>

            {/* Right Side - Map */}
            <div className="lg:col-span-2">
              <MapView 
                alerts={alerts} 
                latestAlert={latestAlert} 
                isLoading={isLoading} 
              />
            </div>
          </div>

          {/* Bottom Section - Alerts Table */}
          <div className="mb-6">
            <AlertsTable 
              alerts={alerts} 
              isLoading={isLoading} 
            />
          </div>

          {/* Footer */}
          <footer className="text-center text-gray-500 text-sm py-6">
            <div className="bg-white rounded-2xl shadow-soft px-6 py-4">
              <p className="mb-2">IoT Alert Dashboard v1.0.0 - Real-time Emergency Monitoring</p>
              <div className="flex items-center justify-center space-x-4 text-xs">
                <span>Auto-refresh: 5s</span>
                <span>•</span>
                <span className={`flex items-center space-x-1 ${isConnected ? 'text-success-600' : 'text-danger-600'}`}>
                  <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-success-500' : 'bg-danger-500'} ${isConnected ? 'animate-pulse-soft' : ''}`}></div>
                  <span>{isConnected ? 'Online' : 'Offline'}</span>
                </span>
                <span>•</span>
                <span>Total Alerts: {stats.total}</span>
              </div>
            </div>
          </footer>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;