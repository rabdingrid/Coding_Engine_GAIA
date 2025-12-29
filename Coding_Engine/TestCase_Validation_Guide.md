# Test Case Validation with Azure Dynamic Sessions

## 🎯 Overview

Azure Dynamic Sessions **does NOT have built-in test case validation**. You need to implement this logic in your **backend** or **frontend**. This is actually a **good thing** because it gives you full control over how test cases are validated.

---

## 🔍 How Test Case Validation Works

### **Architecture:**

```
┌─────────────────────────────────────────────────────────┐
│                    Your Backend                         │
│                                                         │
│  1. Receive user code + test cases                     │
│  2. For each test case:                                │
│     a. Send code + input to Azure Dynamic Sessions     │
│     b. Get output from execution                       │
│     c. Compare output with expected output             │
│     d. Mark test case as pass/fail                     │
│  3. Return results to frontend                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📝 Implementation Options

### **Option 1: Backend Validation (Recommended)**

The backend runs all test cases and validates them before returning results.

#### **Flow:**
```
User submits code
  ↓
Backend receives: {code, testCases: [{input, expectedOutput}]}
  ↓
For each test case:
  - Execute code with test input
  - Get actual output
  - Compare with expected output
  - Record pass/fail
  ↓
Return: {testResults: [{passed: true/false, input, expected, actual}]}
```

#### **Implementation:**

```python
# backend/executor.py

from typing import List
from models import ExecuteRequest, TestCase, TestResult

def validate_test_cases(code: str, language: str, test_cases: List[TestCase]) -> List[TestResult]:
    """
    Execute code against multiple test cases and validate outputs.
    """
    results = []
    
    for i, test_case in enumerate(test_cases):
        # Create execution request with test input
        request = ExecuteRequest(
            language=language,
            version="3.10.0",
            files=[{"name": "main.py", "content": code}],
            stdin=test_case.input  # Provide test input via stdin
        )
        
        # Execute code in Azure Dynamic Sessions
        response = execute_code_in_session(request)
        
        # Get actual output
        actual_output = response.run.stdout.strip()
        expected_output = test_case.expected_output.strip()
        
        # Compare outputs
        passed = actual_output == expected_output
        
        # Record result
        results.append(TestResult(
            test_case_id=i + 1,
            input=test_case.input,
            expected_output=expected_output,
            actual_output=actual_output,
            passed=passed,
            execution_time=response.run.execution_time,
            error=response.run.stderr if response.run.code != 0 else None
        ))
    
    return results
```

#### **Updated Models:**

```python
# backend/models.py

from pydantic import BaseModel
from typing import List, Optional

class TestCase(BaseModel):
    input: str
    expected_output: str
    is_sample: bool = False  # Mark sample test cases

class TestResult(BaseModel):
    test_case_id: int
    input: str
    expected_output: str
    actual_output: str
    passed: bool
    execution_time: Optional[float] = None
    error: Optional[str] = None

class ValidateRequest(BaseModel):
    language: str
    version: str
    code: str
    test_cases: List[TestCase]

class ValidateResponse(BaseModel):
    total_tests: int
    passed_tests: int
    failed_tests: int
    test_results: List[TestResult]
    all_passed: bool
```

#### **New API Endpoint:**

```python
# backend/main.py

@app.post("/api/v2/validate", response_model=ValidateResponse)
def validate_code(request: ValidateRequest):
    """
    Validate user code against multiple test cases.
    """
    # Execute code against all test cases
    test_results = validate_test_cases(
        code=request.code,
        language=request.language,
        test_cases=request.test_cases
    )
    
    # Calculate summary
    total_tests = len(test_results)
    passed_tests = sum(1 for r in test_results if r.passed)
    failed_tests = total_tests - passed_tests
    
    return ValidateResponse(
        total_tests=total_tests,
        passed_tests=passed_tests,
        failed_tests=failed_tests,
        test_results=test_results,
        all_passed=passed_tests == total_tests
    )
```

---

### **Option 2: Frontend Validation**

The frontend runs test cases one by one and validates locally.

#### **Flow:**
```
User submits code
  ↓
Frontend loops through test cases:
  - Call /api/v2/execute with test input
  - Get output
  - Compare with expected output locally
  - Display pass/fail
  ↓
Show results to user
```

#### **Implementation:**

```javascript
// frontend/app.js

async function validateCode(code, language, testCases) {
    const results = [];
    
    for (const testCase of testCases) {
        // Execute code with test input
        const response = await fetch(`${apiUrl}/api/v2/execute`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                language: language,
                version: '3.10.0',
                files: [{name: 'main.py', content: code}],
                stdin: testCase.input
            })
        });
        
        const result = await response.json();
        
        // Compare outputs
        const actualOutput = result.run.stdout.trim();
        const expectedOutput = testCase.expectedOutput.trim();
        const passed = actualOutput === expectedOutput;
        
        results.push({
            testCaseId: testCase.id,
            input: testCase.input,
            expectedOutput: expectedOutput,
            actualOutput: actualOutput,
            passed: passed,
            error: result.run.stderr
        });
    }
    
    return results;
}
```

---

## 🎮 HackerRank-Style Test Case System

### **Database Schema:**

```sql
-- Problems table
CREATE TABLE problems (
    id INT PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    difficulty ENUM('easy', 'medium', 'hard'),
    time_limit INT,  -- milliseconds
    memory_limit INT  -- MB
);

