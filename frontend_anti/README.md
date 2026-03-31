# IoT Alert Dashboard - Frontend

React frontend for the LoRa-based emergency alert system with Tesla-style minimal design.

## Features

- **Real-time Dashboard**: Auto-refreshes every 5 seconds
- **Status Overview**: Shows latest alert with danger/safe status
- **Interactive Map**: Leaflet map showing alert locations with custom markers
- **Alerts Table**: List of all alerts with filtering and highlighting
- **Tesla-style UI**: Dark theme with clean, minimal design
- **Responsive Design**: Works on desktop and mobile devices

## Setup Instructions

### 1. Install Dependencies

```bash
cd frontend_anti
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The application will be available at: `http://localhost:3000`

### 3. Build for Production

```bash
npm run build
```

## Project Structure

```
frontend_anti/
├── src/
│   ├── components/
│   │   ├── Header.jsx          # Top navigation bar
│   │   ├── StatusCard.jsx      # Latest alert status display
│   │   ├── AlertMap.jsx        # Interactive map with markers
│   │   └── AlertsTable.jsx     # Alerts data table
│   ├── services/
│   │   └── api.js              # API service for backend communication
│   ├── App.jsx                 # Main application component
│   ├── main.jsx                # React entry point
│   └── index.css               # Global styles with Tailwind
├── public/                     # Static assets
├── package.json                # Dependencies and scripts
├── vite.config.js              # Vite configuration
├── tailwind.config.js          # Tailwind CSS configuration
└── README.md                   # This file
```

## Configuration

The frontend is configured to connect to the backend at `http://localhost:8000`. 

To change the API endpoint, update the `baseURL` in `src/services/api.js`:

```javascript
const api = axios.create({
  baseURL: 'http://your-backend-url:8000/api',
  // ...
});
```

## UI Components

### StatusCard
- Shows latest alert status (danger/safe)
- Displays location coordinates
- Shows device ID and timestamp
- Color-coded based on alert type

### AlertMap
- Interactive Leaflet map
- Custom markers for danger (red) and safe (green) alerts
- Popup with alert details
- Auto-centers on latest alert

### AlertsTable
- Tabular view of all alerts
- Sortable and filterable
- Highlights danger alerts in red
- Shows device info, location, and timestamp

### Header
- Connection status indicator
- Last update timestamp
- System branding

## Styling

- **Framework**: Tailwind CSS
- **Theme**: Tesla-inspired dark theme
- **Colors**: Custom Tesla color palette
- **Typography**: Inter font family
- **Responsive**: Mobile-first design

## Auto-refresh

The dashboard automatically refreshes data every 5 seconds to show real-time updates from IoT devices.