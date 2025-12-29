# Developer Integration Guide - Code Execution API

## 🚀 Quick Start

This guide shows you how to integrate with the **deployed FastAPI code execution service** running on Azure Container Apps.

**Base URL**: `https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io`

---

## 📋 API Endpoints

### 1. **Health Check** (Test Connection)
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Code Execution Service (FastAPI)",
  "version": "3.0.0"
}
```

---

### 2. **Run Code with Sample Test Cases** (`/run`)
Quick test with sample inputs - perfect for "Run" button in your UI.

**Endpoint:** `POST /run`

**Request Body:**
```json
{
  "language": "python",
  "code": "def solve(n):\n    return n * 2\n\nn = int(input())\nprint(solve(n))",
  "sample_test_cases": [
    {
      "id": "sample_1",
      "input": "5",
      "expected_output": "10"
    }
  ],
  "user_id": "user123",
  "question_id": "q1"
}
```

**Response:**
```json
{
  "execution_id": "uuid-here",
  "summary": {
    "total_tests": 1,
    "passed": 1,
    "failed": 0,
    "all_passed": true,
    "pass_percentage": 100.0
  },
  "test_results": [
    {
      "test_case_id": "sample_1",
      "test_case_number": 1,
      "input": "5",
      "expected_output": "10",
      "actual_output": "10",
      "error": null,
      "status": "passed",
      "passed": true,
      "execution_time_ms": 45,
      "cpu_usage_percent": 12.5,
      "memory_usage_bytes": 1024000
    }
  ],
  "metadata": {
    "replica": "replica-1",
    "execution_time_ms": 45,
    "cpu_usage_percent": 12.5,
    "memory_usage_mb": 0.98
  },
  "timestamp": "2024-12-05T01:00:00"
}
```

---

### 3. **Run All Test Cases** (`/runall`)
Run code against all test cases (excluding sample) - perfect for "Run All" button.

**Endpoint:** `POST /runall`

**Request Body:**
```json
{
  "language": "python",
  "code": "def solve(n):\n    return n * 2\n\nn = int(input())\nprint(solve(n))",
  "test_cases": [
    {
      "id": "test_1",
      "input": "5",
      "expected_output": "10"
    },
    {
      "id": "test_2",
      "input": "10",
      "expected_output": "20"
    },
    {
      "id": "test_3",
      "input": "100",
      "expected_output": "200"
    }
  ],
  "sample_test_cases": [],
  "user_id": "user123",
  "question_id": "q1"
}
```

**Response:** Same format as `/run`, but with results for all test cases.

---

### 4. **Submit Final Code** (`/submit`)
Final submission - saves results to database. **Use this for actual grading.**

**Endpoint:** `POST /submit`

**Request Body:**
```json
{
  "language": "python",
  "code": "def solve(n):\n    return n * 2\n\nn = int(input())\nprint(solve(n))",
  "test_cases": [
    {
      "id": "test_1",
      "input": "5",
      "expected_output": "10"
    },
    {
      "id": "test_2",
      "input": "10",
      "expected_output": "20"
    }
  ],
  "user_id": "user123",
  "question_id": "q1"
}
```

**Note:** `user_id` and `question_id` are **required** for `/submit`.

**Response:** Same format as `/runall`, plus results are saved to database.

---

## 🔧 Integration Examples

### **JavaScript/TypeScript (Frontend)**

```javascript
const API_BASE_URL = 'https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io';

// Run code with sample test case
async function runCode(language, code, testCase) {
  const response = await fetch(`${API_BASE_URL}/run`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      language: language,
      code: code,
      sample_test_cases: [testCase],
      user_id: getCurrentUserId(),
      question_id: getCurrentQuestionId()
    })
  });
  
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  
  return await response.json();
}

// Run all test cases
async function runAllTestCases(language, code, testCases) {
  const response = await fetch(`${API_BASE_URL}/runall`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      language: language,
      code: code,
      test_cases: testCases,
      user_id: getCurrentUserId(),
      question_id: getCurrentQuestionId()
    })
  });
  
  return await response.json();
}

