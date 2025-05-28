# 🚀 WoofWorld Backend Server Startup Guide

## Quick Start

### Option 1: Using the Batch File (Easiest)
1. Navigate to: `C:\Project\Pemograman Web\WoofWorld\woofworld_backend`
2. Double-click `start.bat`
3. Wait for "Server started. Press Ctrl+C to stop"

### Option 2: Using Command Line
1. Open Command Prompt or PowerShell
2. Navigate to the backend directory:
   ```
   cd "C:\Project\Pemograman Web\WoofWorld\woofworld_backend"
   ```
3. Start the server:
   ```
   python start_server.py
   ```

### Option 3: Using Pyramid's pserve
1. Open Command Prompt in the backend directory
2. Run:
   ```
   pserve development.ini --reload
   ```

## ✅ Verification

After starting the server, you should see:
- "Server started. Press Ctrl+C to stop"
- Server running on http://localhost:6544

## 🧪 Test the Fix

Open the test page in your browser:
- `file:///C:/Project/Pemograman%20Web/WoofWorld/final_verification.html`

Click "🚀 Run Complete Test" to verify everything works.

## 🎯 What Was Fixed

1. **CORS Configuration**: Updated `tweens.py` to properly handle cross-origin requests
2. **Field Names**: Confirmed admin endpoint uses `content` field (not `fact`)
3. **Debug Logging**: Added comprehensive logging for troubleshooting
4. **Error Handling**: Improved error handling in CORS tween

## 📁 Files Modified

- `woofworld_backend/woofworld_backend/tweens.py` - Enhanced CORS handling
- `woofworld_backend/development.ini` - Updated CORS origins
- `woofworld_backend/start.bat` - Created easy startup script

## 🔧 If Issues Persist

1. Check that port 6544 is not in use by another application
2. Verify admin user exists in database (`admin@woofworld.com` / `admin123`)
3. Check server console for error messages
4. Use browser F12 console to see detailed error logs

Your FactManagement.jsx should now work perfectly! 🎉
