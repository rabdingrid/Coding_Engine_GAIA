# Local Testing Guide

## 🎯 Why Test Locally First?

Testing locally helps you:
- ✅ Catch bugs before deploying to Azure
- ✅ Verify code execution works correctly
- ✅ Test test case comparison logic
- ✅ Save time and costs
- ✅ Debug more easily

---

## 🚀 Quick Start - Local Testing

### Step 1: Install Dependencies

```bash
cd aca-executor

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### Step 2: Run the Service Locally

```bash
# Run the executor service
python3 executor-service.py
```

**Expected output**:
```
 * Serving Flask app 'executor-service'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8000
 * Running on http://[your-ip]:8000
```

The service is now running on `http://localhost:8000`

---

### Step 3: Test Health Endpoint

**In a new terminal**:

```bash
curl http://localhost:8000/health
```

**Expected response**:
```json
{
  "status": "healthy",
  "service": "Code Execution Service",
  "replica": "unknown"
}
```

---

### Step 4: Test Code Execution (Simple)

```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "print(42)",
    "test_cases": [
      {
        "id": "test_1",
        "input": "",
        "expected_output": "42"
      }
    ],
    "user_id": "test_user",
    "question_id": "test_q1"
  }'
```

**Expected response**:
```json
{
  "execution_id": "...",
  "timestamp": "...",
  "user_id": "test_user",
  "question_id": "test_q1",
  "language": "python",
  "code": "print(42)",
  "summary": {
    "total_tests": 1,
    "passed": 1,
    "failed": 0,
    "all_passed": true,
    "pass_percentage": 100.0
  },
  "test_results": [
    {
      "test_case_id": "test_1",
      "test_case_number": 1,
      "input": "",
      "expected_output": "42",
      "actual_output": "42\n",
      "error": null,
      "status": "passed",
      "passed": true
    }
  ]
}
```

---

### Step 5: Test with Multiple Test Cases

```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "a = int(input())\nb = int(input())\nprint(a + b)",
    "test_cases": [
      {
        "id": "test_1",
        "input": "5\n10",
        "expected_output": "15"
      },
      {
        "id": "test_2",
        "input": "100\n200",
        "expected_output": "300"
      },
      {
        "id": "test_3",
        "input": "-5\n5",
        "expected_output": "0"
      }
    ],
    "user_id": "test_user",
    "question_id": "test_q1"
  }'
```

**Expected**: All 3 test cases should pass

---

### Step 6: Test Failed Case

```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "print(10)",
    "test_cases": [
      {
        "id": "test_1",
        "input": "",
        "expected_output": "20"
      }
    ],
    "user_id": "test_user",
    "question_id": "test_q1"
  }'
```

**Expected**: Test should fail (actual: "10", expected: "20")

---

### Step 7: Test Error Handling

**Test with syntax error**:

```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "print(10  # syntax error",
    "test_cases": [
      {
        "id": "test_1",
        "input": "",
        "expected_output": "10"
      }
    ],
    "user_id": "test_user",
    "question_id": "test_q1"
  }'
```

**Expected**: Should return error status

---

## 🧪 Test Different Languages

### JavaScript

```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "javascript",
    "code": "console.log(42)",
    "test_cases": [
      {
        "id": "test_1",
        "input": "",
        "expected_output": "42"
      }
    ],
    "user_id": "test_user",
    "question_id": "test_q1"
  }'
```

### Java

```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "java",
    "code": "public class Main { public static void main(String[] args) { System.out.println(42); } }",
    "test_cases": [
      {
        "id": "test_1",
        "input": "",
        "expected_output": "42"
      }
    ],
    "user_id": "test_user",
    "question_id": "test_q1"
  }'
```

### C++

```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "cpp",
    "code": "#include <iostream>\nint main() { std::cout << 42 << std::endl; return 0; }",
    "test_cases": [
      {
        "id": "test_1",
        "input": "",
        "expected_output": "42"
      }
    ],
    "user_id": "test_user",
    "question_id": "test_q1"
  }'
```

---

## 🐛 Debugging Tips

### Check Service Logs

The service prints logs to console. Watch for:
- Execution errors
- Timeout issues
- Resource limit violations

### Test Individual Functions

You can also test the executor functions directly in Python:

```python
from executor-service import execute_python, compare_outputs

# Test execution
result = execute_python("print(42)", "")
print(result)

# Test comparison
print(compare_outputs("42\n", "42"))  # Should be True
print(compare_outputs("42", "43"))    # Should be False
```

---

## ✅ Pre-Deployment Checklist

Before deploying to Azure, verify:

- [ ] Health endpoint returns 200
- [ ] Python code execution works
- [ ] JavaScript code execution works
- [ ] Java code execution works (if needed)
- [ ] C++ code execution works (if needed)
- [ ] Test case comparison works correctly
- [ ] Pass/fail logic works
- [ ] Error handling works (syntax errors, timeouts)
- [ ] Multiple test cases work
- [ ] Response structure is correct for database

---

## 🚀 After Local Testing

Once local testing passes:

1. **Build Docker image**:
   ```bash
   docker build -t aitaraacr1763805702.azurecr.io/executor-image:v1 .
   ```

2. **Test Docker image locally** (optional):
   ```bash
   docker run -p 8000:8000 aitaraacr1763805702.azurecr.io/executor-image:v1
   # Test with curl as above
   ```

3. **Push to ACR and deploy** (see DEPLOYMENT_GUIDE.md)

---

## 📋 Quick Test Script

Save this as `test_local.sh`:

```bash
#!/bin/bash

BASE_URL="http://localhost:8000"

echo "Testing Health Endpoint..."
curl -s $BASE_URL/health | python3 -m json.tool

echo -e "\n\nTesting Python Execution..."
curl -s -X POST $BASE_URL/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "print(42)",
    "test_cases": [
      {
        "id": "test_1",
        "input": "",
        "expected_output": "42"
      }
    ],
    "user_id": "test_user",
    "question_id": "test_q1"
  }' | python3 -m json.tool

echo -e "\n\nDone!"
```

**Run it**:
```bash
chmod +x test_local.sh
./test_local.sh
```

---

**Status**: Ready for local testing! ✅