// Submit final code
async function submitCode(language, code, testCases, userId, questionId) {
  const response = await fetch(`${API_BASE_URL}/submit`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      language: language,
      code: code,
      test_cases: testCases,
      user_id: userId,
      question_id: questionId
    })
  });
  
  return await response.json();
}
```

---

### **Python (Backend)**

```python
import requests

API_BASE_URL = 'https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io'

def run_code(language, code, test_case):
    """Run code with a single test case"""
    response = requests.post(
        f'{API_BASE_URL}/run',
        json={
            'language': language,
            'code': code,
            'sample_test_cases': [test_case],
            'user_id': 'user123',
            'question_id': 'q1'
        }
    )
    response.raise_for_status()
    return response.json()

def run_all_test_cases(language, code, test_cases):
    """Run code with all test cases"""
    response = requests.post(
        f'{API_BASE_URL}/runall',
        json={
            'language': language,
            'code': code,
            'test_cases': test_cases,
            'user_id': 'user123',
            'question_id': 'q1'
        }
    )
    response.raise_for_status()
    return response.json()

def submit_code(language, code, test_cases, user_id, question_id):
    """Submit final code (saves to database)"""
    response = requests.post(
        f'{API_BASE_URL}/submit',
        json={
            'language': language,
            'code': code,
            'test_cases': test_cases,
            'user_id': user_id,
            'question_id': question_id
        }
    )
    response.raise_for_status()
    return response.json()

# Example usage
result = run_code(
    language='python',
    code='def solve(n):\n    return n * 2\n\nn = int(input())\nprint(solve(n))',
    test_case={
        'id': 'sample_1',
        'input': '5',
        'expected_output': '10'
    }
)

print(f"Passed: {result['summary']['all_passed']}")
print(f"Output: {result['test_results'][0]['actual_output']}")
```

---

### **cURL (Command Line)**

```bash
# Health check
curl https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/health

# Run code
curl -X POST https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/run \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "def solve(n):\n    return n * 2\n\nn = int(input())\nprint(solve(n))",
    "sample_test_cases": [
      {"id": "sample_1", "input": "5", "expected_output": "10"}
    ],
    "user_id": "user123",
    "question_id": "q1"
  }'

# Run all test cases
curl -X POST https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/runall \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "def solve(n):\n    return n * 2\n\nn = int(input())\nprint(solve(n))",
    "test_cases": [
      {"id": "test_1", "input": "5", "expected_output": "10"},
      {"id": "test_2", "input": "10", "expected_output": "20"}
    ],
    "user_id": "user123",
    "question_id": "q1"
  }'

# Submit final code
curl -X POST https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/submit \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "def solve(n):\n    return n * 2\n\nn = int(input())\nprint(solve(n))",
    "test_cases": [
      {"id": "test_1", "input": "5", "expected_output": "10"},
      {"id": "test_2", "input": "10", "expected_output": "20"}
    ],
    "user_id": "user123",
    "question_id": "q1"
  }'
```

---

## 📝 Request Format Details

### **Language Options**
- `python` - Python 3.11
- `javascript` - Node.js 16
- `java` - OpenJDK (HotSpot JVM)
- `cpp` - C++ (GCC)
- `csharp` - C# (Mono)

### **Test Case Format**
```json
{
  "id": "test_case_1",           // Unique identifier
  "input": "5\n10",              // Input string (use \n for newlines)
  "expected_output": "15"         // Expected output string
}
```

### **Code Format**
- **Important**: Send the **complete code** including boilerplate merged with user code
- For Python: Include all imports and main execution code
- For Java: Include class definition and main method
- For C++: Include all includes and main function

**Example (Python):**
```python
# User writes this:
def solve(n):
    return n * 2

# You merge with boilerplate:
def solve(n):
    return n * 2

