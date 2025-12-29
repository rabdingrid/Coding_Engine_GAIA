# ✅ Simple Question Test Results

## Question: Sum of Two Numbers

### Test Results

**Status:** ✅ **ALL TESTS PASSED**

| Test Case | Input | Expected | Actual | Status | Time |
|-----------|-------|----------|--------|--------|------|
| sample_1 | `5\n3` | `8` | `8` | ✅ Passed | 22ms |
| sample_2 | `10\n20` | `30` | `30` | ✅ Passed | 17ms |

### Performance Summary

- **Total Tests:** 2
- **Passed:** 2 (100%)
- **Failed:** 0
- **Total Execution Time:** 40ms
- **Average per Test:** 19.5ms

### Code Used

```python
def add(a, b):
    return a + b

a = int(input())
b = int(input())
result = add(a, b)
print(result)
```

---

## 📋 Quick Reference

### Request Format for `/run` endpoint:

```json
{
  "language": "python",
  "code": "def add(a, b):\n    return a + b\n\na = int(input())\nb = int(input())\nresult = add(a, b)\nprint(result)",
  "sample_test_cases": [
    {"id": "sample_1", "input": "5\n3", "expected_output": "8"},
    {"id": "sample_2", "input": "10\n20", "expected_output": "30"}
  ],
  "question_id": "simple_sum",
  "user_id": "test_user"
}
```

### Request Format for `/runall` endpoint:

```json
{
  "language": "python",
  "code": "def add(a, b):\n    return a + b\n\na = int(input())\nb = int(input())\nresult = add(a, b)\nprint(result)",
  "test_cases": [
    {"id": "test_1", "input": "1\n1", "expected_output": "2"},
    {"id": "test_2", "input": "0\n0", "expected_output": "0"},
    {"id": "test_3", "input": "-5\n5", "expected_output": "0"},
    {"id": "test_4", "input": "100\n200", "expected_output": "300"},
    {"id": "test_5", "input": "-10\n-20", "expected_output": "-30"}
  ],
  "sample_test_cases": [],
  "question_id": "simple_sum",
  "user_id": "test_user"
}
```

---

## 🚀 Ready to Use!

This simple question is perfect for:
- ✅ Testing API endpoints
- ✅ Demonstrating functionality
- ✅ Quick performance benchmarks
- ✅ Learning the API format

**Files Created:**
- `simple-question-example.json` - Complete question structure
- `test-simple-question.sh` - Test script
- `SIMPLE_QUESTION_EXAMPLES.md` - Documentation with more examples


