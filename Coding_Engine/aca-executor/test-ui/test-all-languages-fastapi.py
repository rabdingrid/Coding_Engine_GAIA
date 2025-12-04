#!/usr/bin/env python3
"""
Comprehensive FastAPI Testing - All Languages
Tests /run, /runall, and /submit with different DSA questions for each language
"""

import json
import urllib.request
import urllib.parse
import sys
import random
import time

BASE_URL = "http://localhost:8000"

def make_request(endpoint, data):
    """Make HTTP POST request"""
    url = f"{BASE_URL}{endpoint}"
    data_json = json.dumps(data).encode('utf-8')
    
    req = urllib.request.Request(
        url,
        data=data_json,
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"❌ HTTP Error {e.code}: {error_body[:200]}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def generate_test_cases(count=20, problem_type="sum"):
    """Generate test cases based on problem type"""
    test_cases = []
    
    if problem_type == "sum":
        for i in range(1, count + 1):
            a = random.randint(1, 10000)
            b = random.randint(1, 10000)
            test_cases.append({
                "id": f"test_{i}",
                "input": f"{a}\n{b}",
                "expected_output": str(a + b)
            })
    
    elif problem_type == "max_array":
        for i in range(1, count + 1):
            n = random.randint(5, 20)
            arr = [random.randint(1, 1000) for _ in range(n)]
            max_val = max(arr)
            test_cases.append({
                "id": f"test_{i}",
                "input": f"{n}\n{' '.join(map(str, arr))}",
                "expected_output": str(max_val)
            })
    
    elif problem_type == "reverse_string":
        for i in range(1, count + 1):
            s = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(5, 15)))
            reversed_s = s[::-1]
            test_cases.append({
                "id": f"test_{i}",
                "input": s,
                "expected_output": reversed_s
            })
    
    elif problem_type == "factorial":
        for i in range(1, count + 1):
            n = random.randint(1, 10)  # Keep small to avoid overflow
            fact = 1
            for j in range(1, n + 1):
                fact *= j
            test_cases.append({
                "id": f"test_{i}",
                "input": str(n),
                "expected_output": str(fact)
            })
    
    return test_cases

# Problem definitions for each language
PROBLEMS = {
    "python": {
        "sum": {
            "code": """a = int(input())
b = int(input())
print(a + b)""",
            "name": "Sum of Two Numbers"
        },
        "max_array": {
            "code": """n = int(input())
arr = list(map(int, input().split()))
print(max(arr))""",
            "name": "Find Maximum in Array"
        },
        "reverse_string": {
            "code": """s = input()
print(s[::-1])""",
            "name": "Reverse String"
        },
        "factorial": {
            "code": """def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

n = int(input())
print(factorial(n))""",
            "name": "Factorial"
        }
    },
    "java": {
        "sum": {
            "code": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int a = sc.nextInt();
        int b = sc.nextInt();
        System.out.println(a + b);
    }
}""",
            "name": "Sum of Two Numbers"
        },
        "max_array": {
            "code": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int max = Integer.MIN_VALUE;
        for (int i = 0; i < n; i++) {
            int num = sc.nextInt();
            if (num > max) {
                max = num;
            }
        }
        System.out.println(max);
    }
}""",
            "name": "Find Maximum in Array"
        },
        "reverse_string": {
            "code": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine();
        StringBuilder sb = new StringBuilder(s);
        System.out.println(sb.reverse().toString());
    }
}""",
            "name": "Reverse String"
        },
        "factorial": {
            "code": """import java.util.Scanner;

public class Main {
    public static int factorial(int n) {
        if (n <= 1) {
            return 1;
        }
        return n * factorial(n - 1);
    }
    
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        System.out.println(factorial(n));
    }
}""",
            "name": "Factorial"
        }
    },
    "cpp": {
        "sum": {
            "code": """#include <iostream>
using namespace std;

int main() {
    int a, b;
    cin >> a >> b;
    cout << a + b << endl;
    return 0;
}""",
            "name": "Sum of Two Numbers"
        },
        "max_array": {
            "code": """#include <iostream>
#include <climits>
using namespace std;

