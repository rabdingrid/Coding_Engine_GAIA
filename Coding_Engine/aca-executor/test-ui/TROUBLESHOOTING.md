# Troubleshooting Guide

## ❌ Error: "Failed to fetch"

This error means the frontend cannot connect to the backend API server.

### Solution 1: Start the Server

The server must be running for the frontend to work.

```bash
cd test-ui
npm install  # If not already done
npm start
```

The server should start on `http://localhost:3000`

### Solution 2: Check Server Status

Open a new terminal and check if the server is running:

```bash
curl http://localhost:3000/api/questions
```

If you get a response, the server is running. If you get "Connection refused", the server is not running.

### Solution 3: Check Port

Make sure port 3000 is not being used by another application:

```bash
lsof -i:3000
```

If something is using port 3000, either:
- Stop that application
- Or change the port in `server.js` (line 5: `const PORT = 3000;`)

### Solution 4: Check Browser Console

Open browser Developer Tools (F12) and check the Console tab for detailed error messages.

### Solution 5: Verify Database Connection

Check the server terminal for database connection errors. The server should show:
```
✅ Database connected successfully
✅ Database tables initialized
```

If you see database errors, check:
- Database connection string is correct
- Database is accessible
- Network/firewall allows connection

---

## 🔧 Quick Fixes

### Restart Everything

```bash
# Stop server (Ctrl+C)
# Then restart:
cd test-ui
npm start
```

### Clear Browser Cache

- Hard refresh: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)
- Or clear browser cache

### Check API URL

In `index.html`, verify the API URL is correct:
```javascript
const API_BASE_URL = 'http://localhost:3000/api';
```

Make sure it matches your server port.

---

## ✅ Expected Behavior

When everything works:

1. **Server starts**: You see:
   ```
   ✅ Database connected successfully
   ✅ Database tables initialized
   🚀 Server running on http://localhost:3000
   ```

2. **Frontend loads**: Questions list appears in left sidebar

3. **API works**: Clicking "Refresh" loads questions from database

---

## 🐛 Common Issues

### Issue: "Cannot find module 'express'"
**Fix**: Run `npm install`

### Issue: "Port 3000 already in use"
**Fix**: 
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
# Or change port in server.js
```

### Issue: "Database connection error"
**Fix**: Check database connection string in `server.js`

### Issue: "CORS error"
**Fix**: Already handled in server.js with CORS middleware

---

## 📞 Still Having Issues?

1. Check server terminal for error messages
2. Check browser console (F12) for errors
3. Verify all dependencies are installed: `npm install`
4. Make sure database is accessible
5. Try restarting the server

---

**Quick Start Command**:
```bash
cd test-ui && ./start.sh
```


