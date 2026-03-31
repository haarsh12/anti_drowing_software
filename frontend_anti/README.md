# IoT Alert Dashboard - Frontend

Modern React dashboard for the LoRa-based emergency alert system with soft neumorphism design.

## 🎨 Design Features

- **Theme**: Soft neumorphism with clean, minimal design
- **Background**: Light gray (#F3F4F6) with white cards
- **Typography**: Inter font family
- **Shadows**: Soft shadows with rounded corners
- **Colors**: Modern color palette with primary, danger, and success variants
- **Animations**: Smooth fade-in and slide-up animations

## 🚀 Features

- **Real-time Dashboard**: Auto-refreshes every 5 seconds
- **Interactive Map**: OpenStreetMap with custom markers (no API key required)
- **Alert Management**: Latest alert card with stats
- **Data Table**: Clean table with danger alert highlighting
- **Responsive Design**: Works on desktop and mobile
- **Loading States**: Smooth loading animations
- **Connection Status**: Real-time connection indicator

## 📁 Project Structure

```
frontend_anti/
├── src/
│   ├── components/
│   │   ├── Navbar.jsx          # Top navigation with search
│   │   ├── AlertCard.jsx       # Latest alert and stats
│   │   ├── MapView.jsx         # Interactive map component
│   │   └── AlertsTable.jsx     # Clean alerts table
│   ├── pages/
│   │   └── Dashboard.jsx       # Main dashboard page
│   ├── services/
│   │   └── api.js              # API service layer
│   ├── App.jsx                 # Main app component
│   ├── main.jsx                # React entry point
│   └── index.css               # Global styles
├── package.json                # Dependencies
├── tailwind.config.js          # Tailwind configuration
└── vite.config.js              # Vite configuration
```

## 🛠 Setup Instructions

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

## 🎯 Component Overview

### Navbar
- Logo and title
- Search functionality
- Connection status indicator
- Profile section

### AlertCard
- Latest alert status display
- Emergency/Safe status with icons
- Location and timestamp information
- Statistics cards (Total alerts, Danger alerts)

### MapView
- Interactive OpenStreetMap integration
- Custom red markers for danger alerts
- Custom green markers for safe alerts
- Detailed popups with alert information
- Map legend and header

### AlertsTable
- Clean table design with proper spacing
- Status column with icons and colors
- Device ID, location, and timestamp columns
- Danger alerts highlighted in red background
- Responsive design

## 🗺 Map Integration

- **Tiles**: OpenStreetMap (no API key required)
- **URL**: `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`
- **Library**: React Leaflet
- **Markers**: Custom SVG icons for danger (red) and safe (green)
- **Popups**: Detailed alert information with clean styling

## 🎨 Styling

### Tailwind Configuration
- Custom color palette with primary, danger, success variants
- Neumorphism shadow utilities
- Custom animations (fade-in, slide-up, pulse-soft)
- Inter font family

### Color Scheme
- **Background**: `#F3F4F6` (gray-100)
- **Cards**: White with soft shadows
- **Primary**: Blue variants for branding
- **Danger**: Red variants for emergency alerts
- **Success**: Green variants for safe status

## 🔄 Data Flow

1. **API Calls**: Axios service layer handles all backend communication
2. **Auto-refresh**: Dashboard updates every 5 seconds
3. **State Management**: React hooks for local state
4. **Error Handling**: Connection status and error states
5. **Loading States**: Skeleton loaders and spinners

## 📱 Responsive Design

- **Desktop**: Full layout with sidebar and main content
- **Tablet**: Stacked layout with responsive grid
- **Mobile**: Single column layout with touch-friendly interface

## 🔧 Configuration

### API Endpoint
Update the backend URL in `src/services/api.js`:

```javascript
const api = axios.create({
  baseURL: 'http://localhost:8000/api', // Change this to your backend URL
  timeout: 10000,
});
```

### Auto-refresh Interval
Modify the refresh interval in `src/pages/Dashboard.jsx`:

```javascript
const interval = setInterval(async () => {
  // Refresh logic
}, 5000); // Change 5000 to desired milliseconds
```

## 🎯 Usage

1. **Start Backend**: Ensure the FastAPI backend is running on port 8000
2. **Start Frontend**: Run `npm run dev` to start the development server
3. **View Dashboard**: Open `http://localhost:3000` in your browser
4. **Monitor Alerts**: The dashboard will automatically refresh and show new alerts

## 🚀 Production Deployment

### Build
```bash
npm run build
```

### Deploy Options
- **Vercel**: `vercel --prod`
- **Netlify**: Upload `dist` folder
- **GitHub Pages**: Use GitHub Actions
- **Static Hosting**: Serve `dist` folder

### Environment Variables
For production, update the API base URL to point to your production backend.

## 🎨 Customization

### Colors
Modify `tailwind.config.js` to change the color scheme:

```javascript
colors: {
  primary: { /* your primary colors */ },
  danger: { /* your danger colors */ },
  success: { /* your success colors */ },
}
```

### Layout
Adjust the grid layout in `Dashboard.jsx` to change component positioning.

### Animations
Customize animations in `tailwind.config.js` keyframes section.

This dashboard provides a production-ready, modern interface for monitoring IoT alerts with a clean, professional design that's both functional and visually appealing.