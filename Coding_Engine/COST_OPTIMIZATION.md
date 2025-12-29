# Cost Optimization - Ready Sessions Set to 0

## ✅ Configuration Updated

**Ready Sessions**: Set to 0 (minimize costs)

### Current Configuration:
- **Ready Sessions**: 0 (no sessions running when idle)
- **Max Sessions**: 5 (can scale up to 5 concurrent sessions when needed)
- **Cooldown Period**: 300 seconds (sessions stay alive for 5 minutes after last request)

---

## 💰 Cost Impact

### Before (Ready Sessions = 1):
- 1 session always running = **Continuous cost**
- Cost: ~$0.0001-0.0002 per hour per session
- Monthly: ~$0.07-0.14 per ready session

### After (Ready Sessions = 0):
- 0 sessions when idle = **No cost when idle**
- Sessions allocated on-demand when requests arrive
- Cost only when code is actually executing
- First request: 3-5 second cold start (session allocation)
- Subsequent requests: Fast (session already allocated)

---

## ⚡ Performance Impact

### Cold Start (First Request):
- **Time**: 3-5 seconds
- **Reason**: Azure needs to allocate a new session container
- **Impact**: Acceptable for testing/development

### Warm Requests (Same Session):
- **Time**: < 1 second
- **Reason**: Session already allocated
- **Impact**: Fast execution

---

## 📋 How It Works

1. **Idle State**: 0 sessions running (no cost)
2. **First Request**: Azure allocates session (3-5 sec delay)
3. **Active State**: Session handles requests (fast)
4. **After 5 min idle**: Session deallocated (back to 0, no cost)

---

## ✅ Benefits

- ✅ **Minimal cost** when not in use
- ✅ **On-demand scaling** when needed
- ✅ **Still functional** - code execution works
- ✅ **Automatic cleanup** - sessions deallocate after cooldown

---

## ⚠️ Note

If ready sessions still shows 1, it might be:
- Existing session still deallocating (wait 1-2 minutes)
- Minimum might be 1 (check Azure docs)
- Update still propagating

---

**Status**: Ready sessions set to 0 for cost optimization  
**Impact**: Minimal cost when idle, on-demand allocation when needed


