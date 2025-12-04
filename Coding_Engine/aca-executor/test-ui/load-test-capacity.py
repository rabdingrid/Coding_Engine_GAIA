#!/usr/bin/env python3
"""
Load Test using curl (via Python) - Tests real capacity with many parallel requests
Uses C++ code to test the actual capacity of the system
"""

import subprocess
import json
import time
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

API_URL = "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io"
NUM_USERS = int(sys.argv[1]) if len(sys.argv) > 1 else 30

# C++ code (working version)
CPP_CODE = """#include <bits/stdc++.h>
using namespace std;

int findTotalWeight(vector<int> cans) {
    int total = 0;
    while (!cans.empty()) {
        int minVal = INT_MAX;
        int idx = -1;
        for (int i = 0; i < cans.size(); i++) {
            if (cans[i] < minVal) {
                minVal = cans[i];
                idx = i;
            }
        }
        total += minVal;
        int start = max(0, idx - 1);
        int end = min((int)cans.size() - 1, idx + 1);
        for (int i = end; i >= start; i--) {
            cans.erase(cans.begin() + i);
        }
    }
    return total;
}

int main() {
    int n;
    cin >> n;
    vector<int> cans(n);
    for (int i = 0; i < n; i++) {
        cin >> cans[i];
    }
    cout << findTotalWeight(cans) << endl;
    return 0;
}"""

# Test cases
TEST_CASES = [
    {"id": "test_1", "input": "7\n6\n4\n9\n10\n34\n56\n54", "expected_output": "68\n"},
    {"id": "test_2", "input": "8\n132\n45\n65\n765\n345\n243\n75\n67", "expected_output": "1120\n"}
]

def submit_request(user_id):
    """Submit a single request using curl"""
    start_time = time.time()
    
    # Create payload
    payload = {
        "language": "cpp",
        "code": CPP_CODE,
        "test_cases": TEST_CASES,
        "user_id": user_id,
        "question_id": "warehouse_box_removal",
        "timeout": 5
    }
    
    # Write payload to temp file
    import tempfile
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
            else:
                continue
        
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
            "user_id": user_id,
            "http_code": http_code or "error",
            "wait_time_ms": wait_time_ms,
            "exec_time_ms": exec_time,
            "container_id": container_id,
            "replica": replica,
            "all_passed": all_passed,
            "time_total": time_total or 0,
            "success": http_code == "200"
        }
    except subprocess.TimeoutExpired:
        return {
            "user_id": user_id,
            "http_code": "timeout",
            "wait_time_ms": int((time.time() - start_time) * 1000),
            "exec_time_ms": 0,
            "container_id": "unknown",
            "replica": "unknown",
            "all_passed": False,
            "time_total": 0,
            "success": False
        }
    except Exception as e:
        return {
            "user_id": user_id,
            "http_code": "error",
            "wait_time_ms": int((time.time() - start_time) * 1000),
            "exec_time_ms": 0,
            "container_id": "unknown",
            "replica": "unknown",
            "all_passed": False,
            "time_total": 0,
            "success": False,
            "error": str(e)
        }
    finally:
        # Cleanup temp file
        import os
        try:
            os.unlink(temp_file)
        except:
            pass

