#!/usr/bin/env python3
"""
Load Test: 100 Dummy Users with All 5 Languages
Each user submits a simple DSA question in different languages
Tests queue system and auto-scaling
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

# Simple DSA questions for each language
SIMPLE_QUESTIONS = {
    "python": {
        "code": """n = int(input())
sum_val = 0
for _ in range(n):
    sum_val += int(input())
print(sum_val)""",
        "test_cases": [{"id": "test_1", "input": "5\n1\n2\n3\n4\n5", "expected_output": "15\n"}]
    },
    "cpp": {
        "code": """#include <bits/stdc++.h>
using namespace std;
int main() {
    int n, sum = 0, x;
    cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> x;
        sum += x;
    }
    cout << sum << endl;
    return 0;
}""",
        "test_cases": [{"id": "test_1", "input": "5\n1\n2\n3\n4\n5", "expected_output": "15\n"}]
    },
    "java": {
        "code": """import java.util.*;
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int sum = 0;
        for (int i = 0; i < n; i++) {
            sum += sc.nextInt();
        }
        System.out.println(sum);
    }
}""",
        "test_cases": [{"id": "test_1", "input": "5\n1\n2\n3\n4\n5", "expected_output": "15\n"}]
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
});
rl.on('close', () => {
    const n = parseInt(lines[0]);
    let sum = 0;
    for (let i = 1; i <= n; i++) {
        sum += parseInt(lines[i]);
    }
    console.log(sum);
    process.exit(0);
});""",
        "test_cases": [{"id": "test_1", "input": "5\n1\n2\n3\n4\n5", "expected_output": "15\n"}]
    },
    "csharp": {
        "code": """using System;
class Program {
    static void Main() {
        int n = int.Parse(Console.ReadLine());
        int sum = 0;
        for (int i = 0; i < n; i++) {
            sum += int.Parse(Console.ReadLine());
        }
        Console.WriteLine(sum);
    }
}""",
        "test_cases": [{"id": "test_1", "input": "5\n1\n2\n3\n4\n5", "expected_output": "15\n"}]
    }
}

LANGUAGES = ["python", "cpp", "java", "javascript", "csharp"]

def submit_request(user_id, language, question_data):
    """Submit a request for a single user"""
    start_time = time.time()
    start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    
    payload = {
        "language": language,
        "code": question_data["code"],
        "test_cases": question_data["test_cases"],
        "user_id": f"user_{user_id}",
        "question_id": f"sum_array_{language}",
        "timeout": 10  # Increased timeout for queue handling
    }
    
    # Write payload to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(payload, f)
        temp_file = f.name
    
    try:
        # Execute curl command with longer timeout for queue
        curl_cmd = [
            'curl', '-s', '-w', '\nHTTP_CODE:%{http_code}\nTIME_TOTAL:%{time_total}',
            '-X', 'POST',
            '-H', 'Content-Type: application/json',
            '-d', f'@{temp_file}',
            '--max-time', '120',  # 2 minute timeout for queue
            API_URL + '/runall'
        ]
        
        result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=125)
        
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
            "language": language,
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
            "language": language,
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
            "language": language,
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
        try:
            os.unlink(temp_file)
        except:
            pass

def main():
    num_users = 100
    
    print("=" * 100)
    print("🚀 LOAD TEST: 100 Dummy Users with All 5 Languages")
    print("=" * 100)
    print(f"API URL: {API_URL}")
    print(f"Total Users: {num_users}")
    print(f"Languages: {', '.join(LANGUAGES)}")
    print(f"Questions: Simple sum of array (repeated)")
    print(f"Test Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 100)
    print()
    
    overall_start = time.time()
    overall_start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    
    print("⚡ Starting parallel execution of 100 users...")
    print("   Distributing across all 5 languages...")
    print("   Queue will handle requests if replicas are busy...")
    print()
    
    results = []
    completed = 0
    
    # Distribute users across languages
    user_assignments = []
    for i in range(num_users):
        language = LANGUAGES[i % len(LANGUAGES)]
        user_assignments.append((i+1, language, SIMPLE_QUESTIONS[language]))
    
    # Submit requests with retry logic and slight staggering to avoid overwhelming the queue
    def submit_with_retry(user_id, language, question_data, max_retries=3):
        """Submit request with retry logic"""
        for attempt in range(max_retries):
            result = submit_request(user_id, language, question_data)
            if result['success'] or result['http_code'] not in ['503', '502', '504']:
                return result
            # Exponential backoff: 1s, 2s, 4s
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
        return result
    
    # Stagger requests slightly (50ms between each) to avoid overwhelming the queue
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {}
        for idx, (user_id, language, question_data) in enumerate(user_assignments):
            # Stagger by 50ms per request
            time.sleep(0.05)
            future = executor.submit(submit_with_retry, user_id, language, question_data)
            futures[future] = user_id
        
        for future in as_completed(futures):
            completed += 1
            result = future.result()
            results.append(result)
            
            status_icon = "✅" if result['success'] else "❌"
            if completed % 10 == 0 or not result['success']:
                print(f"   [{completed:3d}/100] {status_icon} {result['user_id']:10s} - {result['language']:10s} - {result['http_code']:3s} - {result['wait_time_ms']:6d}ms")
    
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
        
        # Language distribution
        languages = {}
        for r in successful:
            lang = r['language']
            languages[lang] = languages.get(lang, 0) + 1
        
        print("📝 Language Distribution (Successful):")
        for lang in LANGUAGES:
            count = languages.get(lang, 0)
            total_for_lang = sum(1 for r in results if r['language'] == lang)
            success_rate_lang = (count / total_for_lang * 100) if total_for_lang > 0 else 0
            print(f"   {lang:12s}: {count:3d}/{total_for_lang:3d} ({success_rate_lang:.1f}%)")
        print()
        
        # Container distribution
        containers = {}
        for r in successful:
            container = r['container_id']
            containers[container] = containers.get(container, 0) + 1
        
        print("🔄 Container Distribution (Top 10):")
        for container, count in sorted(containers.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"   {container}: {count} requests")
        print()
        
        # Replica distribution
        replicas = {}
        for r in successful:
            replica = r['replica']
            replicas[replica] = replicas.get(replica, 0) + 1
        
        print("🔄 Replica Distribution (Top 10):")
        for replica, count in sorted(replicas.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"   {replica}: {count} requests")
        print()
        
        # Test results
        all_passed = sum(1 for r in successful if r['all_passed'])
        print(f"✅ All Tests Passed: {all_passed}/{len(successful)}")
        print()
    
    # Show failures by language
    if failed:
        print("❌ Failed Requests by Language:")
        failed_by_lang = {}
        for r in failed:
            lang = r['language']
            failed_by_lang[lang] = failed_by_lang.get(lang, 0) + 1
        for lang in LANGUAGES:
            count = failed_by_lang.get(lang, 0)
            if count > 0:
                print(f"   {lang:12s}: {count} failures")
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
        print(f"   Throughput: {len(successful) / overall_time:.2f} requests/second")
    print()

if __name__ == "__main__":
    main()

