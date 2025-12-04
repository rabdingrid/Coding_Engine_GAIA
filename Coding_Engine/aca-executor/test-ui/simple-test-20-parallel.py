#!/usr/bin/env python3
"""
Simple Test: 20 Users in PARALLEL with /runall endpoint
Test concurrent capacity (2 replicas = 16 concurrent, should scale to 3 = 24)
"""

import subprocess
import json
import time
from datetime import datetime
import tempfile
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

API_URL = "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io"

# Simple test case
SIMPLE_QUESTION = {
    "code": """n = int(input())
arr = list(map(int, input().split()))
print(sum(arr))""",
    "test_cases": [
        {"id": "tc_1", "input": "5\n1 2 3 4 5", "expected_output": "15\n"},
        {"id": "tc_2", "input": "3\n10 20 30", "expected_output": "60\n"},
        {"id": "tc_3", "input": "4\n1 1 1 1", "expected_output": "4\n"},
    ]
}

def test_user(user_id, language="python"):
    """Test a single user"""
    start_time = time.time()
    start_ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    
    payload = {
        "language": language,
        "code": SIMPLE_QUESTION["code"],
        "test_cases": SIMPLE_QUESTION["test_cases"]
    }
    
    # Write to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(payload, f)
        temp_file = f.name
    
    try:
        # Simple curl request
        curl_cmd = [
            'curl', '-s', '-w', '\nHTTP_CODE:%{http_code}',
            '-X', 'POST',
            '-H', 'Content-Type: application/json',
            '-d', f'@{temp_file}',
            '--max-time', '30',
            API_URL + '/runall'
        ]
        
        result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=35)
        
        end_time = time.time()
        end_ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        duration_ms = int((end_time - start_time) * 1000)
        
        # Parse HTTP code
        http_code = "unknown"
        for line in result.stdout.split('\n'):
            if line.startswith('HTTP_CODE:'):
                http_code = line.split(':', 1)[1].strip()
                break
        
        # Parse JSON response
        body = '\n'.join([l for l in result.stdout.split('\n') if not l.startswith('HTTP_CODE:')])
        success = False
        passed = 0
        total = 0
        
        if http_code == "200" and body:
            try:
                data = json.loads(body)
                summary = data.get('summary', {})
                passed = summary.get('passed', 0)
                total = summary.get('total', 0)
                success = True
            except:
                pass
        
        return {
            'user_id': user_id,
            'start_ts': start_ts,
            'end_ts': end_ts,
            'duration_ms': duration_ms,
            'http_code': http_code,
            'success': success,
            'passed': passed,
            'total': total
        }
    except Exception as e:
        end_ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        return {
            'user_id': user_id,
            'start_ts': start_ts,
            'end_ts': end_ts,
            'duration_ms': int((time.time() - start_time) * 1000),
            'http_code': 'error',
            'success': False,
            'passed': 0,
            'total': 0,
            'error': str(e)
        }
    finally:
        try:
            os.unlink(temp_file)
        except:
            pass

def main():
    num_users = 20
    
    print("=" * 80)
    print(f"🧪 PARALLEL TEST: {num_users} Users at ONCE with /runall")
    print("=" * 80)
    print(f"API: {API_URL}")
    print(f"Endpoint: /runall")
    print(f"Test Cases: 3 per user")
    print(f"Concurrency: {num_users} users at once")
    print(f"Expected: 2 replicas (16 concurrent) should scale to 3 (24 concurrent)")
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print()
    
    overall_start = time.time()
    
    # Test 20 users in PARALLEL (all at once)
    print(f"📤 Sending {num_users} requests in PARALLEL...")
    print()
    
    results = []
    with ThreadPoolExecutor(max_workers=num_users) as executor:
        futures = {executor.submit(test_user, i): i for i in range(1, num_users + 1)}
        
        completed = 0
        for future in as_completed(futures):
            completed += 1
            result = future.result()
            results.append(result)
            status = "✅" if result['success'] else "❌"
            print(f"{status} User {result['user_id']:2d}: {result['start_ts']} → {result['end_ts']} ({result['duration_ms']:5d}ms) - {result['http_code']} - TC: {result['passed']}/{result['total']} [{completed}/{num_users}]")
    
    overall_time = time.time() - overall_start
    
    # Sort by user_id for display
    results.sort(key=lambda x: x['user_id'])
    
    print()
    print("=" * 80)
    print("📊 RESULTS")
    print("=" * 80)
    print()
    
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"✅ Successful: {len(successful)}/{num_users}")
    print(f"❌ Failed: {len(failed)}/{num_users}")
    print()
    
    if successful:
        durations = [r['duration_ms'] for r in successful]
        print(f"⏱️  Duration Stats (successful):")
        print(f"   Min: {min(durations)}ms")
        print(f"   Max: {max(durations)}ms")
        print(f"   Avg: {int(sum(durations) / len(durations))}ms")
        print()
    
    if failed:
        print(f"❌ Failed Requests:")
        for r in failed:
            print(f"   User {r['user_id']}: {r['http_code']} - {r.get('error', 'N/A')}")
        print()
    
    print(f"⏱️  Total Time (all {num_users} parallel): {int(overall_time * 1000)}ms ({overall_time:.2f}s)")
    print(f"   (Should be ~max duration, not sum)")
    print()
    
    print("📋 Detailed Timestamps:")
    print("-" * 80)
    for r in results:
        status = "✅" if r['success'] else "❌"
        print(f"{status} User {r['user_id']:2d}: {r['start_ts']} → {r['end_ts']} ({r['duration_ms']:5d}ms) - {r['http_code']}")
    print("=" * 80)

if __name__ == "__main__":
    main()