int main() {
    int n;
    cin >> n;
    int max_val = INT_MIN;
    for (int i = 0; i < n; i++) {
        int num;
        cin >> num;
        if (num > max_val) {
            max_val = num;
        }
    }
    cout << max_val << endl;
    return 0;
}""",
            "name": "Find Maximum in Array"
        },
        "reverse_string": {
            "code": """#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    string s;
    getline(cin, s);
    reverse(s.begin(), s.end());
    cout << s << endl;
    return 0;
}""",
            "name": "Reverse String"
        },
        "factorial": {
            "code": """#include <iostream>
using namespace std;

int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int main() {
    int n;
    cin >> n;
    cout << factorial(n) << endl;
    return 0;
}""",
            "name": "Factorial"
        }
    },
    "javascript": {
        "sum": {
            "code": """const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

let input = [];
rl.on('line', (line) => {
    input.push(parseInt(line));
    if (input.length === 2) {
        console.log(input[0] + input[1]);
        rl.close();
    }
});""",
            "name": "Sum of Two Numbers"
        },
        "max_array": {
            "code": """const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

let lines = [];
rl.on('line', (line) => {
    lines.push(line);
    if (lines.length === 2) {
        const n = parseInt(lines[0]);
        const arr = lines[1].split(' ').map(Number);
        const max = Math.max(...arr);
        console.log(max);
        rl.close();
    }
});""",
            "name": "Find Maximum in Array"
        },
        "reverse_string": {
            "code": """const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.on('line', (line) => {
    console.log(line.split('').reverse().join(''));
    rl.close();
});""",
            "name": "Reverse String"
        },
        "factorial": {
            "code": """const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

