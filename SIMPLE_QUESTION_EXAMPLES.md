# 📝 Simple Coding Questions with Test Cases

## Question 1: Sum of Two Numbers

### Problem Description
Write a function that takes two integers and returns their sum.

### Input Format
Two integers, one per line.

### Output Format
Print the sum of the two integers.

### Example
**Input:**
```
5
3
```

**Output:**
```
8
```

---

## 📋 Test Cases

### Sample Test Cases (for `/run` endpoint)

```json
{
  "sample_test_cases": [
    {
      "id": "sample_1",
      "input": "5\n3",
      "expected_output": "8"
    },
    {
      "id": "sample_2",
      "input": "10\n20",
      "expected_output": "30"
    }
  ]
}
```

### All Test Cases (for `/runall` endpoint)

```json
{
  "test_cases": [
    {
      "id": "test_1",
      "input": "1\n1",
      "expected_output": "2"
    },
    {
      "id": "test_2",
      "input": "0\n0",
      "expected_output": "0"
    },
    {
      "id": "test_3",
      "input": "-5\n5",
      "expected_output": "0"
    },
    {
      "id": "test_4",
      "input": "100\n200",
      "expected_output": "300"
    },
    {
      "id": "test_5",
      "input": "-10\n-20",
      "expected_output": "-30"
    }
  ]
}
```

---

## 💻 Solution Code

### Python Solution
```python
def add(a, b):
    return a + b

a = int(input())
b = int(input())
result = add(a, b)
print(result)
```

### C++ Solution
```cpp
#include <iostream>
using namespace std;

int add(int a, int b) {
    return a + b;
}

int main() {
    int a, b;
    cin >> a >> b;
    int result = add(a, b);
    cout << result << endl;
    return 0;
}
```

### Java Solution
```java
import java.util.Scanner;

public class Solution {
    public static int add(int a, int b) {
        return a + b;
    }
    
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int a = scanner.nextInt();
        int b = scanner.nextInt();
        int result = add(a, b);
        System.out.println(result);
    }
}
```

---

## 🧪 Quick Test Commands

### Test with `/run` endpoint (Sample cases only)
```bash
curl -X POST "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/run" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "def add(a, b):\n    return a + b\n\na = int(input())\nb = int(input())\nresult = add(a, b)\nprint(result)",
    "sample_test_cases": [
      {"id": "sample_1", "input": "5\n3", "expected_output": "8"},
      {"id": "sample_2", "input": "10\n20", "expected_output": "30"}
    ],
    "question_id": "simple_sum",
    "user_id": "test_user"
  }'
```

### Test with `/runall` endpoint (All cases)
```bash
curl -X POST "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/runall" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

---

## 📊 Expected Performance

For Python:
- **Per test case:** ~50-150ms
- **5 test cases:** ~0.25-0.75s total
- **Very fast** - no compilation needed

For C++:
- **Per test case:** ~1,000-1,500ms (includes compilation)
- **5 test cases:** ~5-7.5s total
- **Slower** - but execution is fast once compiled

---

## 🎯 More Simple Questions

### Question 2: Find Maximum in Array

**Problem:** Find the maximum number in an array of integers.

**Input:**
```
5
1 5 3 9 2
```

**Output:**
```
9
```

**Python Solution:**
```python
n = int(input())
arr = list(map(int, input().split()))
print(max(arr))
```

### Question 3: Check Even or Odd

**Problem:** Check if a number is even or odd.

**Input:**
```
7
```

**Output:**
```
odd
```

**Python Solution:**
```python
n = int(input())
if n % 2 == 0:
    print("even")
else:
    print("odd")
```

### Question 4: Reverse a String

**Problem:** Reverse a given string.

**Input:**
```
hello
```

**Output:**
```
olleh
```

**Python Solution:**
```python
s = input()
print(s[::-1])
```

---

## 📝 Notes

- All test cases are simple and straightforward
- Input/output formats are consistent
- Good for testing API endpoints
- Fast execution times
- Easy to verify correctness


