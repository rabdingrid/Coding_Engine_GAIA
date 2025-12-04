#!/usr/bin/env python3
"""
Quick Test: 5 Users with Simple Test Cases
Should complete within 5 seconds
"""

import subprocess
import json
import time
from datetime import datetime
import tempfile
import os

API_URL = "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io"

# Simple test case - just 1 test case per user (not 20)
SIMPLE_TEST = {
    "python": {
        "code": "print(int(input()) + int(input()))",
        "test_cases": [
            {"id": "tc_1", "input": "5\n10", "expected_output": "15\n"}
        ]
    },
    "cpp": {
        "code": """#include <iostream>
using namespace std;
int main() {
    int a, b;
    cin >> a >> b;
    cout << a + b << endl;
    return 0;
}""",
        "test_cases": [
            {"id": "tc_1", "input": "5\n10", "expected_output": "15\n"}
        ]
    },
    "java": {
        "code": """import java.util.*;
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int a = sc.nextInt();
        int b = sc.nextInt();
        System.out.println(a + b);
    }
}""",
        "test_cases": [
            {"id": "tc_1", "input": "5\n10", "expected_output": "15\n"}
        ]
    },
    "javascript": {
        "code": """const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});
let lines = [];
rl.on('line', (line) => {
    lines.push(line);
    if (lines.length === 2) {
        const a = parseInt(lines[0]);
        const b = parseInt(lines[1]);
        console.log(a + b);
        rl.close();
    }
});""",
        "test_cases": [
            {"id": "tc_1", "input": "5\n10", "expected_output": "15\n"}
        ]
    },
    "csharp": {
        "code": """using System;
class Program {
    static void Main() {
        int a = int.Parse(Console.ReadLine());
        int b = int.Parse(Console.ReadLine());
        Console.WriteLine(a + b);
    }
}""",
        "test_cases": [
            {"id": "tc_1", "input": "5\n10", "expected_output": "15\n"}
        ]
    }
}

LANGUAGES = ["python", "cpp", "java", "javascript", "csharp"]

def submit_request(user_id, language, question_data):
    """Submit a request - should be fast"""
    start_time = time.time()
    
    payload = {
        "language": language,
        "code": question_data["code"],
        "test_cases": question_data["test_cases"],
        "user_id": f"user_{user_id}",
        "question_id": f"simple_add_{language}",
        "timeout": 5
    }
    
    # Write payload to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(payload, f)
        temp_file = f.name
    
    try:
        # Execute curl with short timeout
        curl_cmd = [
            'curl', '-s', '-w', '\nHTTP_CODE:%{http_code}\nTIME_TOTAL:%{time_total}',
            '-X', 'POST',
            '-H', 'Content-Type: application/json',
            '-d', f'@{temp_file}',
            '--max-time', '10',  # 10 second max
            API_URL + '/runall'
        ]
        
        result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=12)
        
        end_time = time.time()
        wait_time_ms = int((end_time - start_time) * 1000)
        
        # Parse response
        output = result.stdout
        http_code = None
        time_total = None
        
        for line in output.split('\n'):
            if line.startswith('HTTP_CODE:'):
                http_code = line.split(':', 1)[1].strip()
            elif line.startswith('TIME_TOTAL:'):
                time_total = float(line.split(':', 1)[1].strip())
        
        # Parse JSON response
        body_lines = [l for l in output.split('\n') if not l.startswith('HTTP_CODE:') and not l.startswith('TIME_TOTAL:')]
        body = '\n'.join(body_lines)
        
        success = http_code == "200"
        passed_count = 0
        total_count = 1
        
        if success and body:
            try:
                response_data = json.loads(body)
                summary = response_data.get('summary', {})
                passed_count = summary.get('passed', 0)
                total_count = summary.get('total', 1)
            except:
                pass
        
        return {
            "user_id": f"user_{user_id}",
            "language": language,
            "http_code": http_code or "error",
            "wait_time_ms": wait_time_ms,
            "success": success,
            "passed_count": passed_count,
            "total_count": total_count
        }
    except subprocess.TimeoutExpired:
        return {
            "user_id": f"user_{user_id}",
            "language": language,
            "http_code": "timeout",
            "wait_time_ms": int((time.time() - start_time) * 1000),
            "success": False,
            "passed_count": 0,
            "total_count": 1
        }
    except Exception as e:
        return {
            "user_id": f"user_{user_id}",
            "language": language,
            "http_code": "error",
            "wait_time_ms": int((time.time() - start_time) * 1000),
            "success": False,
            "passed_count": 0,
            "total_count": 1,
            "error": str(e)
        }
    finally:
        try:
            os.unlink(temp_file)
        except:
            pass

def main():
    num_users = 5
    
    print("=" * 80)
    print("🧪 QUICK TEST: 5 Users (1 test case each)")
    print("=" * 80)
    print(f"API URL: {API_URL}")
    print(f"Total Users: {num_users}")
    print(f"Test Cases: 1 per user (simple addition)")
    print(f"Expected: Complete within 5 seconds")
    print("=" * 80)
    print()
    
    overall_start = time.time()
    
    results = []
    user_assignments = []
    for i in range(num_users):
        language = LANGUAGES[i % len(LANGUAGES)]
        user_assignments.append((i+1, language, SIMPLE_TEST[language]))
    
    print("⚡ Sending 5 requests...")
    print()
    
    # Send all 5 at once
    import threading
    threads = []
    for user_id, language, question_data in user_assignments:
        thread = threading.Thread(
            target=lambda u, l, q: results.append(submit_request(u, l, q)),
            args=(user_id, language, question_data)
        )
        threads.append(thread)
        thread.start()
    
    # Wait for all to complete
    for thread in threads:
        thread.join()
    
    overall_time = time.time() - overall_start
    
    print("=" * 80)
    print("📊 RESULTS")
    print("=" * 80)
    print()
    
    for r in sorted(results, key=lambda x: int(x['user_id'].split('_')[1])):
        status = "✅" if r['success'] else "❌"
        print(f"{status} {r['user_id']:10s} - {r['language']:12s} - {r['http_code']:3s} - {r['wait_time_ms']:5d}ms - TC: {r['passed_count']}/{r['total_count']}")
    
    print()
    print("=" * 80)
    successful = [r for r in results if r['success']]
    print(f"✅ Successful: {len(successful)}/{num_users}")
    print(f"⏱️  Total Time: {overall_time:.2f}s")
    print(f"⏱️  Avg Time: {sum(r['wait_time_ms'] for r in successful) / len(successful) if successful else 0:.0f}ms per request")
    print("=" * 80)
    
    if overall_time > 5:
        print()
        print("⚠️  WARNING: Test took longer than 5 seconds!")
        print(f"   Expected: < 5s")
        print(f"   Actual: {overall_time:.2f}s")
    else:
        print()
        print("✅ SUCCESS: Test completed within 5 seconds!")

if __name__ == "__main__":
    main()

