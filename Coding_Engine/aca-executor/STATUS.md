# 🚀 Coding Engine - Current Status & Integration Guide

**Last Updated:** December 4, 2025  
**Repository:** [https://github.com/rabdingrid/Coding_Engine_GAIA.git](https://github.com/rabdingrid/Coding_Engine_GAIA.git)

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Database Schema](#database-schema)
4. [API Endpoints](#api-endpoints)
5. [Input/Output Formats](#inputoutput-formats)
6. [Deployment](#deployment)
7. [Integration Guide](#integration-guide)
8. [Flow Diagrams](#flow-diagrams)

---

## 🎯 Overview

This is a **production-ready coding execution engine** deployed on Azure Container Apps with PostgreSQL database integration. The system supports multiple programming languages (Python, Java, C++, JavaScript, C#) and handles concurrent code execution with auto-scaling capabilities.

### Key Features

- ✅ **Multi-language Support**: Python, Java, C++, JavaScript, C#
- ✅ **Auto-scaling**: Azure Container Apps with 1-3 replicas
- ✅ **Database Integration**: Azure PostgreSQL for questions and test sessions
- ✅ **Queue System**: Gunicorn handles concurrent requests per replica
- ✅ **Security**: Sandboxed execution, resource limits, code sanitization
- ✅ **Test Session Tracking**: Real-time session monitoring with heartbeat

### Current Status

- **Backend API**: ✅ Fully functional
- **Code Executor**: ✅ Deployed on Azure Container Apps
- **Database**: ✅ Azure PostgreSQL (migrated from Railway)
- **Frontend**: ✅ Test UI available
- **Test Session Table**: ✅ Created and ready for integration

---

## 🏗️ Architecture

### System Components

```
┌─────────────┐
│   Frontend  │ (React/Node.js)
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Backend API     │ (Express.js - server.js)
│  Port: 3001      │
└──────┬───────────┘
       │
       ├──► PostgreSQL (Azure)
       │    - coding_question_bank
       │    - test_session
       │    - candidate
       │
       └──► Code Executor (Azure Container Apps)
            - executor-service.py
            - Multi-language support
            - Auto-scaling (1-3 replicas)
```

### Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend API** | Node.js + Express.js |
| **Code Executor** | Python (Flask + Gunicorn) |
| **Database** | PostgreSQL (Azure Flexible Server) |
| **Deployment** | Azure Container Apps |
| **Container Registry** | Azure Container Registry (ACR) |
| **Infrastructure** | Terraform |

---

## 🗄️ Database Schema

### 1. `coding_question_bank` Table

Stores all coding questions with test cases and boilerplates.

```sql
CREATE TABLE coding_question_bank (
    uuid CHAR(36) PRIMARY KEY,
    question TEXT NOT NULL,
    sample_test_cases JSONB NOT NULL,
    test_cases JSONB NOT NULL,
    boiler_plate TEXT,
    difficulty VARCHAR(50),
    tags JSONB
);
```

**Current Data:** 52 questions loaded

### 2. `test_session` Table

Tracks candidate test sessions with timing and activity monitoring.

```sql
CREATE TABLE test_session (
    candidate_id VARCHAR(36) PRIMARY KEY,
    test_start_time TIMESTAMP NOT NULL,
    test_duration_minutes INTEGER DEFAULT 60,
    last_heartbeat TIMESTAMP,
    last_activity TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'completed', 'abandoned'
    completion_method VARCHAR(50), -- 'manual', 'tab_close', 'timer_expired', 'heartbeat_timeout', 'auto'
    completed_at TIMESTAMP,
    sections_completed JSONB,
    pending_answers JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (candidate_id) REFERENCES candidate(candidate_id) ON DELETE CASCADE
);
```

**Status Values:**
- `active`: Test in progress
- `completed`: Test finished
- `abandoned`: Test abandoned/timeout

**Completion Methods:**
- `manual`: Candidate clicked submit
- `tab_close`: Browser tab closed
- `timer_expired`: Time limit reached
- `heartbeat_timeout`: No heartbeat received
- `auto`: Auto-completed

### 3. `candidate` Table

Stores candidate information (referenced by test_session).

```sql
-- Assumes candidate table exists with candidate_id as primary key
```

---

## 📡 API Endpoints

### Base URL

- **Local Development:** `http://localhost:3001`
- **Production:** (Configure based on deployment)

### Questions API

#### 1. Get All Questions

```http
GET /api/questions
```

**Response:**
```json
{
  "success": true,
  "questions": [
    {
      "id": "uuid-here",
      "title": "Question Title",
      "description": "Question description...",
      "difficulty": "Medium",
      "tags": ["String", "Sliding Window"],
      "test_cases": [...]
    }
  ]
}
```

#### 2. Get Question by ID

```http
GET /api/questions/:id
```

**Parameters:**
- `id`: UUID or integer ID

**Response:**
```json
{
  "success": true,
  "question": {
    "id": "uuid-here",
    "title": "Question Title",
    "description": "Question description...",
    "difficulty": "Medium",
    "tags": ["String"],
    "boiler_plate": "{\"python\": \"...\", \"java\": \"...\"}"
  },
  "test_cases": [
    {
      "id": 1,
      "question_id": "uuid-here",
      "input": "test input",
      "expected_output": "expected output",
      "test_order": 1
    }
  ]
}
```

### Test Session API

#### 1. Create Test Session

```http
POST /api/test-session
Content-Type: application/json

{
  "candidate_id": "candidate-uuid",
  "test_duration_minutes": 60
}
```

**Response:**
```json
{
  "success": true,
  "session": {
    "candidate_id": "candidate-uuid",
    "test_start_time": "2024-12-04T10:00:00Z",
    "status": "active",
    "test_duration_minutes": 60
  }
}
```

#### 2. Update Heartbeat

```http
PUT /api/test-session/:candidate_id/heartbeat
```

**Response:**
```json
{
  "success": true,
  "last_heartbeat": "2024-12-04T10:00:30Z"
}
```

#### 3. Update Activity

```http
PUT /api/test-session/:candidate_id/activity
```

**Response:**
```json
{
  "success": true,
  "last_activity": "2024-12-04T10:00:30Z"
}
```

#### 4. Update Progress

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
```

**Response:**
```json
{
  "success": true,
  "sections_completed": ["section1", "section2"],
  "pending_answers": {...}
}
```

#### 5. Complete Test

```http
PUT /api/test-session/:candidate_id/complete
Content-Type: application/json

{
  "completion_method": "manual"
}
```

**Response:**
```json
{
  "success": true,
  "status": "completed",
  "completed_at": "2024-12-04T10:30:00Z"
}
```

#### 6. Abandon Test

```http
PUT /api/test-session/:candidate_id/abandon
Content-Type: application/json

{
  "completion_method": "tab_close"
}
```

**Response:**
```json
{
  "success": true,
  "status": "abandoned"
}
```

#### 7. Get Session

```http
GET /api/test-session/:candidate_id
```

**Response:**
```json
{
  "success": true,
  "session": {
    "candidate_id": "candidate-uuid",
    "test_start_time": "2024-12-04T10:00:00Z",
    "status": "active",
    "last_heartbeat": "2024-12-04T10:00:30Z",
    "last_activity": "2024-12-04T10:00:30Z",
    "sections_completed": [],
    "pending_answers": {}
  }
}
```

### Code Execution API

#### Execute Code

```http
POST /proxy/execute
Content-Type: application/json

{
  "language": "python",
  "code": "def solve():\n    return 42\n\nprint(solve())",
  "test_cases": [
    {
      "id": "test_1",
      "input": "5\n10",
      "expected_output": "15"
    }
  ],
  "user_id": "user123",
  "question_id": "question-uuid"
}
```

**Response:**
```json
{
  "execution_id": "exec-123",
  "summary": {
    "total_tests": 1,
    "passed": 1,
    "failed": 0,
    "all_passed": true
  },
  "results": [
    {
      "test_id": "test_1",
      "passed": true,
      "output": "15",
      "expected_output": "15",
      "error": null
    }
  ],
  "metadata": {
    "execution_time_ms": 150,
    "container_id": "container-abc",
    "replica": "replica-1"
  }
}
```

---

## 📥📤 Input/Output Formats

### Code Execution Request

```json
{
  "language": "python" | "java" | "cpp" | "javascript" | "csharp",
  "code": "string (code to execute)",
  "test_cases": [
    {
      "id": "string",
      "input": "string",
      "expected_output": "string"
    }
  ],
  "user_id": "string",
  "question_id": "string (optional)"
}
```

### Code Execution Response

```json
{
  "execution_id": "string",
  "summary": {
    "total_tests": "number",
    "passed": "number",
    "failed": "number",
    "all_passed": "boolean"
  },
  "results": [
    {
      "test_id": "string",
      "passed": "boolean",
      "output": "string",
      "expected_output": "string",
      "error": "string | null"
    }
  ],
  "metadata": {
    "execution_time_ms": "number",
    "container_id": "string",
    "replica": "string",
    "cpu_usage_percent": "number",
    "memory_usage_bytes": "number"
  }
}
```

### Test Case Format

```json
{
  "id": "test_1",
  "input": "5\n10",
  "expected_output": "15"
}
```

**Note:** Input and output are plain strings. For complex data structures, use JSON strings.

### Boilerplate Format

Stored as JSON string in `boiler_plate` column:

```json
{
  "python": "def solve():\n    pass\n\nprint(solve())",
  "java": "public class Main {\n    public static void main(String[] args) {\n        // code\n    }\n}",
  "cpp": "#include <iostream>\nusing namespace std;\n\nint main() {\n    // code\n    return 0;\n}",
  "javascript": "function solve() {\n    // code\n}\n\nconsole.log(solve());",
  "csharp": "using System;\n\npublic class Solution {\n    public static void Main() {\n        // code\n    }\n}"
}
```

---

## 🚀 Deployment

### Executor Service (Azure Container Apps)

**Current Deployment:**
- **URL:** `https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io`
- **Replicas:** 1-3 (auto-scaling)
- **Resource Group:** `ai-ta-2`
- **Container App:** `ai-ta-ra-code-executor2`

### Database (Azure PostgreSQL)

**Connection String:**
```
postgresql://postgresadmin:5oXcNX59QmEl7zmV3DbjemkiJ@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require
```

**Server:** `ai-ta-ra-postgre.postgres.database.azure.com`  
**Database:** `railway`  
**Port:** `5432`

### Deployment Steps

1. **Build Docker Image:**
   ```bash
   docker build -t aca-executor:latest .
   ```

2. **Push to ACR:**
   ```bash
   az acr login --name <acr-name>
   docker tag aca-executor:latest <acr-name>.azurecr.io/aca-executor:v<version>
   docker push <acr-name>.azurecr.io/aca-executor:v<version>
   ```

3. **Deploy with Terraform:**
   ```bash
   cd terraform
   terraform init
   terraform plan
   terraform apply
   ```

---

## 🔗 Integration Guide

### For Frontend Developers

#### 1. Connect to Backend API

```javascript
const API_BASE_URL = 'http://localhost:3001'; // or production URL

// Fetch questions
const response = await fetch(`${API_BASE_URL}/api/questions`);
const data = await response.json();
const questions = data.questions;
```

#### 2. Create Test Session

```javascript
// When test starts
const sessionResponse = await fetch(`${API_BASE_URL}/api/test-session`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    candidate_id: candidateId,
    test_duration_minutes: 60
  })
});
const session = await sessionResponse.json();
```

#### 3. Send Heartbeat (Every 30 seconds)

```javascript
setInterval(async () => {
  await fetch(`${API_BASE_URL}/api/test-session/${candidateId}/heartbeat`, {
    method: 'PUT'
  });
}, 30000); // 30 seconds
```

#### 4. Update Activity

```javascript
// On user interaction
document.addEventListener('click', updateActivity);
document.addEventListener('keypress', updateActivity);

async function updateActivity() {
  await fetch(`${API_BASE_URL}/api/test-session/${candidateId}/activity`, {
    method: 'PUT'
  });
}
```

#### 5. Execute Code

```javascript
const executeResponse = await fetch(`${API_BASE_URL}/proxy/execute`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    language: 'python',
    code: userCode,
    test_cases: questionTestCases,
    user_id: candidateId,
    question_id: questionId
  })
});
const result = await executeResponse.json();
```

#### 6. Complete Test

```javascript
// When test finished
await fetch(`${API_BASE_URL}/api/test-session/${candidateId}/complete`, {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    completion_method: 'manual'
  })
});
```

#### 7. Handle Tab Close

```javascript
window.addEventListener('beforeunload', () => {
  navigator.sendBeacon(
    `${API_BASE_URL}/api/test-session/${candidateId}/abandon`,
    JSON.stringify({ completion_method: 'tab_close' })
  );
});
```

### For Backend Developers

#### 1. Database Connection

```javascript
const { Pool } = require('pg');

