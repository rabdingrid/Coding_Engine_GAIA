# 🎯 Test Session Integration Plan

## 📋 Current Status

### ✅ What We Have:
1. **`test_session` table** - Created in Azure PostgreSQL ✅
2. **`coding_question_bank` table** - Already exists in Azure DB ✅
3. **Frontend server.js** - Already queries `coding_question_bank` ✅
4. **Database connection** - Azure PostgreSQL configured ✅

### ❌ What's Missing:
1. **API endpoints** for test_session (CRUD operations)
2. **Frontend integration** to create/update test sessions
3. **Heartbeat mechanism** (periodic updates)
4. **Session management** (start, update, complete, abandon)

---

## 🎯 Integration Goals

### 1. **Backend API Endpoints** (server.js)
- `POST /api/test-session` - Create new test session
- `GET /api/test-session/:candidate_id` - Get session details
- `PUT /api/test-session/:candidate_id/heartbeat` - Update heartbeat
- `PUT /api/test-session/:candidate_id/activity` - Update last activity
- `PUT /api/test-session/:candidate_id/complete` - Mark as completed
- `PUT /api/test-session/:candidate_id/abandon` - Mark as abandoned
- `PUT /api/test-session/:candidate_id/progress` - Update progress (sections, answers)
- `GET /api/test-session/active` - Get all active sessions
- `GET /api/test-session/abandoned` - Get abandoned sessions (for cleanup)

### 2. **Frontend Integration**
- Create session when test starts
- Send heartbeat every 30 seconds
- Update activity on user interaction
- Update progress when sections completed
- Mark as completed when test finished
- Handle tab close detection

### 3. **Data Flow**
```
Frontend → Create Session → Backend → Database
Frontend → Heartbeat (every 30s) → Backend → Database
Frontend → Update Progress → Backend → Database
Frontend → Complete Test → Backend → Database
```

---

## 📊 Database Schema Reference

### `test_session` Table:
```sql
- candidate_id (PK, FK → candidate)
- test_start_time
- test_duration_minutes (default: 60)
- last_heartbeat
- last_activity
- status ('active', 'completed', 'abandoned')
- completion_method ('manual', 'tab_close', 'timer_expired', 'heartbeat_timeout', 'auto')
- completed_at
- sections_completed (JSONB)
- pending_answers (JSONB)
- created_at (auto)
- updated_at (auto via trigger)
```

### `coding_question_bank` Table:
```sql
- uuid (PK)
- question
- sample_test_cases (JSONB)
- test_cases (JSONB)
- boiler_plate
- difficulty
- tags (JSONB)
```

---

## 🔧 Implementation Steps

### Phase 1: Backend API Endpoints ✅
1. Add test_session CRUD endpoints to server.js
2. Add validation for candidate_id
3. Add error handling
4. Test endpoints with curl/Postman

### Phase 2: Frontend Integration ✅
1. Add session creation on test start
2. Implement heartbeat interval (30s)
3. Add activity tracking
4. Add progress tracking
5. Add completion handling
6. Add tab close detection

### Phase 3: Testing ✅
1. Test session creation
2. Test heartbeat mechanism
3. Test progress updates
4. Test completion
5. Test abandonment detection

### Phase 4: Cleanup & Monitoring ✅
1. Add abandoned session cleanup job
2. Add session analytics endpoints
3. Add logging

---

## 📝 API Endpoint Specifications

### 1. Create Test Session
```http
POST /api/test-session
Content-Type: application/json

{
  "candidate_id": "uuid-here",
  "test_duration_minutes": 60
}

Response:
{
  "success": true,
  "session": {
    "candidate_id": "uuid-here",
    "test_start_time": "2024-01-01T10:00:00Z",
    "status": "active",
    ...
  }
}
```

### 2. Update Heartbeat
```http
PUT /api/test-session/:candidate_id/heartbeat

Response:
{
  "success": true,
  "last_heartbeat": "2024-01-01T10:00:30Z"
}
```

### 3. Update Activity
```http
PUT /api/test-session/:candidate_id/activity

Response:
{
  "success": true,
  "last_activity": "2024-01-01T10:00:30Z"
}
```

