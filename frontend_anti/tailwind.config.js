/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'tesla-dark': '#1a1a1a',
        'tesla-gray': '#2a2a2a',
        'tesla-light': '#f5f5f5',
        'tesla-blue': '#3b82f6',
        'tesla-red': '#ef4444',
        'tesla-green': '#10b981',
      },
      fontFamily: {
        'tesla': ['Inter', 'system-ui', 'sans-serif'],
      }
    },
  },
  plugins: [],
}