const pool = new Pool({
  connectionString: process.env.DATABASE_URL || 'postgresql://...',
  ssl: { rejectUnauthorized: false }
});
```

#### 2. Query Questions

```javascript
const result = await pool.query(
  'SELECT * FROM coding_question_bank WHERE uuid = $1',
  [questionId]
);
```

#### 3. Create Test Session

```javascript
await pool.query(`
  INSERT INTO test_session (candidate_id, test_start_time, status)
  VALUES ($1, CURRENT_TIMESTAMP, 'active')
  ON CONFLICT (candidate_id) DO UPDATE
  SET test_start_time = CURRENT_TIMESTAMP, status = 'active'
`, [candidateId]);
```

---

## 📊 Flow Diagrams

### Test Session Flow

```
┌─────────────┐
│   Frontend  │
└──────┬──────┘
       │
       │ 1. POST /api/test-session
       ▼
┌─────────────────┐
│  Backend API    │
└──────┬──────────┘
       │
       │ 2. INSERT INTO test_session
       ▼
┌─────────────────┐
│   PostgreSQL    │
└─────────────────┘

       │
       │ 3. Heartbeat every 30s
       │    PUT /api/test-session/:id/heartbeat
       │
       │ 4. Update activity on interaction
       │    PUT /api/test-session/:id/activity
       │
       │ 5. Update progress
       │    PUT /api/test-session/:id/progress
       │
       │ 6. Complete test
       │    PUT /api/test-session/:id/complete
       ▼