-- Test cases table
CREATE TABLE test_cases (
    id INT PRIMARY KEY,
    problem_id INT,
    input TEXT,
    expected_output TEXT,
    is_sample BOOLEAN,  -- Show to user or hidden
    points INT,  -- Points for this test case
    FOREIGN KEY (problem_id) REFERENCES problems(id)
);

-- Submissions table
CREATE TABLE submissions (
    id INT PRIMARY KEY,
    user_id INT,
    problem_id INT,
    code TEXT,
    language VARCHAR(50),
    status ENUM('pending', 'running', 'accepted', 'wrong_answer', 'timeout', 'error'),
    score INT,
    submitted_at TIMESTAMP
);

-- Test results table
CREATE TABLE test_results (
    id INT PRIMARY KEY,
    submission_id INT,
    test_case_id INT,
    passed BOOLEAN,
    actual_output TEXT,
    execution_time INT,  -- milliseconds
    error_message TEXT,
    FOREIGN KEY (submission_id) REFERENCES submissions(id),
    FOREIGN KEY (test_case_id) REFERENCES test_cases(id)
);
```

---

### **Complete Validation Flow:**

```python
# backend/validator.py

from typing import List, Tuple
from models import Problem, TestCase, Submission, TestResult
from executor import execute_code_in_session

class CodeValidator:
    def __init__(self, problem: Problem):
        self.problem = problem
        self.test_cases = self.load_test_cases(problem.id)
    
    def load_test_cases(self, problem_id: int) -> List[TestCase]:
        """Load test cases from database."""
        # Query database for test cases
        return db.query(TestCase).filter(
            TestCase.problem_id == problem_id
        ).all()
    
    def validate_submission(self, code: str, language: str) -> Tuple[str, int, List[TestResult]]:
        """
        Validate user submission against all test cases.
        
        Returns:
            status: 'accepted', 'wrong_answer', 'timeout', 'error'
            score: Total points earned
            results: List of test results
        """
        results = []
        total_score = 0
        max_score = sum(tc.points for tc in self.test_cases)
        
        for test_case in self.test_cases:
            # Execute code with test input
            try:
                response = execute_code_in_session(
                    code=code,
                    language=language,
                    stdin=test_case.input,
                    timeout=self.problem.time_limit
                )
                
                # Check for runtime errors
                if response.run.code != 0:
                    result = TestResult(
                        test_case_id=test_case.id,
                        passed=False,
                        actual_output=response.run.stdout,
                        error_message=response.run.stderr
                    )
                    results.append(result)
                    continue
                
                # Check for timeout
                if response.run.execution_time > self.problem.time_limit:
                    result = TestResult(
                        test_case_id=test_case.id,
                        passed=False,
                        actual_output=response.run.stdout,
                        error_message="Time Limit Exceeded"
                    )
                    results.append(result)
                    continue
                
                # Compare outputs
                actual = self.normalize_output(response.run.stdout)
                expected = self.normalize_output(test_case.expected_output)
                passed = actual == expected
                
                # Record result
                result = TestResult(
                    test_case_id=test_case.id,
                    passed=passed,
                    actual_output=response.run.stdout,
                    execution_time=response.run.execution_time
                )
                results.append(result)
                
                # Add points if passed
                if passed:
                    total_score += test_case.points
                
            except Exception as e:
                result = TestResult(
                    test_case_id=test_case.id,
                    passed=False,
                    error_message=str(e)
                )
                results.append(result)
        
        # Determine overall status
        if total_score == max_score:
            status = 'accepted'
        elif any(r.error_message == "Time Limit Exceeded" for r in results):
            status = 'timeout'
        elif any(r.error_message for r in results):
            status = 'error'
        else:
            status = 'wrong_answer'
        
        return status, total_score, results
    
    def normalize_output(self, output: str) -> str:
        """
        Normalize output for comparison.
        - Strip leading/trailing whitespace
        - Normalize line endings
        - Remove trailing spaces on each line
        """
        lines = output.strip().split('\n')
        normalized = [line.rstrip() for line in lines]
        return '\n'.join(normalized)
```

---

## 📊 Example: Two Sum Problem

### **Problem Definition:**

```json
{
  "id": 1,
  "title": "Two Sum",
  "description": "Given an array of integers and a target, return indices of two numbers that add up to target.",
  "difficulty": "easy",
  "time_limit": 1000,
  "memory_limit": 128,
  "test_cases": [
    {
      "id": 1,
      "input": "4\n2 7 11 15\n9",
      "expected_output": "0 1",
      "is_sample": true,
      "points": 10
    },
    {
      "id": 2,
      "input": "3\n3 2 4\n6",
      "expected_output": "1 2",
      "is_sample": true,
      "points": 10
    },
    {
      "id": 3,
      "input": "5\n1 5 3 7 9\n10",
      "expected_output": "1 3",
      "is_sample": false,
      "points": 20
    },
    {
      "id": 4,
      "input": "6\n10 20 30 40 50 60\n90",
      "expected_output": "3 4",
      "is_sample": false,
      "points": 20
    }
  ]
}
```

### **User Submission:**

```python
# User's code
n = int(input())
nums = list(map(int, input().split()))
target = int(input())

