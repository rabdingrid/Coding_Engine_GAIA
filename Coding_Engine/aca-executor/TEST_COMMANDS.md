# Test Commands - Public Access

## 🚀 Quick Test Commands for Deployed Service

**Service URL**: `https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io`

---

## 1. Health Check

```bash
curl https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/health
```

**Expected Response**:
```json
{
  "status": "healthy",
  "service": "Code Execution Service",
  "replica": "unknown"
}
```

---

## 2. Service Info (Root Endpoint)

```bash
curl https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/
```

**Expected Response**:
```json
{
  "service": "Code Execution Service with Test Cases",
  "version": "2.0.0",
  "status": "running",
  "supported_languages": ["python", "javascript", "java", "cpp"]
}
```

---

## 3. Simple Python Execution (Should Pass)

```bash
curl -X POST "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/execute" \
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

**Expected**: `"all_passed": true`, `"passed": 1`

---

## 4. Multiple Test Cases (Should Pass All)

```bash
curl -X POST "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/execute" \
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

**Expected**: `"all_passed": true`, `"passed": 3`

---

## 5. Failed Test Case (Should Fail)

```bash
curl -X POST "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/execute" \
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

**Expected**: `"all_passed": false`, `"failed": 1`

---

## 6. Security Test - Blocked Import (Should Block)

```bash
curl -X POST "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "import os; print(os.getcwd())",
    "test_cases": [
      {
        "id": "test_1",
        "input": "",
        "expected_output": ""
      }
    ],
    "user_id": "test_user",
    "question_id": "test_q1"
  }'
```

**Expected**: Error - `"Code validation failed: Blocked pattern detected: import\\s+os\\b"`

---

## 7. Security Test - Blocked Function (Should Block)

```bash
curl -X POST "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "eval(\"print(42)\")",
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

**Expected**: Error - `"Code validation failed: Blocked pattern detected: eval\\s*\\("`

---

## 8. Security Test - Network Operations (Should Block)

```bash
curl -X POST "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "import requests; print(requests.get(\"https://google.com\"))",
    "test_cases": [
      {
        "id": "test_1",
        "input": "",
        "expected_output": ""
      }
    ],
    "user_id": "test_user",
    "question_id": "test_q1"
  }'
```

**Expected**: Error - `"Network operations not allowed"`

---

## 9. JavaScript Execution

```bash
curl -X POST "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/execute" \
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

**Expected**: `"all_passed": true`

---

## 10. Java Execution

```bash
curl -X POST "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/execute" \
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

**Expected**: `"all_passed": true`

---

## 11. C++ Execution

```bash
curl -X POST "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/execute" \
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

**Expected**: `"all_passed": true`

---

## 12. Syntax Error Handling

```bash
curl -X POST "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/execute" \
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

**Expected**: `"status": "error"`, SyntaxError in error field

---

## 13. Timeout Test

```bash
curl -X POST "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "import time; time.sleep(10); print(42)",
    "test_cases": [
      {
        "id": "test_1",
        "input": "",
        "expected_output": "42"
      }
    ],
    "timeout": 6,
    "user_id": "test_user",
    "question_id": "test_q1"
  }'
```

**Expected**: `"status": "error"`, Timeout error

---

## 14. Complex Problem - Array Sum

```bash
curl -X POST "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "n = int(input())\narr = list(map(int, input().split()))\nprint(sum(arr))",
    "test_cases": [
      {
        "id": "test_1",
        "input": "5\n1 2 3 4 5",
        "expected_output": "15"
      },
      {
        "id": "test_2",
        "input": "3\n10 20 30",
        "expected_output": "60"
      }
    ],
    "user_id": "test_user",
    "question_id": "array_sum"
  }'
```

**Expected**: `"all_passed": true`, `"passed": 2`

---

## 15. Pretty Print (with jq)

### Health Check (Pretty):
```bash
curl -s https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/health | jq
```

### Code Execution (Pretty):
```bash
curl -s -X POST "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "print(42)",
    "test_cases": [{"id": "test_1", "input": "", "expected_output": "42"}],
    "user_id": "test",
    "question_id": "test"
  }' | jq
```

---

## 16. Python Format (with python3 -m json.tool)

```bash
curl -s -X POST "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "print(42)",
    "test_cases": [{"id": "test_1", "input": "", "expected_output": "42"}],
    "user_id": "test",
    "question_id": "test"
  }' | python3 -m json.tool
```

---

## 📋 Quick Reference

### Service URL:
```
https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io
```

### Endpoints:
- **Health**: `GET /health`
- **Info**: `GET /`
- **Execute**: `POST /execute`

### Supported Languages:
- `python` / `py`
- `javascript` / `js` / `node`
- `java`
- `cpp` / `c++`

### Test Case Format:
```json
{
  "id": "test_1",
  "input": "input string",
  "expected_output": "expected output"
}
```

---

## 🧪 Test Scenarios

| # | Test | Expected Result |
|---|------|----------------|
| 1 | Health Check | ✅ Healthy |
| 2 | Simple Execution | ✅ Pass |
| 3 | Multiple Test Cases | ✅ All Pass |
| 4 | Failed Test | ❌ Fail (correct) |
| 5 | Blocked Import | 🚫 Blocked |
| 6 | Blocked Function | 🚫 Blocked |
| 7 | Network Operations | 🚫 Blocked |
| 8 | JavaScript | ✅ Pass |
| 9 | Java | ✅ Pass |
| 10 | C++ | ✅ Pass |
| 11 | Syntax Error | ⚠️ Error |
| 12 | Timeout | ⚠️ Timeout |

---

## 💡 Tips

1. **Use `-s` flag** to silence progress: `curl -s ...`
2. **Use `jq` or `python3 -m json.tool`** for pretty JSON output
3. **Save responses** to file: `curl ... > response.json`
4. **Test from different locations** to verify public access
5. **Check rate limiting** by sending many rapid requests

---

**Last Updated**: 2025-11-28  
**Service Status**: ✅ **DEPLOYED AND WORKING**