```

### Code Execution Flow

```
┌─────────────┐
│   Frontend  │
└──────┬──────┘
       │
       │ POST /proxy/execute
       │ {
       │   language, code, test_cases
       │ }
       ▼
┌─────────────────┐
│  Backend API    │
└──────┬──────────┘
       │
       │ Forward to executor
       ▼
┌─────────────────────────┐
│  Code Executor (Azure)  │
│  - Sandbox execution     │
│  - Run test cases        │
│  - Collect results      │
└──────┬──────────────────┘
       │
       │ Return results
       ▼
┌─────────────────┐
│  Backend API    │
└──────┬──────────┘
       │
       │ Return to frontend
       ▼
┌─────────────┐
│   Frontend  │
│  Display    │
│  Results    │
└─────────────┘
```

### Question Fetching Flow

```
┌─────────────┐
│   Frontend  │
└──────┬──────┘
       │
       │ GET /api/questions
       ▼
┌─────────────────┐
│  Backend API    │
└──────┬──────────┘
       │
       │ SELECT FROM coding_question_bank
       ▼
┌─────────────────┐
│   PostgreSQL    │
│ coding_question │
│     _bank       │
└──────┬──────────┘
       │
       │ Return questions
       ▼
┌─────────────────┐
│  Backend API    │
└──────┬──────────┘
       │
       │ Format and return
       ▼