def main():
    print("=" * 80)
    print("🚀 CURL LOAD TEST - REAL CAPACITY TESTING")
    print("=" * 80)
    print(f"API URL: {API_URL}")
    print(f"Number of parallel users: {NUM_USERS}")
    print(f"Language: C++ (all users)")
    print(f"Question: Warehouse Box Removal")
    print("=" * 80)
    print()
    
    print(f"⚡ Starting parallel execution of {NUM_USERS} users...")
    print(f"   All requests sent simultaneously...")
    print()
    
    overall_start = time.time()
    results = []
    completed = 0
    
    # Submit all requests in parallel
    with ThreadPoolExecutor(max_workers=NUM_USERS) as executor:
        futures = {executor.submit(submit_request, f"user_{i+1}"): i+1 for i in range(NUM_USERS)}
        
        for future in as_completed(futures):
            completed += 1
            result = future.result()
            results.append(result)
            
            if completed % 10 == 0:
                print(f"   Progress: {completed}/{NUM_USERS} requests completed...")
    
    overall_time = time.time() - overall_start
    overall_time_ms = int(overall_time * 1000)
    
    print("✅ All requests completed!")
    print()
    
    # Analyze results
    print("=" * 80)
    print("📊 RESULTS ANALYSIS")
    print("=" * 80)
    print()
    
    total = len(results)
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"📈 Summary:")
    print(f"   Total requests: {total}")
    print(f"   ✅ Successful: {len(successful)}")
    print(f"   ❌ Failed: {len(failed)}")
    if total > 0:
        success_rate = (len(successful) / total) * 100
        print(f"   Success rate: {success_rate:.1f}%")
    print()
    
    if successful:
        wait_times = [r['wait_time_ms'] for r in successful]
        exec_times = [r['exec_time_ms'] for r in successful]
        
        print(f"⏱️  Wait Times (Time until response received):")
        print(f"   Min: {min(wait_times)}ms")
        print(f"   Max: {max(wait_times)}ms")
        print(f"   Avg: {int(sum(wait_times) / len(wait_times))}ms")
        if max(wait_times) < 5000:
            print(f"   Target: < 5000ms ✅")
        else:
            print(f"   Target: < 5000ms ❌ (Max: {max(wait_times)}ms)")
        print()
        
        print(f"⚡ Execution Times:")
        print(f"   Min: {min(exec_times)}ms")
        print(f"   Max: {max(exec_times)}ms")
        print(f"   Avg: {int(sum(exec_times) / len(exec_times))}ms")
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
        print(f"✅ All tests passed: {all_passed}/{len(successful)}")
        print()
        
        # Capacity analysis
        total_exec_time = sum(exec_times)
        efficiency = (total_exec_time / overall_time_ms * 100) if overall_time_ms > 0 else 0
        req_per_sec = (len(successful) / overall_time) if overall_time > 0 else 0
        
        print("📈 Capacity Analysis:")
        print(f"   Total time: {overall_time_ms}ms ({overall_time:.2f}s)")
        print(f"   Requests handled: {len(successful)}")
        print(f"   Requests/second: {req_per_sec:.2f}")
        print(f"   Concurrent capacity: ~{len(successful)} requests in {overall_time_ms}ms")
        print(f"   Parallel efficiency: {efficiency:.1f}%")
        print()
    
    # Show failures
    if failed:
        print("❌ Failed Requests (first 10):")
        for r in failed[:10]:
            print(f"   {r['user_id']}: {r['http_code']}")
        print()
    
    # Show sample results
    print("=" * 80)
    print("📋 SAMPLE RESULTS (First 20)")
    print("=" * 80)
    print(f"{'User':<10} {'Status':<8} {'Wait(ms)':<10} {'Exec(ms)':<10} {'Container':<25} {'All Pass':<10}")
    print("-" * 80)
    for r in results[:20]:
        status = "✅" if r['success'] else f"❌{r['http_code']}"
        pass_icon = "✅" if r['all_passed'] else "❌"
        container_short = r['container_id'][:25] if len(r['container_id']) > 25 else r['container_id']
        print(f"{r['user_id']:<10} {status:<8} {r['wait_time_ms']:<10} {r['exec_time_ms']:<10} {container_short:<25} {pass_icon:<10}")
    
    print()
    print("=" * 80)
    print("✅ Load test complete!")
    print("=" * 80)
    print()
    print("📊 Final Capacity Summary:")
    print(f"   Current replicas: 2 (min)")
    print(f"   Expected capacity: 2 × 10 = 20 concurrent requests")
    print(f"   Actual requests handled: {len(successful)}")
    if successful:
        print(f"   Max wait time: {max([r['wait_time_ms'] for r in successful])}ms")
        print(f"   Average wait time: {int(sum([r['wait_time_ms'] for r in successful]) / len(successful))}ms")
    print()

if __name__ == "__main__":
    main()

