# Session Pool Testing Status & Cost Summary

## 📊 Current Status

**Date**: December 2024  
**Phase**: Testing Phase (Cost-Optimized)

### Resource Configuration
- **Session Pool**: `ai-ta-ra-session-pool`
- **Backend**: `ai-ta-ra-coding-engine`
- **Status**: ⏳ Update in progress (scaling down for testing)

### Current Issue
- ❌ **Code execution not working**: HTTP 404 errors
- ✅ **Infrastructure working**: Backend → Session Pool connection successful
- ✅ **Authentication working**: Managed Identity configured correctly

---

## 💰 Cost Analysis

### **Testing Configuration (Recommended)**
```bash
--max-sessions 5              # Maximum 5 concurrent
--ready-sessions 1            # 1 always-ready (minimum required)
--cooldown-period 300        # 5 minutes (minimum allowed)
```

**Daily Cost: ~$5.82/day** ($174/month)
- Ready session: $4.90/day
- Fixed costs: $0.27/day
- Backend: $0.65/day

### **Stopped/Idle Configuration**
```bash
# Delete session pool or scale to minimum
```

**Daily Cost: $0.27/day** ($8/month)
- Only ACR + Environment (fixed costs)

### **Contest Configuration (200+ students)**
```bash
--max-sessions 50             # Maximum 50 concurrent
--ready-sessions 5            # 5 always-ready
--cooldown-period 300        # 5 minutes
```

**Contest Cost: ~$2.39 for 2-hour contest**
- Ready sessions (2h): $2.04
- Active executions: $0.08
- Backend scaling: $0.27

---

## 🔧 How Code Execution Works

### Execution Flow:
```
1. User → Frontend → Backend API
2. Backend → Azure AD → Get Auth Token
3. Backend → Session Pool → POST /python/execute
4. Session Pool → Allocates Session Container (Hyper-V)
5. Session Container → Adapter Service (port 2000)
6. Adapter Service → Piston API (localhost:2001)
7. Piston → Executes Code in Sandbox
8. Piston → Returns stdout/stderr
9. Adapter → Translates to Azure Format
10. Adapter → Returns to Session Pool
11. Session Pool → Returns to Backend
12. Backend → Returns to Frontend
```

### Key Components:
- **Session Pool**: Manages container lifecycle
- **Session Container**: Hyper-V isolated container
- **Adapter Service**: Translates Azure ↔ Piston format
- **Piston API**: Actual code execution engine

---

## 🐛 Current Problem: HTTP 404

### Symptoms:
- Backend successfully authenticates
- Requests reach session pool (HTTP 200 auth)
- But execution returns: `{"message":"Not Found"}`

### Root Cause:
The session pool container's adapter service is not matching the route `/python/execute`, or the adapter service isn't running properly.

### Possible Issues:
1. Wrong image deployed (minimal-test instead of full)
2. Adapter service not starting
3. Piston not starting, causing adapter to fail
4. Route matching issue

---

## ✅ Fix Steps

### Step 1: Reduce Resources (Cost Optimization)
```bash
# Already in progress - scaling to:
--max-sessions 5
--ready-sessions 1
```

### Step 2: Fix Code Execution
Try different image tag:
```bash
# Try "working" tag instead of "v1"
az containerapp sessionpool update \
  --name ai-ta-ra-session-pool \
  --resource-group ai-ta-2 \
  --image aitaraacr1763805702.azurecr.io/session-image:working \
  --max-sessions 5 \
  --ready-sessions 1
```

### Step 3: Wait for Update
- Current update in progress
- Wait 2-3 minutes for completion
- Check status: `az containerapp sessionpool show ...`

### Step 4: Test After Fix
```bash
# Simple test
curl -X POST https://ai-ta-ra-coding-engine.happypond-428960e8.eastus2.azurecontainerapps.io/api/v2/execute \
  -H "Content-Type: application/json" \
  -d '{"language":"python","version":"3.11","files":[{"content":"print(42)"}],"stdin":"","args":[]}'

# Full test suite
python test_session_pool.py --endpoint https://ai-ta-ra-coding-engine.happypond-428960e8.eastus2.azurecontainerapps.io
```

---

## 📋 Cost Recommendations

### **For Testing Phase:**
1. ✅ Use minimum: `max-sessions: 5`, `ready-sessions: 1`
2. ✅ **Stop/delete when not testing** (saves $5.55/day)
3. ✅ Expected cost: **$5.82/day when running**

### **For Idle Periods:**
1. ✅ Delete session pool completely
2. ✅ Scale backend to 0 replicas
3. ✅ Cost: **$0.27/day** (only fixed costs)

### **For Contest:**
1. ✅ Scale up 30 min before: `max: 50`, `ready: 5`
2. ✅ Run contest: **$2.39 for 2 hours**
3. ✅ Scale down immediately after
4. ✅ Cost: **$0.27/day** when idle

---

## 📊 Cost Breakdown Details

### Per Resource:
| Resource | When Running | When Stopped |
|----------|-------------|--------------|
| Session Pool (ready: 1) | $4.90/day | $0/day |
| Backend (1 replica) | $0.65/day | $0/day |
| ACR | $0.17/day | $0.17/day |
| Environment | $0.10/day | $0.10/day |
| **Total** | **$5.82/day** | **$0.27/day** |

### Per Execution:
- **Warm execution**: $0.00004 per execution
- **Cold start**: $0.0001 per execution
- **1000 executions**: ~$0.04-0.10

**Conclusion**: Execution cost is negligible. Main cost is ready sessions running 24/7.

---

## 🎯 Next Actions

1. ⏳ **Wait for current update to complete** (scaling down)
2. 🔧 **Try "working" image tag** to fix 404 issue
3. ✅ **Test code execution** after fix
4. 💰 **Monitor costs** and stop when not testing
5. 📊 **Document results** for contest planning

---

## 📁 Related Documents

- `Cost_Analysis.md` - Detailed cost breakdown
- `Session_Pool_Fix_Guide.md` - Technical fix steps
- `SessionPool_Test_Plan.md` - Test scenarios
- `Azure_Test_Results.md` - Test results

---

**Status**: ⏳ Update in progress, fix pending  
**Cost**: $5.82/day when running, $0.27/day when stopped  
**Next**: Fix code execution, then test


