# Fix for "Failed to fetch" Error

## ✅ Solution

The server is now configured to run on **port 3001** (to avoid conflict with port 3000).

### Step 1: Start the Server

Open a terminal and run:

```bash
cd aca-executor/test-ui
npm start
```

You should see:
```
✅ Database connected successfully
✅ Database tables initialized
🚀 Server running on http://localhost:3001
```

### Step 2: Open in Browser

Open: **http://localhost:3001**

The frontend is already configured to connect to the API on port 3001.

---

## 🔧 Alternative: Use Port 3000

If you want to use port 3000 instead:

1. **Stop the service on port 3000:**
   ```bash
   lsof -ti:3000 | xargs kill -9
   ```

2. **Change port in server.js:**
   ```javascript
   const PORT = 3000; // Change from 3001
   ```

3. **Change API URL in index.html:**
   ```javascript
   const API_BASE_URL = 'http://localhost:3000/api';
   ```

4. **Restart server:**
   ```bash
   npm start
   ```

---

## ✅ Verify It's Working

1. Server shows: `✅ Database connected successfully`
2. Browser opens: `http://localhost:3001`
3. Questions list appears in left sidebar
4. No "Failed to fetch" error

---

**Quick Start:**
```bash
cd aca-executor/test-ui
npm start
# Then open: http://localhost:3001
```


