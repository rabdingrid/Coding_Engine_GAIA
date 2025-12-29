# 🔧 Troubleshooting 503 Error - Code Execution Service

## Problem
Your external backend (localhost:5000) is getting a **503 Service Unavailable** error when calling the code execution service.

## Root Causes

### 1. **Request Format Mismatch** ⚠️ **MOST LIKELY ISSUE**

Your external backend is sending:
```json
{
  "question_id": "22c620aa-b462-4ca5-adee-74ef95598862",
  "language": "cpp",
  "code": "...",
  "mode": "run"
}
```

But the FastAPI service expects:
```json
{
  "language": "cpp",
  "code": "...",
  "sample_test_cases": [
    {
      "id": "sample_1",
      "input": "5\n1 2 3 4 5\n2\n1 3\n2 4",
      "expected_output": "2\n3"
    }
  ],
  "user_id": "optional",
  "question_id": "optional"
}
```

### 2. **Service Not Running**
The code execution service might not be running or accessible.

### 3. **Wrong Service URL**
The external backend might be pointing to the wrong URL.

---

## ✅ Solution Steps

### Step 1: Check if Service is Running

**If running locally:**
```bash
# Check if service is running on port 8000
curl http://localhost:8000/health

# Or check Azure service
curl https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "Code Execution Service (FastAPI)",
  "version": "3.0.0"
}
```

### Step 2: Fix Request Format in External Backend

Your external backend needs to:

1. **Fetch test cases from database** using `question_id`
2. **Format request correctly** with `sample_test_cases` array
3. **Call the correct endpoint**

**Example Fix (Node.js/TypeScript):**
```typescript
// In your external backend (coding.api.ts or similar)
async function runCodeViaBackend(request: {
  question_id: string;
  language: string;
  code: string;
  mode: string;
}) {
  // 1. Fetch test cases from your database using question_id
  const question = await db.questions.findOne({ 
    where: { id: request.question_id } 
  });
  
  if (!question) {
    throw new Error('Question not found');
  }
  
  // 2. Format test cases for FastAPI
  const sampleTestCases = question.sample_test_cases.map((tc, idx) => ({
    id: tc.id || `sample_${idx + 1}`,
    input: tc.input,
    expected_output: tc.expected_output
  }));
  
  // 3. Call FastAPI service with correct format
  const executorServiceUrl = process.env.EXECUTOR_SERVICE_URL || 
    'https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io';
  
  const response = await fetch(`${executorServiceUrl}/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      language: request.language,
      code: request.code,
      sample_test_cases: sampleTestCases,  // ✅ Required!
      user_id: request.user_id || 'anonymous',
      question_id: request.question_id
    })
  });
  
  if (!response.ok) {
    if (response.status === 503) {
      throw new Error('Code execution service is currently unavailable. Please try again later.');
    }
    const error = await response.json();
    throw new Error(error.detail || 'Code execution failed');
  }
  
  return await response.json();
}
```

**Example Fix (Python/Flask):**
```python
import requests
import os

def run_code_via_backend(question_id, language, code, user_id=None):
    # 1. Fetch test cases from database
    question = db.session.query(Question).filter_by(id=question_id).first()
    if not question:
        raise ValueError('Question not found')
    
    # 2. Format test cases
    sample_test_cases = [
        {
            'id': tc.id or f'sample_{i+1}',
            'input': tc.input,
            'expected_output': tc.expected_output
        }
        for i, tc in enumerate(question.sample_test_cases)
    ]
    
    # 3. Call FastAPI service
    executor_url = os.getenv('EXECUTOR_SERVICE_URL', 
        'https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io')
    
    try:
        response = requests.post(
            f'{executor_url}/run',
            json={
                'language': language,
                'code': code,
                'sample_test_cases': sample_test_cases,  # ✅ Required!
                'user_id': user_id or 'anonymous',
                'question_id': question_id
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 503:
            raise Exception('Code execution service is currently unavailable. Please try again later.')
        raise
```

### Step 3: Configure Service URL

Set the environment variable in your external backend:

```bash
# .env file or environment variables
EXECUTOR_SERVICE_URL=https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io

# Or for local development:
EXECUTOR_SERVICE_URL=http://localhost:8000
```

### Step 4: Handle Different Modes

If your external backend uses `mode: "run"` vs `mode: "runall"`:

```typescript
async function runCodeViaBackend(request: {
  question_id: string;
  language: string;
  code: string;
  mode: 'run' | 'runall' | 'submit';
}) {
  const question = await fetchQuestion(request.question_id);
  
  const executorUrl = process.env.EXECUTOR_SERVICE_URL;
  
  if (request.mode === 'run') {
    // Use /run endpoint with sample_test_cases
    return await fetch(`${executorUrl}/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        language: request.language,
        code: request.code,
        sample_test_cases: question.sample_test_cases.map(...),
        question_id: request.question_id
      })
    });
  } else if (request.mode === 'runall') {
    // Use /runall endpoint with test_cases (excluding sample)
    return await fetch(`${executorUrl}/runall`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        language: request.language,
        code: request.code,
        test_cases: question.test_cases.filter(tc => !tc.is_sample).map(...),
        sample_test_cases: [],  // Optional, for reference
        question_id: request.question_id
      })
    });
  } else if (request.mode === 'submit') {
    // Use /submit endpoint with all test_cases
    return await fetch(`${executorUrl}/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        language: request.language,
        code: request.code,
        test_cases: question.test_cases.map(...),
        user_id: request.user_id,  // Required for submit
        question_id: request.question_id
      })
    });
  }
}
```

---

## 🔍 Diagnostic Commands

Run these to diagnose the issue:

```bash
# 1. Check if Azure service is accessible
curl -v https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/health

# 2. Test with correct request format
curl -X POST https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/run \
  -H "Content-Type: application/json" \
  -d '{
    "language": "cpp",
    "code": "#include <iostream>\nint main() { std::cout << \"Hello\"; return 0; }",
    "sample_test_cases": [
      {"id": "test1", "input": "", "expected_output": "Hello"}
    ]
  }'

# 3. Check external backend logs
# Look for the actual URL being called and error details
```

---

## 📋 Checklist

- [ ] Code execution service is running and accessible
- [ ] External backend fetches test cases from database using `question_id`
- [ ] Request includes `sample_test_cases` array (required for `/run`)
- [ ] Service URL is correctly configured (`EXECUTOR_SERVICE_URL`)
- [ ] Error handling for 503 errors is implemented
- [ ] Request timeout is set appropriately (30-60 seconds)

---

## 🚨 Common Mistakes

1. **Missing `sample_test_cases`**: FastAPI will return 400 Bad Request, not 503
2. **Wrong endpoint**: Using `/run` without test cases → 400
3. **Service not running**: Returns 503 or connection refused
4. **Timeout too short**: Large code execution times out → 503
5. **CORS issues**: Check CORS headers (should be `*` already configured)

---

## 📞 Need More Help?

If the issue persists:
1. Check external backend logs for the exact error
2. Verify the service URL is correct
3. Test the service directly with curl (see diagnostic commands)
4. Check if test cases exist in database for the given `question_id`



