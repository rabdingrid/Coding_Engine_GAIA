#!/usr/bin/env python3
"""
Load Test: 20 Dummy Users with Different Simple DSA Questions
Each user submits a different question, all executed in parallel
Shows timestamps and detailed execution summary
"""

import subprocess
import json
import time
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import tempfile
import os

API_URL = "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io"

# 20 Simple DSA Questions with Solutions
QUESTIONS = [
    {
        "id": 1,
        "name": "Sum of Array",
        "language": "cpp",
        "code": """#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    int sum = 0;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        sum += x;
    }
    cout << sum << endl;
    return 0;
}""",
        "test_cases": [{"id": "test_1", "input": "5\n1 2 3 4 5", "expected_output": "15\n"}]
    },
    {
        "id": 2,
        "name": "Find Maximum",
        "language": "cpp",
        "code": """#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    int max_val = INT_MIN;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        max_val = max(max_val, x);
    }
    cout << max_val << endl;
    return 0;
}""",
        "test_cases": [{"id": "test_1", "input": "5\n3 7 2 9 1", "expected_output": "9\n"}]
    },
    {
        "id": 3,
        "name": "Count Even Numbers",
        "language": "python",
        "code": """n = int(input())
count = 0
for _ in range(n):
    x = int(input())
    if x % 2 == 0:
        count += 1
print(count)""",
        "test_cases": [{"id": "test_1", "input": "5\n2 3 4 5 6", "expected_output": "3\n"}]
    },
    {
        "id": 4,
        "name": "Reverse Array",
        "language": "cpp",
        "code": """#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }
    for (int i = n-1; i >= 0; i--) {
        cout << arr[i] << " ";
    }
    cout << endl;
    return 0;
}""",
        "test_cases": [{"id": "test_1", "input": "5\n1 2 3 4 5", "expected_output": "5 4 3 2 1 \n"}]
    },
    {
        "id": 5,
        "name": "Factorial",
        "language": "python",
        "code": """def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)

n = int(input())
print(factorial(n))""",
        "test_cases": [{"id": "test_1", "input": "5", "expected_output": "120\n"}]
    },
    {
        "id": 6,
        "name": "Check Prime",
        "language": "cpp",
        "code": """#include <bits/stdc++.h>
using namespace std;
bool isPrime(int n) {
    if (n < 2) return false;
    for (int i = 2; i * i <= n; i++) {
        if (n % i == 0) return false;
    }
    return true;
}
int main() {
    int n;
    cin >> n;
    cout << (isPrime(n) ? "Yes" : "No") << endl;
    return 0;
}""",
        "test_cases": [{"id": "test_1", "input": "7", "expected_output": "Yes\n"}]
    },
    {
        "id": 7,
        "name": "Fibonacci",
        "language": "python",
        "code": """def fibonacci(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n+1):
        a, b = b, a + b
    return b

n = int(input())
print(fibonacci(n))""",
        "test_cases": [{"id": "test_1", "input": "7", "expected_output": "13\n"}]
    },
    {
        "id": 8,
        "name": "Find Minimum",
        "language": "cpp",
        "code": """#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    int min_val = INT_MAX;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        min_val = min(min_val, x);
    }
    cout << min_val << endl;
    return 0;
}""",
        "test_cases": [{"id": "test_1", "input": "5\n3 7 2 9 1", "expected_output": "1\n"}]
    },
    {
        "id": 9,
        "name": "Count Odd Numbers",
        "language": "python",
        "code": """n = int(input())
count = 0
for _ in range(n):
    x = int(input())
    if x % 2 == 1:
        count += 1
print(count)""",
        "test_cases": [{"id": "test_1", "input": "5\n2 3 4 5 6", "expected_output": "2\n"}]
    },
    {
        "id": 10,
        "name": "Sum of Digits",
        "language": "cpp",
        "code": """#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    int sum = 0;
    while (n > 0) {
        sum += n % 10;
        n /= 10;
    }
    cout << sum << endl;
    return 0;
}""",
        "test_cases": [{"id": "test_1", "input": "12345", "expected_output": "15\n"}]
    },
    {
        "id": 11,
        "name": "Check Palindrome",
        "language": "python",
        "code": """s = input().strip()
if s == s[::-1]:
    print("Yes")
else:
    print("No")""",
        "test_cases": [{"id": "test_1", "input": "racecar", "expected_output": "Yes\n"}]
    },
    {
        "id": 12,
        "name": "Power of Two",
        "language": "cpp",
        "code": """#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    if (n > 0 && (n & (n-1)) == 0) {
        cout << "Yes" << endl;
    } else {
        cout << "No" << endl;
    }
    return 0;
}""",
        "test_cases": [{"id": "test_1", "input": "8", "expected_output": "Yes\n"}]
    },
    {
        "id": 13,
        "name": "GCD",
        "language": "python",
        "code": """def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

a, b = map(int, input().split())
print(gcd(a, b))""",
        "test_cases": [{"id": "test_1", "input": "48 18", "expected_output": "6\n"}]
    },
    {
        "id": 14,
        "name": "Count Vowels",
        "language": "cpp",
        "code": """#include <bits/stdc++.h>
using namespace std;
int main() {
    string s;
    getline(cin, s);
    int count = 0;
    for (char c : s) {
        if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u' ||
            c == 'A' || c == 'E' || c == 'I' || c == 'O' || c == 'U') {
            count++;
        }
    }
    cout << count << endl;
    return 0;
}""",
        "test_cases": [{"id": "test_1", "input": "hello world", "expected_output": "3\n"}]
    },
    {
        "id": 15,
        "name": "Square Root",
        "language": "python",
        "code": """import math
n = int(input())
print(int(math.sqrt(n)))""",
        "test_cases": [{"id": "test_1", "input": "25", "expected_output": "5\n"}]
    },
    {
        "id": 16,
        "name": "Count Primes",
        "language": "cpp",
        "code": """#include <bits/stdc++.h>
using namespace std;
bool isPrime(int n) {
    if (n < 2) return false;
    for (int i = 2; i * i <= n; i++) {
        if (n % i == 0) return false;
    }
    return true;
}
int main() {
    int n;
    cin >> n;
    int count = 0;
    for (int i = 2; i <= n; i++) {
        if (isPrime(i)) count++;
    }
    cout << count << endl;
    return 0;
}""",
        "test_cases": [{"id": "test_1", "input": "10", "expected_output": "4\n"}]
    },
    {
        "id": 17,
        "name": "String Length",
        "language": "python",
        "code": """s = input().strip()
print(len(s))""",
        "test_cases": [{"id": "test_1", "input": "hello", "expected_output": "5\n"}]
    },
    {
        "id": 18,
        "name": "Binary to Decimal",
        "language": "cpp",
        "code": """#include <bits/stdc++.h>
using namespace std;
int main() {
    string binary;
    cin >> binary;
    int decimal = 0;
    int power = 1;
    for (int i = binary.length() - 1; i >= 0; i--) {
        if (binary[i] == '1') {
            decimal += power;
        }
        power *= 2;
    }
    cout << decimal << endl;
    return 0;
}""",
        "test_cases": [{"id": "test_1", "input": "1010", "expected_output": "10\n"}]
    },
    {
        "id": 19,
        "name": "Sum of Squares",
        "language": "python",
        "code": """n = int(input())
sum_sq = 0
for i in range(1, n+1):
    sum_sq += i * i
print(sum_sq)""",
        "test_cases": [{"id": "test_1", "input": "5", "expected_output": "55\n"}]
    },
    {
        "id": 20,
        "name": "Check Even",
        "language": "cpp",
        "code": """#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    if (n % 2 == 0) {
        cout << "Yes" << endl;
    } else {
        cout << "No" << endl;
    }
    return 0;
}""",
        "test_cases": [{"id": "test_1", "input": "8", "expected_output": "Yes\n"}]
    }
]