n = int(input())
print(solve(n))
```

---

## ✅ Response Format

### **Success Response**
```json
{
  "execution_id": "uuid",
  "summary": {
    "total_tests": 5,
    "passed": 4,
    "failed": 1,
    "all_passed": false,
    "pass_percentage": 80.0
  },
  "test_results": [
    {
      "test_case_id": "test_1",
      "test_case_number": 1,
      "input": "5",
      "expected_output": "10",
      "actual_output": "10",
      "error": null,
      "status": "passed",
      "passed": true,
      "execution_time_ms": 45,
      "cpu_usage_percent": 12.5,
      "memory_usage_bytes": 1024000
    }
  ],
  "metadata": {
    "replica": "replica-1",
    "execution_time_ms": 500,
    "cpu_usage_percent": 15.2,
    "memory_usage_mb": 2.5
  },
  "timestamp": "2024-12-05T01:00:00"
}
```

### **Error Response**
```json
{
  "detail": "Code validation failed: Blocked pattern detected: import os"
}
```

**Status Codes:**
- `200` - Success
- `400` - Bad Request (invalid input, code validation failed)
- `429` - Rate Limit Exceeded
- `500` - Server Error

---

## 🚨 Error Status Types

In `test_results[].status`, you may see:

- `passed` - Test case passed ✅
- `failed` - Output doesn't match expected ❌
- `tle` - Time Limit Exceeded (execution took too long) ⏱️
- `mle` - Memory Limit Exceeded (used too much memory) 💾
- `syntax_error` - Code has syntax errors 🔴
- `runtime_error` - Code crashed during execution 💥
- `error` - Other execution error ⚠️

---

## ⚡ Rate Limits

- `/run`: **50 requests per minute** per IP
- `/runall`: **1000 requests per minute** per IP
- `/submit`: **200 requests per minute** per IP

If you hit rate limits, you'll get a `429` status code. Wait a minute and retry.

---

## 🔒 Security Notes

The API automatically:
- ✅ Blocks dangerous code patterns (file I/O, network, system calls)
- ✅ Limits resources (CPU: 10s, Memory: 1GB, Timeout: 5s per test case)
- ✅ Isolates execution in sandbox
- ✅ Blocks network access during execution

**Blocked Patterns:**
- Python: `import os`, `import subprocess`, `eval()`, `exec()`
- JavaScript: `require('fs')`, `require('child_process')`, `eval()`
- Java: `java.io.File`, `Runtime.getRuntime()`, `ProcessBuilder`
- C++: `#include <fstream>`, `system()`, `popen()`
- C#: `System.IO.File`, `System.Net.*`

---

## 📊 Best Practices

1. **Use `/run` for quick testing** during development
2. **Use `/runall` for full validation** before submission
3. **Use `/submit` only for final submissions** (saves to DB)
4. **Handle errors gracefully** - check `status` field in response
5. **Show execution metrics** - display `execution_time_ms`, `cpu_usage_percent` to users
6. **Implement retry logic** for rate limit errors (429)
7. **Merge boilerplate correctly** - ensure complete runnable code

---

## 🧪 Testing Your Integration

### **Step 1: Health Check**
```bash
curl https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/health
```

### **Step 2: Test Simple Code**
```bash
curl -X POST https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/run \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "print(42)",
    "sample_test_cases": [{"id": "t1", "input": "", "expected_output": "42"}]
  }'
```

### **Step 3: Test with Real DSA Question**
Use your actual question code and test cases.

---

## 🆘 Troubleshooting

### **"Code validation failed"**
- Check if code contains blocked patterns
- Ensure code is complete and runnable
- Verify language is correct (`python`, `java`, `cpp`, `javascript`, `csharp`)

### **"Rate limit exceeded" (429)**
- Wait 1 minute and retry
- Reduce request frequency
- Use `/runall` instead of multiple `/run` calls

### **"Timeout" or "TLE"**
- Code execution exceeded 5 seconds
- Optimize the algorithm
- Check for infinite loops

### **"Memory Limit Exceeded" (MLE)**
- Code used more than 1GB memory
- Optimize memory usage
- Check for memory leaks

---

## 📞 Support

**Service URL**: `https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io`

**Health Check**: `GET /health`

**Status**: ✅ Production Ready

---

**Last Updated**: December 2024  
**API Version**: 3.0.0 (FastAPI)

