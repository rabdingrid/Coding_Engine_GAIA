#!/usr/bin/env python3
"""
Comprehensive Load Test: 50, 200, 500 Users in PARALLEL
Generates detailed CSV with container ID, timestamps, and all metrics
"""

import subprocess
import json
import time
from datetime import datetime
import tempfile
import os
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys

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
    """Test a single user - returns all metrics"""
    start_time = time.time()
    start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    
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
        duration_ms = int((end_time - start_time) * 1000)
        
        # Parse HTTP code and time
        http_code = "unknown"
        time_total = 0.0
        for line in result.stdout.split('\n'):
            if line.startswith('HTTP_CODE:'):
                http_code = line.split(':', 1)[1].strip()
            elif line.startswith('TIME_TOTAL:'):
                time_total = float(line.split(':', 1)[1].strip())
        
        # Parse JSON response
        body = '\n'.join([l for l in result.stdout.split('\n') if not l.startswith('HTTP_CODE:') and not l.startswith('TIME_TOTAL:')])
        success = False
        passed = 0
        total = 0
        all_passed = False
        container_id = "unknown"
        replica_id = "unknown"
        execution_time_ms = 0
        cpu_usage = 0.0
        memory_usage = 0
        test_results_detail = []
        
        if http_code == "200" and body:
            try:
                data = json.loads(body)
                metadata = data.get('metadata', {})
                container_id = metadata.get('container_id', 'unknown')
                replica_id = metadata.get('replica', 'unknown')
                execution_time_ms = metadata.get('execution_time_ms', metadata.get('test_execution_time_ms', 0))
                cpu_usage = metadata.get('cpu_usage_percent', 0.0)
                memory_usage = metadata.get('memory_usage_bytes', 0)
                
                summary = data.get('summary', {})
                passed = summary.get('passed', 0)
                total = summary.get('total', len(SIMPLE_QUESTION["test_cases"]))
                all_passed = summary.get('all_passed', False)
                
                # Get detailed test results
                test_results_detail = data.get('test_results', [])
                
                success = True
            except Exception as e:
                pass
        
        return {
            'user_id': f"user_{user_id}",
            'language': language,
            'start_timestamp': start_timestamp,
            'end_timestamp': end_timestamp,
            'duration_ms': duration_ms,
            'http_code': http_code,
            'success': success,
            'container_id': container_id,
            'replica_id': replica_id,
            'execution_time_ms': execution_time_ms,
            'cpu_usage_percent': cpu_usage,
            'memory_usage_bytes': memory_usage,
            'test_cases_passed': passed,
            'test_cases_total': total,
            'all_passed': all_passed,
            'time_total': time_total,
            'test_results': test_results_detail
        }
    except subprocess.TimeoutExpired:
        end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        return {
            'user_id': f"user_{user_id}",
            'language': language,
            'start_timestamp': start_timestamp,
            'end_timestamp': end_timestamp,
            'duration_ms': int((time.time() - start_time) * 1000),
            'http_code': 'timeout',
            'success': False,
            'container_id': 'unknown',
            'replica_id': 'unknown',
            'execution_time_ms': 0,
            'cpu_usage_percent': 0.0,
            'memory_usage_bytes': 0,
            'test_cases_passed': 0,
            'test_cases_total': len(SIMPLE_QUESTION["test_cases"]),
            'all_passed': False,
            'time_total': 0.0,
            'test_results': []
        }
    except Exception as e:
        end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        return {
            'user_id': f"user_{user_id}",
            'language': language,
            'start_timestamp': start_timestamp,
            'end_timestamp': end_timestamp,
            'duration_ms': int((time.time() - start_time) * 1000),
            'http_code': 'error',
            'success': False,
            'container_id': 'unknown',
            'replica_id': 'unknown',
            'execution_time_ms': 0,
            'cpu_usage_percent': 0.0,
            'memory_usage_bytes': 0,
            'test_cases_passed': 0,
            'test_cases_total': len(SIMPLE_QUESTION["test_cases"]),
            'all_passed': False,
            'time_total': 0.0,
            'test_results': [],
            'error': str(e)
        }
    finally:
        try:
            os.unlink(temp_file)
        except:
            pass

