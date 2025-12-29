# Code Execution Service - Scope

## ✅ What This Service Does

This service is a **pure code execution engine** that:
- Executes code in 5 languages (Python, JavaScript, Java, C++, C#)
- Runs test cases and returns results
- Provides execution metrics (CPU, memory, timing)

## 📡 Endpoints

### `/health`
- Health check endpoint
- Returns service status

### `/run`
- **Purpose**: Run code with sample test cases
- **Input**: Code + sample test cases
- **Output**: Execution results for sample test cases
- **Rate Limit**: 50 requests/minute

### `/runall`
- **Purpose**: Run code with all test cases (excluding sample)
- **Input**: Code + all test cases
- **Output**: Execution results for all test cases
- **Rate Limit**: 1000 requests/minute
- **Optimization**: Uses batch execution for C++ (compile once, run multiple times)

## ❌ What This Service Does NOT Do

- **No Database**: This service does NOT save results to database
- **No `/submit` endpoint**: Submission handling is done by another service
- **No User Management**: This service doesn't handle user authentication
- **No Question Management**: Questions are managed by another service

## 🔄 Workflow

```
External Service → /run or /runall → Code Executor → Results → External Service
                                                          ↓
                                                    (No database)
```

The external service:
1. Sends code + test cases to this executor
2. Receives execution results
3. Handles database storage, user management, etc.

## 🚀 Deployment

- **No DATABASE_URL needed**: This service doesn't connect to any database
- **Environment Variables**: Only `PORT` (optional, defaults to 8000)
- **Simple & Fast**: No database overhead, pure execution

