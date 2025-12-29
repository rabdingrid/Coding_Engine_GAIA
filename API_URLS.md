# 🌐 Complete API URLs - Code Execution Service

## Base URL
```
https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io
```

---

## 📋 Full Endpoint URLs

### 1. **Health Check**
```
GET https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/health
```

**Quick Test:**
```bash
curl https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/health
```

---

### 2. **Run Code (Single Test Case)**
```
POST https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/run
```

**Full cURL Example:**
```bash
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
```

**JavaScript Example:**
```javascript
const response = await fetch(
  'https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/run',
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      language: 'python',
      code: 'def solve(n):\n    return n * 2\n\nn = int(input())\nprint(solve(n))',
      sample_test_cases: [
        { id: 'sample_1', input: '5', expected_output: '10' }
      ],
      user_id: 'user123',
      question_id: 'q1'
    })
  }
);
const result = await response.json();
```

**Python Example:**
```python
import requests

url = 'https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/run'
response = requests.post(url, json={
    'language': 'python',
    'code': 'def solve(n):\n    return n * 2\n\nn = int(input())\nprint(solve(n))',
    'sample_test_cases': [
        {'id': 'sample_1', 'input': '5', 'expected_output': '10'}
    ],
    'user_id': 'user123',
    'question_id': 'q1'
})
result = response.json()
```

---

### 3. **Run All Test Cases**
```
POST https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/runall
```

**Full cURL Example:**
```bash
curl -X POST https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/runall \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "def solve(n):\n    return n * 2\n\nn = int(input())\nprint(solve(n))",
    "test_cases": [
      {"id": "test_1", "input": "5", "expected_output": "10"},
      {"id": "test_2", "input": "10", "expected_output": "20"},
      {"id": "test_3", "input": "100", "expected_output": "200"}
    ],
    "user_id": "user123",
    "question_id": "q1"
  }'
```

**JavaScript Example:**
```javascript
const response = await fetch(
  'https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/runall',
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      language: 'python',
      code: 'def solve(n):\n    return n * 2\n\nn = int(input())\nprint(solve(n))',
      test_cases: [
        { id: 'test_1', input: '5', expected_output: '10' },
        { id: 'test_2', input: '10', expected_output: '20' },
        { id: 'test_3', input: '100', expected_output: '200' }
      ],
      user_id: 'user123',
      question_id: 'q1'
    })
  }
);
const result = await response.json();
```

**Python Example:**
```python
import requests

url = 'https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/runall'
response = requests.post(url, json={
    'language': 'python',
    'code': 'def solve(n):\n    return n * 2\n\nn = int(input())\nprint(solve(n))',
    'test_cases': [
        {'id': 'test_1', 'input': '5', 'expected_output': '10'},
        {'id': 'test_2', 'input': '10', 'expected_output': '20'},
        {'id': 'test_3', 'input': '100', 'expected_output': '200'}
    ],
    'user_id': 'user123',
    'question_id': 'q1'
})
result = response.json()
```

---

### 4. **Submit Final Code**
```
POST https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/submit
```

**Full cURL Example:**
```bash
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

## 🔗 Quick Reference

| Endpoint | Method | Full URL |
|----------|--------|----------|
| Health Check | GET | `https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/health` |
| Run (Single) | POST | `https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/run` |
| Run All | POST | `https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/runall` |
| Submit | POST | `https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/submit` |

---

## 📝 Notes

- **All endpoints use HTTPS** (secure connection)
- **Content-Type**: `application/json` required
- **Rate Limits**: 
  - `/run`: 50 requests/minute
  - `/runall`: 1000 requests/minute
  - `/submit`: 200 requests/minute

---

**Last Updated**: December 5, 2024




