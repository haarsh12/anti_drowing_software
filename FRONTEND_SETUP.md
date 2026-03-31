# 🎨 Modern IoT Dashboard - Frontend Setup Guide

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd frontend_anti
npm install
```

### 2. Start Development Server
```bash
npm run dev
```

Dashboard will be available at: `http://localhost:3000`

## 🎯 What You'll See

### Modern Neumorphism Design
- **Light theme** with soft shadows and rounded corners
- **Clean typography** using Inter font
- **Smooth animations** with fade-in and slide-up effects
- **Professional color palette** with primary, danger, and success variants

### Dashboard Layout
```
┌─────────────────────────────────────────────────────────┐
│                    Navbar                               │
│  🔔 IoT Dashboard    [Search Bar]    📶 Status Profile │
└─────────────────────────────────────────────────────────┘
┌─────────────────┐ ┌─────────────────────────────────────┐
│   Alert Card    │ │                                     │
│   ┌───────────┐ │ │            Map View                 │
│   │ Latest    │ │ │                                     │
│   │ Alert     │ │ │  🗺️ Interactive OpenStreetMap      │
│   └───────────┘ │ │     with custom markers             │
│   ┌─────┬─────┐ │ │                                     │
│   │Total│Danger│ │ │                                     │
│   │  5  │  2   │ │ │                                     │
│   └─────┴─────┘ │ │                                     │
└─────────────────┘ └─────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│                 Alerts Table                            │
│  Status  │ Device ID │ Location  │ Timestamp            │
│  🚨 DANGER│ esp32_1   │ 18.52,73.85│ 2024-01-01 10:30   │
│  ✅ SAFE  │ esp32_2   │ 18.53,73.86│ 2024-01-01 10:25   │
└─────────────────────────────────────────────────────────┘
```

## 🎨 Design Features

### Color Scheme
- **Background**: Light gray (#F3F4F6)
- **Cards**: White with soft shadows
- **Primary**: Blue variants for branding
- **Danger**: Red variants for emergency alerts
- **Success**: Green variants for safe status

### Components

#### 1. Navbar
- Logo with gradient background
- Search bar (ready for future functionality)
- Connection status indicator
- Profile avatar

#### 2. Alert Card
- Latest alert status with large icons
- Device information and location
- Timestamp display
- Statistics cards showing total and danger alerts

#### 3. Map View
- OpenStreetMap integration (no API key needed)
- Custom red markers for danger alerts
- Custom green markers for safe alerts
- Detailed popups with alert information
- Map legend and header

#### 4. Alerts Table
- Clean table design with proper spacing
- Status column with colored icons
- Device ID, location, and timestamp
- Danger alerts highlighted with red background
- Hover effects and smooth transitions

## 🔧 Configuration

### API Connection
The frontend connects to your backend at `http://localhost:8000`. If your backend runs on a different port or server, update `src/services/api.js`:

```javascript
const api = axios.create({
  baseURL: 'http://your-server:8000/api',
  timeout: 10000,
});
```

### Auto-refresh Interval
Data refreshes every 5 seconds. To change this, modify `src/pages/Dashboard.jsx`:

```javascript
const interval = setInterval(async () => {
  // Refresh logic
}, 5000); // Change to desired milliseconds
```

## 🗺️ Map Integration

### OpenStreetMap Setup
- **No API key required** - uses free OpenStreetMap tiles
- **Tile URL**: `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`
- **Library**: React Leaflet for React integration
- **Markers**: Custom SVG icons for better visibility

### Map Features
- **Auto-centering**: Map centers on latest alert location
- **Custom markers**: Red for danger, green for safe
- **Interactive popups**: Click markers to see alert details
- **Responsive**: Works on all screen sizes

## 📱 Responsive Design

### Breakpoints
- **Mobile**: Single column layout
- **Tablet**: Stacked components
- **Desktop**: Full grid layout with sidebar

### Mobile Optimizations
- Touch-friendly buttons and interactions
- Optimized map controls for mobile
- Readable text sizes on small screens
- Proper spacing for touch targets

## 🔄 Data Flow

### Real-time Updates
1. Dashboard loads initial data on mount
2. Sets up 5-second auto-refresh interval
3. Fetches latest alert and all alerts simultaneously
4. Updates UI with smooth animations
5. Shows connection status and last update time

### Error Handling
- Connection status indicator shows red when offline
- Graceful fallbacks for missing data
- Loading states with skeleton animations
- Error boundaries for component failures

## 🎯 Testing the Dashboard

### 1. With Backend Running
```bash
# Terminal 1 - Backend
cd backend_anti
python main.py

# Terminal 2 - Frontend  
cd frontend_anti
npm run dev
```

### 2. Expected Behavior
- Dashboard loads with "No alerts" state initially
- Connection indicator shows green "Connected"
- Map displays default location (Pune, India)
- Auto-refresh indicator pulses every 5 seconds

### 3. With Test Data
Once you have alerts in your database:
- Latest alert appears in the alert card
- Map centers on alert location with colored marker
- Alerts table populates with all alerts
- Danger alerts highlighted in red

## 🚀 Production Build

### Build for Production
```bash
npm run build
```

### Deploy Options
1. **Vercel** (Recommended)
   ```bash
   npm install -g vercel
   vercel --prod
   ```

2. **Netlify**
   - Upload `dist` folder to Netlify
   - Set build command: `npm run build`
   - Set publish directory: `dist`

3. **Static Hosting**
   - Serve the `dist` folder with any web server
   - Ensure proper routing for SPA

### Environment Variables
For production deployment, create environment-specific API configurations.

## 🎨 Customization

### Changing Colors
Edit `tailwind.config.js`:
```javascript
colors: {
  primary: {
    500: '#your-primary-color',
    // ... other variants
  },
}
```

### Modifying Layout
- Edit `src/pages/Dashboard.jsx` for overall layout
- Modify individual components for specific sections
- Adjust grid classes for different responsive behavior

### Adding Features
- Search functionality in Navbar
- Filtering in AlertsTable
- Additional map layers
- Export functionality
- Real-time notifications

## 🔍 Troubleshooting

### Common Issues

1. **Map not loading**
   - Check internet connection
   - Verify Leaflet CSS is loaded
   - Check browser console for errors

2. **API connection failed**
   - Verify backend is running on port 8000
   - Check CORS configuration in backend
   - Verify API base URL in `api.js`

3. **Styling issues**
   - Run `npm install` to ensure all dependencies
   - Check Tailwind CSS is properly configured
   - Verify PostCSS configuration

4. **Build errors**
   - Clear node_modules and reinstall: `rm -rf node_modules && npm install`
   - Check for TypeScript errors if using TS
   - Verify all imports are correct

### Debug Mode
Add this to see API calls in console:
```javascript
// In src/services/api.js
api.interceptors.request.use(request => {
  console.log('Starting Request', request);
  return request;
});
```

## 🎉 Success!

Your modern IoT dashboard is now ready with:
- ✅ Beautiful neumorphism design
- ✅ Real-time data updates
- ✅ Interactive map with custom markers
- ✅ Clean, professional UI
- ✅ Responsive design
- ✅ Smooth animations
- ✅ Production-ready code

The dashboard will automatically connect to your backend and start displaying alerts as they come in from your ESP32 devices!