┌─────────────┐
│   Frontend  │
│  Display    │
│  Questions  │
└─────────────┘
```

---

## 🔧 Configuration

### Environment Variables

**Backend API (server.js):**
```bash
PORT=3001
DATABASE_URL=postgresql://postgresadmin:...@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require
```

**Code Executor:**
```bash
PORT=8000
MAX_WORKERS=4
TIMEOUT_SECONDS=30
MEMORY_LIMIT_MB=512
```

### Database Setup

1. **Create test_session table:**
   ```bash
   psql $DATABASE_URL < test-session-table.sql
   ```

2. **Verify tables:**
   ```sql
   SELECT table_name FROM information_schema.tables 
   WHERE table_schema = 'public';
   ```

---

## 📝 Important Notes

1. **Database Connection:** Always use SSL (`sslmode=require`) for Azure PostgreSQL
2. **Heartbeat Frequency:** Send heartbeat every 30 seconds for active sessions
3. **Test Session Status:** Monitor `last_heartbeat` to detect abandoned sessions
4. **Code Execution:** All code runs in sandboxed containers with resource limits
5. **Auto-scaling:** Container Apps scale 1-3 replicas based on load

---

## 🐛 Troubleshooting

### Database Connection Issues

- Verify connection string format
- Check firewall rules in Azure Portal
- Ensure SSL is enabled (`sslmode=require`)

### Test Session Not Updating

- Verify `candidate_id` exists in `candidate` table
- Check foreign key constraint
- Ensure heartbeat is being sent

### Code Execution Fails

- Check executor service is running
- Verify language is supported
- Check code syntax and test case format

---

## 📚 Additional Resources

- **Architecture Diagram:** See `COMPLETE_ARCHITECTURE_DIAGRAM.md`
- **Deployment Guide:** See `DEPLOYMENT_DIAGRAM.md`
- **Test Session Integration:** See `TEST_SESSION_INTEGRATION_PLAN.md`

---

## 👥 For Contributors

1. **Clone Repository:**
   ```bash
   git clone https://github.com/rabdingrid/Coding_Engine_GAIA.git
   cd Coding_Engine_GAIA
   ```

2. **Install Dependencies:**
   ```bash
   cd test-ui
   npm install
   ```

3. **Set Environment Variables:**
   ```bash
   export DATABASE_URL="postgresql://..."
   ```

4. **Run Backend:**
   ```bash
   npm start
   ```

5. **Test API:**
   ```bash
   curl http://localhost:3001/api/questions
   ```

---

**Ready for Integration!** 🚀

For questions or issues, refer to the integration plan or contact the team.