def run_test(num_users, test_name):
    """Run load test for specified number of users"""
    print("=" * 100)
    print(f"🧪 {test_name}: {num_users} Users in PARALLEL")
    print("=" * 100)
    print(f"API: {API_URL}")
    print(f"Endpoint: /runall")
    print(f"Test Cases: {len(SIMPLE_QUESTION['test_cases'])} per user")
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 100)
    print()
    
    overall_start = time.time()
    overall_start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    
    print(f"📤 Sending {num_users} requests in PARALLEL...")
    print()
    
    results = []
    completed = 0
    
    with ThreadPoolExecutor(max_workers=num_users) as executor:
        futures = {executor.submit(test_user, i): i for i in range(1, num_users + 1)}
        
        for future in as_completed(futures):
            completed += 1
            result = future.result()
            results.append(result)
            
            status = "✅" if result['success'] else "❌"
            if completed % 10 == 0 or not result['success']:
                print(f"   [{completed:3d}/{num_users}] {status} {result['user_id']:10s} - {result['http_code']:3s} - {result['duration_ms']:5d}ms - Container: {result['container_id'][:20]}...")
    
    overall_time = time.time() - overall_start
    overall_end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    
    # Sort by user_id for consistent output
    results.sort(key=lambda x: int(x['user_id'].split('_')[1]))
    
    # Write detailed CSV
    csv_filename = f"LOAD_TEST_{num_users}_USERS_DETAILED.csv"
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = [
            'User_ID', 'Language', 'HTTP_Code', 'Success',
            'Start_Timestamp', 'End_Timestamp', 'Duration_ms', 'Execution_Time_ms',
            'Container_ID', 'Replica_ID', 'CPU_Usage_%', 'Memory_Usage_Bytes',
            'Test_Cases_Passed', 'Test_Cases_Total', 'All_Passed', 'Time_Total'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for r in results:
            writer.writerow({
                'User_ID': r['user_id'],
                'Language': r['language'],
                'HTTP_Code': r['http_code'],
                'Success': 'Yes' if r['success'] else 'No',
                'Start_Timestamp': r['start_timestamp'],
                'End_Timestamp': r['end_timestamp'],
                'Duration_ms': r['duration_ms'],
                'Execution_Time_ms': r['execution_time_ms'],
                'Container_ID': r['container_id'],
                'Replica_ID': r['replica_id'],
                'CPU_Usage_%': f"{r['cpu_usage_percent']:.2f}",
                'Memory_Usage_Bytes': r['memory_usage_bytes'],
                'Test_Cases_Passed': r['test_cases_passed'],
                'Test_Cases_Total': r['test_cases_total'],
                'All_Passed': 'Yes' if r['all_passed'] else 'No',
                'Time_Total': f"{r['time_total']:.3f}"
            })
    
    # Summary
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print()
    print("=" * 100)
    print("📊 RESULTS SUMMARY")
    print("=" * 100)
    print()
    print(f"Test Start: {overall_start_timestamp}")
    print(f"Test End:   {overall_end_timestamp}")
    print(f"Total Duration: {int(overall_time * 1000)}ms ({overall_time:.2f}s)")
    print()
    print(f"✅ Successful: {len(successful)}/{num_users}")
    print(f"❌ Failed: {len(failed)}/{num_users}")
    if num_users > 0:
        success_rate = (len(successful) / num_users) * 100
        print(f"Success Rate: {success_rate:.1f}%")
    print()
    
    if successful:
        durations = [r['duration_ms'] for r in successful]
        exec_times = [r['execution_time_ms'] for r in successful if r['execution_time_ms'] > 0]
        
        print(f"⏱️  Performance Metrics (Successful):")
        print(f"   Duration - Min: {min(durations)}ms, Max: {max(durations)}ms, Avg: {int(sum(durations) / len(durations))}ms")
        if exec_times:
            print(f"   Execution - Min: {min(exec_times)}ms, Max: {max(exec_times)}ms, Avg: {int(sum(exec_times) / len(exec_times))}ms")
        print()
        
        # Container distribution
        containers = {}
        replicas = {}
        for r in successful:
            cid = r['container_id']
            rid = r['replica_id']
            containers[cid] = containers.get(cid, 0) + 1
            replicas[rid] = replicas.get(rid, 0) + 1
        
        print("🔄 Container Distribution:")
        for cid, count in sorted(containers.items(), key=lambda x: x[1], reverse=True):
            print(f"   {cid[:50]}: {count} requests")
        print()
        
        print("🔄 Replica Distribution:")
        for rid, count in sorted(replicas.items(), key=lambda x: x[1], reverse=True):
            print(f"   {rid}: {count} requests")
        print()
    
    print(f"📄 Detailed CSV saved to: {csv_filename}")
    print("=" * 100)
    print()
    
    return results

def main():
    test_configs = [
        (50, "TEST 1"),
        (200, "TEST 2"),
        (500, "TEST 3")
    ]
    
    all_results = {}
    
    for num_users, test_name in test_configs:
        print(f"\n\n{'='*100}")
        print(f"🚀 STARTING {test_name}")
        print(f"{'='*100}\n")
        
        results = run_test(num_users, test_name)
        all_results[num_users] = results
        
        # Wait a bit between tests
        if test_name != "TEST 3":
            print(f"⏳ Waiting 10 seconds before next test...")
            time.sleep(10)
    
    # Final summary
    print("\n\n" + "=" * 100)
    print("📊 FINAL SUMMARY - ALL TESTS")
    print("=" * 100)
    print()
    for num_users, results in all_results.items():
        successful = [r for r in results if r['success']]
        success_rate = (len(successful) / num_users * 100) if num_users > 0 else 0
        avg_duration = int(sum(r['duration_ms'] for r in successful) / len(successful)) if successful else 0
        print(f"{num_users:3d} Users: {len(successful):3d}/{num_users:3d} successful ({success_rate:5.1f}%) - Avg: {avg_duration:4d}ms")
    print("=" * 100)

if __name__ == "__main__":
    main()