def submit_request(user_id, question):
    """Submit a request for a single user with a specific question"""
    start_time = time.time()
    start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    
    payload = {
        "language": question["language"],
        "code": question["code"],
        "test_cases": question["test_cases"],
        "user_id": f"user_{user_id}",
        "question_id": f"dsa_q{question['id']}",
        "timeout": 5
    }
    
    # Write payload to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(payload, f)
        temp_file = f.name
    
    try:
        # Execute curl command
        curl_cmd = [
            'curl', '-s', '-w', '\nHTTP_CODE:%{http_code}\nTIME_TOTAL:%{time_total}',
            '-X', 'POST',
            '-H', 'Content-Type: application/json',
            '-d', f'@{temp_file}',
            '--max-time', '60',
            API_URL + '/runall'
        ]
        
        result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=65)
        
        end_time = time.time()
        end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        wait_time_ms = int((end_time - start_time) * 1000)
        
        # Parse response
        output = result.stdout
        http_code = None
        time_total = None
        body = output
        
        for line in output.split('\n'):
            if line.startswith('HTTP_CODE:'):
                http_code = line.split(':', 1)[1].strip()
            elif line.startswith('TIME_TOTAL:'):
                time_total = float(line.split(':', 1)[1].strip())
        
        # Remove curl metadata lines from body
        body_lines = [l for l in output.split('\n') if not l.startswith('HTTP_CODE:') and not l.startswith('TIME_TOTAL:')]
        body = '\n'.join(body_lines)
        
        # Parse JSON response
        container_id = "unknown"
        replica = "unknown"
        exec_time = 0
        all_passed = False
        
        if http_code == "200" and body:
            try:
                response_data = json.loads(body)
                metadata = response_data.get('metadata', {})
                container_id = metadata.get('container_id', 'unknown')
                replica = metadata.get('replica', 'unknown')
                exec_time = metadata.get('execution_time_ms', 0)
                summary = response_data.get('summary', {})
                all_passed = summary.get('all_passed', False)
            except:
                pass
        
        return {
            "user_id": f"user_{user_id}",
            "question_id": question['id'],
            "question_name": question['name'],
            "language": question["language"],
            "http_code": http_code or "error",
            "wait_time_ms": wait_time_ms,
            "exec_time_ms": exec_time,
            "container_id": container_id,
            "replica": replica,
            "all_passed": all_passed,
            "time_total": time_total or 0,
            "success": http_code == "200",
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp,
            "duration_ms": wait_time_ms
        }
    except subprocess.TimeoutExpired:
        end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        return {
            "user_id": f"user_{user_id}",
            "question_id": question['id'],
            "question_name": question['name'],
            "language": question["language"],
            "http_code": "timeout",
            "wait_time_ms": int((time.time() - start_time) * 1000),
            "exec_time_ms": 0,
            "container_id": "unknown",
            "replica": "unknown",
            "all_passed": False,
            "time_total": 0,
            "success": False,
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp,
            "duration_ms": int((time.time() - start_time) * 1000)
        }
    except Exception as e:
        end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        return {
            "user_id": f"user_{user_id}",
            "question_id": question['id'],
            "question_name": question['name'],
            "language": question["language"],
            "http_code": "error",
            "wait_time_ms": int((time.time() - start_time) * 1000),
            "exec_time_ms": 0,
            "container_id": "unknown",
            "replica": "unknown",
            "all_passed": False,
            "time_total": 0,
            "success": False,
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp,
            "duration_ms": int((time.time() - start_time) * 1000),
            "error": str(e)
        }
    finally:
        # Cleanup temp file
        try:
            os.unlink(temp_file)
        except:
            pass

