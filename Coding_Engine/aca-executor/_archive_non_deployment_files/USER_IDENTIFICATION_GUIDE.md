# User Identification Guide

## 🔍 Current Implementation

### **Problem:**
Currently, `user_id` is **hardcoded** as `'test_user'` in the frontend. This means:
- ❌ All users appear as the same user
- ❌ Can't distinguish between you and your friend
- ❌ No way to track individual submissions

### **Current Code:**
```javascript
// In index.html - line ~324
user_id: 'test_user',  // ← Hardcoded!
```

---

## ✅ Solution Options

### **Option 1: Browser Session ID (Quick Fix)** ⭐ Recommended for Testing

**How it works:**
- Generate a unique ID when page loads
- Store in browser's `localStorage`
- Same ID persists across page refreshes
- Different browser = different user

**Implementation:**
```javascript
// Generate unique user ID on page load
let userId = localStorage.getItem('user_id');
if (!userId) {
    userId = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    localStorage.setItem('user_id', userId);
}
```

**Pros:**
- ✅ Quick to implement (5 minutes)
- ✅ Works immediately
- ✅ Each browser gets unique ID
- ✅ Persists across page refreshes

**Cons:**
- ⚠️ Clears if user clears browser data
- ⚠️ Not tied to actual user account

---

### **Option 2: IP Address + Browser Fingerprint**

**How it works:**
- Use IP address from backend
- Combine with browser fingerprint
- More stable identification

**Implementation:**
```javascript
// Get IP from backend
const response = await fetch('/api/user-id');
const { user_id } = await response.json();
```

**Pros:**
- ✅ More stable
- ✅ Works across devices on same network

**Cons:**
- ⚠️ Same network = same IP (can't distinguish)
- ⚠️ Requires backend changes

---

### **Option 3: Login/Authentication (Production)**

**How it works:**
- User logs in with email/username
- Backend assigns user_id
- Stored in session/cookie

**Pros:**
- ✅ Proper user management
- ✅ Secure
- ✅ Production-ready

**Cons:**
- ⚠️ Requires full auth system
- ⚠️ More complex

---

## 🚀 Recommended: Option 1 (Session ID)

### **For Testing/Contest:**

**Quick Implementation:**
1. Generate unique ID per browser
2. Store in localStorage
3. Send with each request

**Result:**
- You: `user_1732800000_abc123`
- Friend: `user_1732800001_xyz789`
- Each browser = unique user

---

## 📋 Implementation Steps

### **Step 1: Update Frontend**

Add to `index.html`:
```javascript
// Generate or retrieve user ID
function getUserId() {
    let userId = localStorage.getItem('user_id');
    if (!userId) {
        // Generate unique ID: user_timestamp_random
        userId = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('user_id', userId);
    }
    return userId;
}

// Use in runCode():
user_id: getUserId(),  // Instead of 'test_user'
```

### **Step 2: Display User ID in UI**

Add to header:
```html
<div class="text-sm text-gray-600">
    User ID: <span id="user-id-display"></span>
</div>
```

```javascript
// Show user ID
document.getElementById('user-id-display').textContent = getUserId();
```

---

## 🧪 Testing Scenarios

### **Scenario 1: You Test from Your System**
1. Open browser → Gets ID: `user_1732800000_abc123`
2. Submit code → Logged as: `user_1732800000_abc123`
3. Refresh page → Same ID (from localStorage)
4. **Monitoring shows:** Your submissions with your ID

### **Scenario 2: Friend Tests from Their System**
1. Friend opens browser → Gets ID: `user_1732800001_xyz789`
2. Friend submits code → Logged as: `user_1732800001_xyz789`
3. **Monitoring shows:** Friend's submissions with different ID

### **Scenario 3: Same Computer, Different Browser**
1. Chrome → Gets ID: `user_1732800000_abc123`
2. Firefox → Gets ID: `user_1732800001_xyz789`
3. **Result:** Treated as different users ✅

---

## 📊 Monitoring View

### **What You'll See:**

**Before (Current):**
```
User ID: test_user
User ID: test_user
User ID: test_user
```

**After (With Session ID):**
```
User ID: user_1732800000_abc123  (You)
User ID: user_1732800001_xyz789  (Friend)
User ID: user_1732800002_def456  (Another user)
```

---

## 🔧 Quick Fix Implementation

I'll update the frontend to:
1. Generate unique user ID per browser
2. Display it in the UI
3. Send it with each execution request
4. Persist across page refreshes

**Result:** Each browser gets a unique ID, so you and your friend will have different IDs!

---

## 💡 Future Enhancements

### **For Production:**
1. Add login system
2. Store user_id in database
3. Link submissions to user accounts
4. Add user management dashboard

### **For Contest:**
1. Pre-register users
2. Assign contest IDs
3. Validate user_id before execution
4. Track submissions per user

---

## ✅ Summary

**Current:** All users = `'test_user'` ❌

**After Fix:** Each browser = unique ID ✅

**Implementation Time:** 5 minutes

**Result:** You and your friend will have different user IDs, and monitoring will show them separately!


