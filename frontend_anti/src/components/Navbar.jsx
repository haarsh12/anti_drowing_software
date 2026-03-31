/**
 * Navbar Component - Top navigation with search and profile
 */
import React from 'react';
import { Search, Bell, User, Wifi, WifiOff } from 'lucide-react';

const Navbar = ({ isConnected, lastUpdate }) => {
  return (
    <nav className="bg-white shadow-soft rounded-2xl mx-6 mt-6 px-6 py-4 animate-fade-in">
      <div className="flex items-center justify-between">
        {/* Logo and Title */}
        <div className="flex items-center space-x-4">
          <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl flex items-center justify-center shadow-soft">
            <Bell className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-gray-800">IoT Alert Dashboard</h1>
            <p className="text-sm text-gray-500">Real-time monitoring system</p>
          </div>
        </div>

        {/* Search Bar */}
        <div className="flex-1 max-w-md mx-8">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search alerts..."
              className="w-full pl-10 pr-4 py-2 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200"
            />
          </div>
        </div>

        {/* Status and Profile */}
        <div className="flex items-center space-x-4">
          {/* Connection Status */}
          <div className="flex items-center space-x-2 px-3 py-2 bg-gray-50 rounded-xl">
            {isConnected ? (
              <Wifi className="w-4 h-4 text-success-500" />
            ) : (
              <WifiOff className="w-4 h-4 text-danger-500" />
            )}
            <span className={`text-sm font-medium ${isConnected ? 'text-success-600' : 'text-danger-600'}`}>
              {isConnected ? 'Connected' : 'Disconnected'}
            </span>
          </div>

          {/* Last Update */}
          {lastUpdate && (
            <div className="text-xs text-gray-500">
              Last update: {new Date(lastUpdate).toLocaleTimeString()}
            </div>
          )}

          {/* Profile */}
          <div className="w-8 h-8 bg-gradient-to-br from-gray-400 to-gray-500 rounded-full flex items-center justify-center cursor-pointer hover:shadow-soft transition-all duration-200">
            <User className="w-4 h-4 text-white" />
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;