def main():
    print("=" * 100)
    print("🚀 LOAD TEST: 20 Dummy Users with Different DSA Questions")
    print("=" * 100)
    print(f"API URL: {API_URL}")
    print(f"Total Users: 20")
    print(f"Questions: 20 different simple DSA problems")
    print(f"Test Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 100)
    print()
    
    overall_start = time.time()
    overall_start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    
    print("⚡ Starting parallel execution of 20 users...")
    print("   Each user submitting a different DSA question...")
    print()
    
    results = []
    completed = 0
    
    # Submit all requests in parallel
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {
            executor.submit(submit_request, i+1, QUESTIONS[i]): i+1 
            for i in range(20)
        }
        
        for future in as_completed(futures):
            completed += 1
            result = future.result()
            results.append(result)
            
            status_icon = "✅" if result['success'] else "❌"
            print(f"   [{completed:2d}/20] {status_icon} {result['user_id']:10s} - {result['question_name']:20s} ({result['language']:6s}) - {result['http_code']:3s} - {result['wait_time_ms']:5d}ms")
    
    overall_time = time.time() - overall_start
    overall_end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    overall_time_ms = int(overall_time * 1000)
    
    print()
    print("✅ All requests completed!")
    print()
    
    # Analyze results
    print("=" * 100)
    print("📊 RESULTS SUMMARY")
    print("=" * 100)
    print()
    
    total = len(results)
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"📈 Overall Statistics:")
    print(f"   Test Start: {overall_start_timestamp}")
    print(f"   Test End:   {overall_end_timestamp}")
    print(f"   Total Duration: {overall_time_ms}ms ({overall_time:.2f}s)")
    print(f"   Total Requests: {total}")
    print(f"   ✅ Successful: {len(successful)}")
    print(f"   ❌ Failed: {len(failed)}")
    if total > 0:
        success_rate = (len(successful) / total) * 100
        print(f"   Success Rate: {success_rate:.1f}%")
    print()
    
    if successful:
        wait_times = [r['wait_time_ms'] for r in successful]
        exec_times = [r['exec_time_ms'] for r in successful]
        
        print(f"⏱️  Performance Metrics (Successful Requests):")
        print(f"   Wait Time - Min: {min(wait_times)}ms, Max: {max(wait_times)}ms, Avg: {int(sum(wait_times) / len(wait_times))}ms")
        print(f"   Execution Time - Min: {min(exec_times)}ms, Max: {max(exec_times)}ms, Avg: {int(sum(exec_times) / len(exec_times))}ms")
        print()
        
        # Container distribution
        containers = {}
        for r in successful:
            container = r['container_id']
            containers[container] = containers.get(container, 0) + 1
        
        print("🔄 Container Distribution:")
        for container, count in sorted(containers.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"   {container}: {count} requests")
        print()
        
        # Replica distribution
        replicas = {}
        for r in successful:
            replica = r['replica']
            replicas[replica] = replicas.get(replica, 0) + 1
        
        print("🔄 Replica Distribution:")
        for replica, count in sorted(replicas.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"   {replica}: {count} requests")
        print()
        
        # Test results
        all_passed = sum(1 for r in successful if r['all_passed'])
        print(f"✅ All Tests Passed: {all_passed}/{len(successful)}")
        print()
        
        # Language distribution
        languages = {}
        for r in successful:
            lang = r['language']
            languages[lang] = languages.get(lang, 0) + 1
        
        print("📝 Language Distribution:")
        for lang, count in sorted(languages.items()):
            print(f"   {lang}: {count} requests")
        print()
    
    # Detailed results with timestamps
    print("=" * 100)
    print("📋 DETAILED RESULTS WITH TIMESTAMPS")
    print("=" * 100)
    print(f"{'User':<10} {'Q#':<4} {'Question':<20} {'Lang':<6} {'Status':<8} {'Start Time':<23} {'End Time':<23} {'Duration':<10} {'Exec':<8} {'Pass':<6}")
    print("-" * 100)
    
    # Sort by start timestamp
    results_sorted = sorted(results, key=lambda x: x['start_timestamp'])
    
    for r in results_sorted:
        status = "✅" if r['success'] else f"❌{r['http_code']}"
        pass_icon = "✅" if r.get('all_passed') else "❌"
        start_time_short = r['start_timestamp'].split('.')[0] + '.' + r['start_timestamp'].split('.')[1][:2] if '.' in r['start_timestamp'] else r['start_timestamp']
        end_time_short = r['end_timestamp'].split('.')[0] + '.' + r['end_timestamp'].split('.')[1][:2] if '.' in r['end_timestamp'] else r['end_timestamp']
        
        print(f"{r['user_id']:<10} {r['question_id']:<4} {r['question_name']:<20} {r['language']:<6} {status:<8} {start_time_short:<23} {end_time_short:<23} {r['duration_ms']:<10} {r['exec_time_ms']:<8} {pass_icon:<6}")
    
    print()
    print("=" * 100)
    print("✅ Load test complete!")
    print("=" * 100)
    print()
    print(f"📊 Final Summary:")
    print(f"   Test Duration: {overall_time_ms}ms ({overall_time:.2f}s)")
    print(f"   Requests Handled: {len(successful)}/{total}")
    if successful:
        print(f"   Average Wait Time: {int(sum([r['wait_time_ms'] for r in successful]) / len(successful))}ms")
        print(f"   Average Execution Time: {int(sum([r['exec_time_ms'] for r in successful]) / len(successful))}ms")
    print()

if __name__ == "__main__":
    main()