function factorial(n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

rl.on('line', (line) => {
    const n = parseInt(line);
    console.log(factorial(n));
    rl.close();
});""",
            "name": "Factorial"
        }
    },
    "csharp": {
        "sum": {
            "code": """using System;

public class Solution {
    public static void Main() {
        int a = int.Parse(Console.ReadLine());
        int b = int.Parse(Console.ReadLine());
        Console.WriteLine(a + b);
    }
}""",
            "name": "Sum of Two Numbers"
        },
        "max_array": {
            "code": """using System;
using System.Linq;

public class Solution {
    public static void Main() {
        int n = int.Parse(Console.ReadLine());
        int[] arr = Console.ReadLine().Split(' ').Select(int.Parse).ToArray();
        int max = arr[0];
        for (int i = 1; i < n; i++) {
            if (arr[i] > max) {
                max = arr[i];
            }
        }
        Console.WriteLine(max);
    }
}""",
            "name": "Find Maximum in Array"
        },
        "reverse_string": {
            "code": """using System;

public class Solution {
    public static void Main() {
        string s = Console.ReadLine();
        char[] arr = s.ToCharArray();
        Array.Reverse(arr);
        Console.WriteLine(new string(arr));
    }
}""",
            "name": "Reverse String"
        },
        "factorial": {
            "code": """using System;

public class Solution {
    public static int Factorial(int n) {
        if (n <= 1) {
            return 1;
        }
        return n * Factorial(n - 1);
    }
    
    public static void Main() {
        int n = int.Parse(Console.ReadLine());
        Console.WriteLine(Factorial(n));
    }
}""",
            "name": "Factorial"
        }
    }
}

def test_endpoint(language, problem_type, endpoint, test_cases, code, problem_name):
    """Test a specific endpoint"""
    print(f"\n   Testing {endpoint.upper()} endpoint...")
    
    if endpoint == "/run":
        request_data = {
            "language": language,
            "code": code,
            "sample_test_cases": test_cases[:10],  # First 10 as sample
            "user_id": f"test_user_{language}",
            "question_id": f"test_q_{problem_type}",
            "timeout": 5
        }
    elif endpoint == "/runall":
        request_data = {
            "language": language,
            "code": code,
            "test_cases": test_cases[10:],  # Rest as all test cases
            "sample_test_cases": [],
            "user_id": f"test_user_{language}",
            "question_id": f"test_q_{problem_type}",
            "timeout": 5
        }
    else:  # /submit
        request_data = {
            "language": language,
            "code": code,
            "test_cases": test_cases,
            "sample_test_cases": [],
            "user_id": f"test_user_{language}_submit",
            "question_id": f"test_q_{problem_type}_submit",
            "timeout": 5
        }
    
    start_time = time.time()
    response = make_request(endpoint, request_data)
    elapsed = time.time() - start_time
    
    if response:
        summary = response.get('summary', {})
        total = summary.get('total_tests', 0)
        passed = summary.get('passed', 0)
        failed = summary.get('failed', 0)
        all_passed = summary.get('all_passed', False)
        
        status_icon = "✅" if all_passed else "⚠️"
        print(f"   {status_icon} {passed}/{total} passed, {failed} failed (took {elapsed:.2f}s)")
        
        # Check for error types
        test_results = response.get('test_results', [])
        error_types = {}
        for tr in test_results:
            status = tr.get('status', 'unknown')
            if status not in ['passed']:
                error_types[status] = error_types.get(status, 0) + 1
        
        if error_types:
            print(f"   ⚠️  Errors: {', '.join(f'{k}({v})' for k, v in error_types.items())}")
        
        return all_passed
    else:
        print(f"   ❌ Request failed")
        return False

def test_language(language):
    """Test all problems for a language"""
    print(f"\n{'='*70}")
    print(f"🔤 Testing {language.upper()}")
    print(f"{'='*70}")
    
    if language not in PROBLEMS:
        print(f"❌ Language {language} not supported")
        return False
    
    results = []
    
    # Test each problem type
    for problem_type, problem_data in PROBLEMS[language].items():
        print(f"\n📝 Problem: {problem_data['name']} ({problem_type})")
        print("-" * 70)
        
        code = problem_data['code']
        test_cases = generate_test_cases(20, problem_type)
        
        # Test /run endpoint
        run_passed = test_endpoint(language, problem_type, "/run", test_cases, code, problem_data['name'])
        results.append(("/run", problem_type, run_passed))
        
        time.sleep(0.5)  # Small delay between requests
        
        # Test /runall endpoint
        runall_passed = test_endpoint(language, problem_type, "/runall", test_cases, code, problem_data['name'])
        results.append(("/runall", problem_type, runall_passed))
        
        time.sleep(0.5)
        
        # Test /submit endpoint
        submit_passed = test_endpoint(language, problem_type, "/submit", test_cases, code, problem_data['name'])
        results.append(("/submit", problem_type, submit_passed))
        
        time.sleep(1)  # Longer delay between problems
    
    # Summary for language
    print(f"\n📊 {language.upper()} Summary:")
    print("-" * 70)
    all_passed = True
    for endpoint, problem, passed in results:
        status = "✅" if passed else "❌"
        print(f"   {status} {endpoint} - {problem}")
        if not passed:
            all_passed = False
    
    return all_passed

def test_health():
    """Test health endpoint"""
    try:
        url = f"{BASE_URL}/health"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            print("✅ Health check passed!")
            print(f"   Status: {data.get('status', 'unknown')}")
            print(f"   Version: {data.get('version', 'unknown')}")
            return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Comprehensive FastAPI Testing - All Languages")
    print("=" * 70)
    print(f"Base URL: {BASE_URL}")
    print("Testing: Python, Java, C++, JavaScript, C#")
    print("Problems: Sum, Max Array, Reverse String, Factorial")
    print("Endpoints: /run, /runall, /submit")
    print("=" * 70)
    
    # Check if service is running
    if not test_health():
        print("\n❌ Service is not running!")
        print("   Start the service with:")
        print("   cd Coding_Engine/aca-executor")
        print("   uvicorn executor-service-fastapi:app --reload --port 8000")
        sys.exit(1)
    
    # Test all languages
    languages = ["python", "java", "cpp", "javascript", "csharp"]
    language_results = []
    
    for language in languages:
        passed = test_language(language)
        language_results.append((language, passed))
        print("\n")
    
    # Final summary
    print("=" * 70)
    print("📊 FINAL SUMMARY")
    print("=" * 70)
    
    for language, passed in language_results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {language.upper()}")
    
    all_passed = all(result[1] for result in language_results)
    
    if all_passed:
        print("\n🎉 All languages passed all tests!")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Check output above for details.")
        sys.exit(1)