# Two Sum solution
seen = {}
for i, num in enumerate(nums):
    complement = target - num
    if complement in seen:
        print(seen[complement], i)
        break
    seen[num] = i
```

### **Validation Process:**

```
Test Case 1 (Sample):
  Input: "4\n2 7 11 15\n9"
  Expected: "0 1"
  Actual: "0 1"
  Result: ✅ PASS (10 points)

Test Case 2 (Sample):
  Input: "3\n3 2 4\n6"
  Expected: "1 2"
  Actual: "1 2"
  Result: ✅ PASS (10 points)

Test Case 3 (Hidden):
  Input: "5\n1 5 3 7 9\n10"
  Expected: "1 3"
  Actual: "1 3"
  Result: ✅ PASS (20 points)

Test Case 4 (Hidden):
  Input: "6\n10 20 30 40 50 60\n90"
  Expected: "3 4"
  Actual: "3 4"
  Result: ✅ PASS (20 points)

Final Score: 60/60 points
Status: ACCEPTED ✅
```

---

## 🔧 Advanced Validation Features

### **1. Fuzzy Output Matching**

For problems where output format may vary:

```python
def fuzzy_compare(actual: str, expected: str, tolerance: float = 1e-6) -> bool:
    """
    Compare outputs with tolerance for floating-point numbers.
    """
    actual_lines = actual.strip().split('\n')
    expected_lines = expected.strip().split('\n')
    
    if len(actual_lines) != len(expected_lines):
        return False
    
    for actual_line, expected_line in zip(actual_lines, expected_lines):
        # Try to parse as floats
        try:
            actual_num = float(actual_line)
            expected_num = float(expected_line)
            if abs(actual_num - expected_num) > tolerance:
                return False
        except ValueError:
            # Not a number, do exact string comparison
            if actual_line.strip() != expected_line.strip():
                return False
    
    return True
```

### **2. Custom Validators**

For problems with multiple correct answers:

```python
def validate_graph_output(actual: str, expected: str, graph_data: dict) -> bool:
    """
    Custom validator for graph problems where multiple solutions exist.
    """
    # Parse actual output
    actual_edges = parse_edges(actual)
    
    # Validate that it forms a valid spanning tree
    if not is_valid_spanning_tree(actual_edges, graph_data):
        return False
    
    # Check total weight (for MST problems)
    actual_weight = sum(edge.weight for edge in actual_edges)
    expected_weight = sum(edge.weight for edge in parse_edges(expected))
    
    return actual_weight == expected_weight
```

### **3. Partial Credit**

For problems with multiple test case groups:

```python
test_case_groups = [
    {"name": "Basic", "cases": [1, 2], "points": 20},
    {"name": "Medium", "cases": [3, 4, 5], "points": 30},
    {"name": "Hard", "cases": [6, 7, 8, 9, 10], "points": 50}
]

def calculate_score(test_results: List[TestResult]) -> int:
    score = 0
    for group in test_case_groups:
        # Check if all tests in group passed
        group_passed = all(
            test_results[i-1].passed for i in group["cases"]
        )
        if group_passed:
            score += group["points"]
    return score
```

---

## 📈 Performance Optimization

### **Parallel Test Execution:**

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def validate_test_cases_parallel(code: str, language: str, test_cases: List[TestCase]) -> List[TestResult]:
    """
    Execute test cases in parallel for faster validation.
    """
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for test_case in test_cases:
            future = executor.submit(
                execute_single_test_case,
                code, language, test_case
            )
            futures.append(future)
        
        # Wait for all to complete
        results = [future.result() for future in futures]
    
    return results
```

**Benefits:**
- 5x faster validation (5 test cases in parallel)
- Better user experience (faster feedback)
- Efficient use of Azure Dynamic Sessions

---

## 🎯 Summary

### **Key Points:**

1. **Azure Dynamic Sessions does NOT validate test cases** - you implement this logic
2. **Backend validation is recommended** - more secure, consistent
3. **Store test cases in database** - separate sample vs hidden tests
4. **Normalize outputs** - handle whitespace, line endings
5. **Support custom validators** - for problems with multiple solutions
6. **Implement partial credit** - group test cases by difficulty
7. **Run tests in parallel** - faster validation

### **Implementation Checklist:**

- [ ] Create test case database schema
- [ ] Implement backend validation endpoint
- [ ] Add output normalization logic
- [ ] Support fuzzy matching (for floats)
- [ ] Implement custom validators (if needed)
- [ ] Add partial credit system
- [ ] Optimize with parallel execution
- [ ] Add timeout handling
- [ ] Track execution time per test
- [ ] Store submission history

---

**Created:** November 24, 2025  
**Purpose:** Guide for implementing test case validation with Azure Dynamic Sessions
