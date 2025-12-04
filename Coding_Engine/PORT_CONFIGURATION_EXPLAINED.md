# Port Configuration - Why Different Ports Are CORRECT

## ✅ Port Configuration is CORRECT

### Backend (Coding Engine)
- **Port**: 8000
- **Location**: Container App (`ai-ta-ra-coding-engine`)
- **Purpose**: Receives API requests from users/frontend
- **URL**: `https://ai-ta-ra-coding-engine.happypond-428960e8.eastus2.azurecontainerapps.io`
- **Endpoint**: `/api/v2/execute`

### Session Pool
- **Port**: 2000
- **Location**: Session Pool containers (separate service)
- **Purpose**: Executes code via adapter service
- **URL**: `https://ai-ta-ra-session-pool.happypond-428960e8.eastus2.azurecontainerapps.io`
- **Endpoint**: `/python/execute`

---

## 🔍 Why Different Ports Are NOT a Problem

### They're Different Services

```
┌─────────────────────────────────────┐
│  User/Frontend                      │
│  (makes HTTP request)               │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Backend (Coding Engine)            │
│  Port: 8000                         │
│  Container App                      │
│  Receives: /api/v2/execute         │
└──────────────┬──────────────────────┘
               │
               │ HTTP Request
               │ (to session pool URL)
               ▼
┌─────────────────────────────────────┐
│  Session Pool                       │
│  Port: 2000                         │
│  Session Pool Container             │
│  Receives: /python/execute         │
└─────────────────────────────────────┘
```

### How They Communicate

1. **User** → **Backend (port 8000)**: User sends code execution request
2. **Backend** → **Session Pool (port 2000)**: Backend forwards request to session pool
3. **Session Pool** → **Backend**: Returns execution result
4. **Backend** → **User**: Returns final response

**Key Point**: The backend makes an **HTTP request** to the session pool's **public URL**. The ports don't conflict because:
- Backend listens on port 8000 (for incoming user requests)
- Session pool listens on port 2000 (for incoming backend requests)
- They're **different services** in **different containers**

---

## ❌ The REAL Issue

The problem is **NOT port conflicts**. The problem is:

1. **Ingress not enabled** on session pool
   - Backend cannot reach session pool's public URL
   - Results in 404 errors

2. **Target port not set** (or ingress not configured)
   - Azure doesn't know how to route traffic to port 2000
   - Even though container listens on 2000, Azure can't forward requests

---

## ✅ What Needs to Happen

### Current Flow (BROKEN):
```
Backend → Session Pool URL → ❌ 404 Not Found
(ingress not enabled, so Azure can't route)
```

### Fixed Flow (AFTER INGRESS ENABLED):
```
Backend → Session Pool URL → ✅ Port 2000 → Container → Adapter → Code Execution
(ingress enabled, Azure routes to port 2000)
```

---

## 📋 Summary

| Question | Answer |
|----------|--------|
| **Are different ports a problem?** | ❌ NO - They're different services |
| **Should they be the same port?** | ❌ NO - They're separate services |
| **Is port 8000 vs 2000 causing issues?** | ❌ NO - Not a port conflict |
| **What's the real issue?** | ✅ Ingress not enabled on session pool |
| **What needs to be fixed?** | ✅ Enable ingress + set target-port=2000 |

---

## 🎯 Conclusion

**Different ports are CORRECT and EXPECTED.**

The issue is **ingress configuration**, not port conflicts.

Once ingress is enabled and target-port is set to 2000, the backend will be able to reach the session pool, and everything will work correctly.

---

**Status**: Port configuration is correct ✅  
**Issue**: Ingress not enabled (not a port problem) ❌


