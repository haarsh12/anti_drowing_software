/**
 * Header Component - Top navigation bar
 */
import React from 'react';
import { Shield, Wifi, WifiOff } from 'lucide-react';

const Header = ({ isConnected, lastUpdate }) => {
  return (
    <header className="bg-tesla-gray border-b border-gray-700 px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <Shield className="w-8 h-8 text-tesla-blue" />
          <div>
            <h1 className="text-xl font-bold text-white">IoT Alert Dashboard</h1>
            <p className="text-sm text-gray-400">Emergency Monitoring System</p>
          </div>
        </div>
        
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            {isConnected ? (
              <Wifi className="w-5 h-5 text-tesla-green" />
            ) : (
              <WifiOff className="w-5 h-5 text-tesla-red" />
            )}
            <span className={`text-sm ${isConnected ? 'text-tesla-green' : 'text-tesla-red'}`}>
              {isConnected ? 'Connected' : 'Disconnected'}
            </span>
          </div>
          
          {lastUpdate && (
            <div className="text-sm text-gray-400">
              Last update: {new Date(lastUpdate).toLocaleTimeString()}
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;