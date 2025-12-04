# File-Based Test Cases Support

## ✅ Enhanced Executor with File-Based Test Cases

The executor now supports **both string-based and file-based test cases**!

---

## 📋 Supported Test Case Formats

### 1. **String-Based** (Original)
```json
{
  "language": "python",
  "code": "a = int(input())\nb = int(input())\nprint(a + b)",
  "test_cases": [
    {
      "id": "test_1",
      "input": "5\n10",
      "expected_output": "15"
    }
  ]
}
```

### 2. **File-Based** (New)
```json
{
  "language": "python",
  "code": "a = int(input())\nb = int(input())\nprint(a + b)",
  "test_cases": [
    {
      "id": "test_1",
      "input_file": "/app/test_cases/input1.txt",
      "expected_output_file": "/app/test_cases/output1.txt"
    }
  ]
}
```

### 3. **Mixed** (Input from file, output as string)
```json
{
  "language": "python",
  "code": "n = int(input())\nfor i in range(n):\n    print('Hello')",
  "test_cases": [
    {
      "id": "test_1",
      "input_file": "/app/test_cases/input1.txt",
      "expected_output": "Hello\nHello\nHello\nHello\nHello"
    }
  ]
}
```

### 4. **Mixed** (Input as string, output from file)
```json
{
  "language": "python",
  "code": "print('Hello World')",
  "test_cases": [
    {
      "id": "test_1",
      "input": "",
      "expected_output_file": "/app/test_cases/output1.txt"
    }
  ]
}
```

---

## 🔒 Security

**File Access Restrictions**:
- ✅ Only allows reading from:
  - `/app/test_cases/` - Test case files directory
  - `/tmp/` - Temporary files
- ❌ Blocks access to other directories
- ✅ Validates file paths before reading

---

## 📁 Directory Structure

```
/app/
├── executor-service.py
├── executor-service-secure.py
├── requirements.txt
└── test_cases/          # Test case files directory
    ├── input1.txt
    ├── output1.txt
    ├── input2.txt
    ├── output2.txt
    └── ...
```

---

## 🚀 Usage Examples

### Example 1: Using File-Based Test Cases

```bash
curl -X POST "https://ai-ta-ra-code-executor2.../execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "n = int(input())\nfor i in range(n):\n    print(\"Hello\")",
    "test_cases": [
      {
        "id": "test_1",
        "input_file": "/app/test_cases/input1.txt",
        "expected_output_file": "/app/test_cases/output1.txt"
      }
    ],
    "user_id": "user123",
    "question_id": "q1"
  }'
```

### Example 2: Multiple File-Based Test Cases

```json
{
  "language": "python",
  "code": "a = int(input())\nb = int(input())\nprint(a + b)",
  "test_cases": [
    {
      "id": "test_1",
      "input_file": "/app/test_cases/input1.txt",
      "expected_output_file": "/app/test_cases/output1.txt"
    },
    {
      "id": "test_2",
      "input_file": "/app/test_cases/input2.txt",
      "expected_output_file": "/app/test_cases/output2.txt"
    },
    {
      "id": "test_3",
      "input_file": "/app/test_cases/input3.txt",
      "expected_output_file": "/app/test_cases/output3.txt"
    }
  ]
}
```

---

## 📊 Response Format

The response format remains the same, whether using file-based or string-based test cases:

```json
{
  "execution_id": "uuid",
  "timestamp": "2025-11-28T12:00:00",
  "user_id": "user123",
  "question_id": "q1",
  "language": "python",
  "code": "...",
  "summary": {
    "total_tests": 3,
    "passed": 2,
    "failed": 1,
    "all_passed": false,
    "pass_percentage": 66.67
  },
  "test_results": [
    {
      "test_case_id": "test_1",
      "test_case_number": 1,
      "input": "5\n",  // Content from input file
      "expected_output": "Hello\nHello\n...",  // Content from output file
      "actual_output": "Hello\nHello\n...",
      "error": null,
      "status": "passed",
      "passed": true
    }
  ]
}
```

**Note**: The `input` and `expected_output` fields in the response will contain the actual content (read from files if file-based).

---

## 🔧 How It Works

1. **Test Case Processing**:
   - Checks for `input_file` → reads from file if present
   - Falls back to `input` string if no file
   - Same for `expected_output_file` vs `expected_output`

2. **File Reading**:
   - Validates file path (security check)
   - Reads file content
   - Handles errors gracefully

3. **Execution**:
   - Uses file content as stdin for code execution
   - Compares actual output with expected (from file or string)

---

## ✅ Benefits

1. **Easier Management**: Store test cases in files instead of JSON
2. **Reusability**: Same test case files can be used across different requests
3. **Large Test Cases**: Handle large input/output without bloating JSON
4. **Version Control**: Test case files can be versioned separately
5. **Flexibility**: Mix file-based and string-based test cases

---

## 🧪 Testing

### Test with File-Based Test Cases

```bash
# Upload test case files to container first
# Then use file paths in test cases
curl -X POST "http://localhost:8001/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "n = int(input())\nfor i in range(n):\n    print(\"Hello\")",
    "test_cases": [
      {
        "id": "test_1",
        "input_file": "/app/test_cases/input1.txt",
        "expected_output_file": "/app/test_cases/output1.txt"
      }
    ]
  }'
```

---

## 📝 Notes

- **File paths must be absolute** (e.g., `/app/test_cases/input1.txt`)
- **Relative paths** starting with `./test_cases/` are automatically converted to `/app/test_cases/`
- **File reading is secure** - only allows access to `/app/test_cases/` and `/tmp/`
- **Both formats work** - you can mix file-based and string-based in the same request

---

**Status**: ✅ **Fully Implemented and Tested**


