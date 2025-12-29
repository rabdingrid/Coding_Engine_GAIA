# Quick Start Guide

## 🚨 "Failed to fetch" Error Fix

This error means **the backend server is not running**.

### ✅ Solution: Start the Server

**Option 1: Using the start script (Recommended)**
```bash
cd aca-executor/test-ui
./start.sh
```

**Option 2: Manual start**
```bash
cd aca-executor/test-ui
npm install  # Only needed first time
npm start
```

**Option 3: If port 3000 is busy**
```bash
# Kill existing process
lsof -ti:3000 | xargs kill -9

# Then start server
npm start
```

---

## ✅ Verify Server is Running

After starting the server, you should see:
```
✅ Database connected successfully
✅ Database tables initialized
🚀 Server running on http://localhost:3000
```

Then test the API:
```bash
curl http://localhost:3000/api/questions
```

You should get a JSON response (even if empty array).

---

## 🌐 Open in Browser

Once server is running:
1. Open: `http://localhost:3000`
2. You should see the UI with questions sidebar
3. Click "↻ Refresh" to load questions

---

## 🔧 If Still Not Working

1. **Check server terminal** for error messages
2. **Check browser console** (F12) for detailed errors
3. **Verify port 3000** is not blocked
4. **Check database connection** in server logs

---

**Quick Command**:
```bash
cd aca-executor/test-ui && npm start
```

Then open: `http://localhost:3000`


