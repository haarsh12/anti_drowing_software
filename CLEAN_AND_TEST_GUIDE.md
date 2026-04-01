# Clean Database and Test Single Case

## Quick Start (Recommended)

### Option 1: Automatic Cleanup and Test
```bash
# Run the complete cleanup and test
clean_and_test_single.bat
```

### Option 2: Manual Steps
```bash
# Step 1: Clear all previous cases
python clear_all_cases.py

# Step 2: Create single test case
python test_single_case.py
```

## Manual Database Cleanup (If Needed)

### Option 3: Interactive Cleanup
```bash
# Interactive cleanup with multiple options
python manual_database_cleanup.py
```

### Option 4: Complete Database Reset
```bash
# Stop backend server first, then:
python clear_database_and_test_one.py
```

## What Each Script Does

### `clear_all_cases.py`
- ✅ Finds and clears SQLite database
- ✅ Verifies cleanup via API
- ✅ Quick and simple

### `test_single_case.py`
- ✅ Creates one emergency case (Jalgaon Hospital)
- ✅ Adds guard responses
- ✅ Verifies case creation
- ✅ Perfect for testing

### `manual_database_cleanup.py`
- ✅ Interactive cleanup options
- ✅ Handles different database types
- ✅ Complete file deletion option

### `clear_database_and_test_one.py`
- ✅ Complete cleanup and test in one script
- ✅ Comprehensive verification
- ✅ Detailed output

## Testing the Single Case

After cleanup and creating the single case:

### 1. Mobile App Test
- ✅ Should show emergency notification
- ✅ Tap notification to open emergency overlay
- ✅ Test action buttons (Accept, Complete, Not Available)

### 2. Website Test
- ✅ Open: http://localhost:3000
- ✅ Should show exactly 1 case
- ✅ Check "Guard Responses" column
- ✅ Click "View Details" button
- ✅ Click "View Maps" button

### 3. Expected Results
- **Total Cases**: 1
- **Device**: JALGAON_04_JALGAON_HOSPITAL
- **Status**: 🚨 DANGER
- **Location**: 20.95, 75.556
- **Guard Responses**: 2 (1 Accepted, 1 Completed)

## Troubleshooting

### Database Not Clearing
1. Stop backend server
2. Run `python manual_database_cleanup.py`
3. Choose option 2 (delete files)
4. Restart backend server

### API Not Responding
1. Check backend is running: http://localhost:8000
2. Check API endpoint: http://localhost:8000/api/alerts
3. Restart backend if needed

### Mobile App Not Getting Notifications
1. Ensure app is running
2. Check API connection in app
3. Try closing and reopening app
4. Check device notification permissions

### Website Not Showing Case
1. Check frontend is running: http://localhost:3000
2. Check browser console for errors
3. Refresh the page
4. Check backend API directly

## Quick Verification Commands

```bash
# Check if backend is running
curl http://localhost:8000/api/alerts

# Check number of alerts
python -c "import requests; r=requests.get('http://localhost:8000/api/alerts'); print(f'Alerts: {len(r.json()[\"alerts\"])}')"

# Test single case creation
python test_single_case.py
```

## Success Criteria

After running the cleanup and test:
- ✅ Database has exactly 1 case
- ✅ Mobile app shows emergency notification
- ✅ Website shows 1 case with guard responses
- ✅ "View Details" shows complete case information
- ✅ "View Maps" opens Google Maps with correct location
- ✅ All features work as expected

## Next Steps After Testing

1. **Mobile App**: Test emergency response workflow
2. **Website**: Test case management features
3. **Integration**: Test real ESP32 device alerts
4. **Performance**: Test with multiple simultaneous alerts
5. **Production**: Deploy to production environment