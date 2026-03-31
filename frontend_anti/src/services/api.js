/**
 * API service for communicating with the backend
 */
import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API endpoints
export const alertsAPI = {
  // Get all alerts
  getAllAlerts: async () => {
    try {
      const response = await api.get('/alerts');
      return response.data;
    } catch (error) {
      console.error('Error fetching alerts:', error);
      throw error;
    }
  },

  // Get latest alert
  getLatestAlert: async () => {
    try {
      const response = await api.get('/alerts/latest');
      return response.data;
    } catch (error) {
      if (error.response?.status === 404) {
        return null; // No alerts found
      }
      console.error('Error fetching latest alert:', error);
      throw error;
    }
  },

  // Get alerts by device ID
  getAlertsByDevice: async (deviceId) => {
    try {
      const response = await api.get(`/alerts/${deviceId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching alerts for device ${deviceId}:`, error);
      throw error;
    }
  },
};

export default api;