### 4. Update Progress
```http
PUT /api/test-session/:candidate_id/progress
Content-Type: application/json

{
  "sections_completed": ["section1", "section2"],
  "pending_answers": {
    "question1": "answer1",
    "question2": "answer2"
  }
}

Response:
{
  "success": true,
  "sections_completed": ["section1", "section2"],
  "pending_answers": {...}
}
```

### 5. Complete Test
```http
PUT /api/test-session/:candidate_id/complete
Content-Type: application/json

{
  "completion_method": "manual"
}

Response:
{
  "success": true,
  "status": "completed",
  "completed_at": "2024-01-01T10:30:00Z"
}
```

### 6. Abandon Test
```http
PUT /api/test-session/:candidate_id/abandon
Content-Type: application/json

{
  "completion_method": "tab_close"
}

Response:
{
  "success": true,
  "status": "abandoned"
}
```

### 7. Get Session
```http
GET /api/test-session/:candidate_id

Response:
{
  "success": true,
  "session": {
    "candidate_id": "uuid-here",
    "test_start_time": "2024-01-01T10:00:00Z",
    "status": "active",
    "last_heartbeat": "2024-01-01T10:00:30Z",
    ...
  }
}
```

### 8. Get Active Sessions
```http
GET /api/test-session/active

Response:
{
  "success": true,
  "sessions": [
    {
      "candidate_id": "uuid-1",
      "status": "active",
      ...
    },
    ...
  ]
}
```

---

## 🔄 Frontend Integration Flow

### Test Start Flow:
```javascript
1. User clicks "Start Test"
2. Frontend: POST /api/test-session
   {
     candidate_id: getCandidateId(),
     test_duration_minutes: 60
   }
3. Backend: Create session in DB
4. Frontend: Start heartbeat interval (30s)
5. Frontend: Start activity tracking
```

### Heartbeat Flow:
```javascript
setInterval(() => {
  fetch(`/api/test-session/${candidateId}/heartbeat`, {
    method: 'PUT'
  });
}, 30000); // Every 30 seconds
```

### Activity Tracking:
```javascript
// Track on any user interaction
document.addEventListener('click', updateActivity);
document.addEventListener('keypress', updateActivity);
document.addEventListener('scroll', updateActivity);

function updateActivity() {
  fetch(`/api/test-session/${candidateId}/activity`, {
    method: 'PUT'
  });
}
```

### Progress Tracking:
```javascript
// When section completed
fetch(`/api/test-session/${candidateId}/progress`, {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    sections_completed: completedSections,
    pending_answers: pendingAnswers
  })
});
```

### Completion Flow:
```javascript
// When test finished
fetch(`/api/test-session/${candidateId}/complete`, {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    completion_method: 'manual'
  })
});
```

### Tab Close Detection:
```javascript
window.addEventListener('beforeunload', () => {
  // Send abandon request
  navigator.sendBeacon(
    `/api/test-session/${candidateId}/abandon`,
    JSON.stringify({ completion_method: 'tab_close' })
  );
});
```

---

## 🧪 Testing Checklist

- [ ] Create session on test start
- [ ] Heartbeat updates every 30s
- [ ] Activity updates on user interaction
- [ ] Progress updates when sections completed
- [ ] Completion works correctly
- [ ] Tab close detection works
- [ ] Abandoned sessions detected
- [ ] Get session endpoint works
- [ ] Get active sessions works
- [ ] Error handling works

---

## 📊 Analytics & Monitoring

### Useful Queries:

**Active Sessions:**
```sql
SELECT * FROM test_session WHERE status = 'active';
```

**Abandoned Sessions (no heartbeat for 5 min):**
```sql
SELECT * FROM test_session
WHERE status = 'active'
AND last_heartbeat < CURRENT_TIMESTAMP - INTERVAL '5 minutes';
```

**Average Test Duration:**
```sql
SELECT AVG(EXTRACT(EPOCH FROM (completed_at - test_start_time))/60) as avg_minutes
FROM test_session
WHERE status = 'completed';
```

**Completion Rate:**
```sql
SELECT 
  status,
  COUNT(*) as count,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as percentage
FROM test_session
GROUP BY status;
```

---

## 🚀 Next Steps

1. **Implement Backend API** - Add endpoints to server.js
2. **Test Backend** - Use curl/Postman to test endpoints
3. **Frontend Integration** - Add session management to frontend
4. **Testing** - Test complete flow
5. **Deployment** - Deploy and monitor

---

**Ready to implement!** 🎯

