#!/usr/bin/env python3
"""
Verify Network Overhead and Execution Times with Actual API Calls
Tests Python vs C++ to verify findings
"""

import json
import time
import urllib.request
import ssl
from datetime import datetime

API_URL = "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/runall"
ssl_context = ssl._create_unverified_context()

# Test case: 200 boxes (medium size for testing)
TEST_INPUT = "200\n" + "\n".join([str(i) for i in range(1, 201)])

# Python O(n²) solution
PYTHON_N2 = """def findTotalWeight(boxes):
    total = 0
    while boxes:
        min_weight = min(boxes)
        min_idx = boxes.index(min_weight)
        start = max(0, min_idx - 1)
        end = min(len(boxes), min_idx + 2)
        total += min_weight
        boxes = boxes[:start] + boxes[end:]
    return total

n = int(input())
boxes = [int(input()) for _ in range(n)]
result = findTotalWeight(boxes)
print(result)"""

# Python O(n log n) solution
PYTHON_OPTIMIZED = """import heapq

def findTotalWeight(boxes):
    if not boxes:
        return 0
    heap = [(weight, idx) for idx, weight in enumerate(boxes)]
    heapq.heapify(heap)
    removed = [False] * len(boxes)
    total = 0
    
    while heap:
        weight, idx = heapq.heappop(heap)
        if removed[idx]:
            continue
        removed[idx] = True
        if idx > 0:
            removed[idx-1] = True
        if idx < len(boxes) - 1:
            removed[idx+1] = True
        total += weight
    
    return total

n = int(input())
boxes = [int(input()) for _ in range(n)]
result = findTotalWeight(boxes)
print(result)"""

# C++ O(n²) solution
CPP_N2 = """#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>

using namespace std;

int findTotalWeight(vector<int>& boxes) {
    int total = 0;
    while (!boxes.empty()) {
        int min_weight = INT_MAX;
        int min_idx = -1;
        
        for (int i = 0; i < boxes.size(); i++) {
            if (boxes[i] < min_weight) {
                min_weight = boxes[i];
                min_idx = i;
            }
        }
        
        total += min_weight;
        
        int start = max(0, min_idx - 1);
        int end = min((int)boxes.size(), min_idx + 2);
        boxes.erase(boxes.begin() + start, boxes.begin() + end);
    }
    return total;
}

int main() {
    int n;
    cin >> n;
    vector<int> boxes(n);
    for (int i = 0; i < n; i++) {
        cin >> boxes[i];
    }
    cout << findTotalWeight(boxes) << endl;
    return 0;
}"""

def test_implementation(language, code, test_name, test_input):
    """Test an implementation and measure all timings"""
    print(f"\n{'='*80}")
    print(f"🧪 Testing: {test_name}")
    print(f"{'='*80}")
    print(f"Language: {language}")
    
    # Prepare payload
    payload = {
        "language": language,
        "code": code,
        "test_cases": [{
            "id": f"test_{test_name.lower().replace(' ', '_')}",
            "input": test_input,
            "expected_output": "0"  # Will calculate actual
        }],
        "sample_test_cases": [],
        "user_id": f"timing_test_{language}",
        "question_id": "timing_test"
    }
    
    # Measure total time
    total_start = time.time()
    
    # Measure network send time
    network_send_start = time.time()
    data = json.dumps(payload).encode('utf-8')
    network_send_time = (time.time() - network_send_start) * 1000
    
    try:
        # Make request
        req = urllib.request.Request(
            API_URL,
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        request_start = time.time()
        with urllib.request.urlopen(req, timeout=600, context=ssl_context) as response:
            request_time = (time.time() - request_start) * 1000
            
            # Parse response
            parse_start = time.time()
            result_json = response.read().decode('utf-8')
            result = json.loads(result_json)
            parse_time = (time.time() - parse_start) * 1000
            
            total_time = (time.time() - total_start) * 1000
            
            # Extract execution time from response
            execution_time = result.get('metadata', {}).get('execution_time_ms', 0)
            network_overhead = total_time - execution_time
            
            print(f"\n📊 Timing Breakdown:")
            print(f"   Total Time:        {total_time:.2f}ms ({total_time/1000:.3f}s)")
            print(f"   Execution Time:    {execution_time}ms ({execution_time/1000:.3f}s)")
            print(f"   Network Overhead:  {network_overhead:.2f}ms ({network_overhead/1000:.3f}s)")
            print(f"   Overhead %:        {network_overhead/total_time*100:.1f}%")
            print(f"   Request Time:      {request_time:.2f}ms")
            print(f"   Parse Time:        {parse_time:.2f}ms")
            print(f"   Serialize Time:    {network_send_time:.2f}ms")
            
            # Check if passed
            summary = result.get('summary', {})
            passed = summary.get('passed', 0)
            total_tests = summary.get('total_tests', 0)
            print(f"\n✅ Results: {passed}/{total_tests} tests passed")
            
            return {
                'test_name': test_name,
                'language': language,
                'total_time_ms': total_time,
                'total_time_s': total_time / 1000,
                'execution_time_ms': execution_time,
                'execution_time_s': execution_time / 1000,
                'network_overhead_ms': network_overhead,
                'network_overhead_s': network_overhead / 1000,
                'overhead_percentage': network_overhead / total_time * 100,
                'passed': passed,
                'total_tests': total_tests
            }
    except Exception as e:
        total_time = (time.time() - total_start) * 1000
        print(f"\n❌ Error: {str(e)}")
        return {
            'test_name': test_name,
            'language': language,
            'error': str(e),
            'total_time_ms': total_time
        }

def main():
    print("="*80)
    print("🔍 Verifying Network Overhead and Execution Times")
    print("="*80)
    print(f"Test Case: 200 boxes")
    print(f"API URL: {API_URL}")
    
    results = []
    
    # Test 1: Python O(n²)
    result1 = test_implementation("python", PYTHON_N2, "Python O(n²)", TEST_INPUT)
    results.append(result1)
    
    # Wait a bit between requests
    time.sleep(2)
    
    # Test 2: Python O(n log n)
    result2 = test_implementation("python", PYTHON_OPTIMIZED, "Python O(n log n)", TEST_INPUT)
    results.append(result2)
    
    # Wait a bit between requests
    time.sleep(2)
    
    # Test 3: C++ O(n²)
    result3 = test_implementation("cpp", CPP_N2, "C++ O(n²)", TEST_INPUT)
    results.append(result3)
    
    # Generate comparison
    print(f"\n{'='*80}")
    print("📊 COMPARISON SUMMARY")
    print(f"{'='*80}")
    
    print(f"\n{'Test':<25} {'Total Time':<15} {'Execution':<15} {'Network':<15} {'Overhead %':<12}")
    print("-" * 80)
    
    for r in results:
        if 'error' not in r:
            print(f"{r['test_name']:<25} {r['total_time_s']:.3f}s ({r['total_time_ms']:.0f}ms)  "
                  f"{r['execution_time_s']:.3f}s ({r['execution_time_ms']:.0f}ms)  "
                  f"{r['network_overhead_s']:.3f}s ({r['network_overhead_ms']:.0f}ms)  "
                  f"{r['overhead_percentage']:.1f}%")
    
    # Verify network overhead consistency
    print(f"\n{'='*80}")
    print("🔍 Network Overhead Analysis")
    print(f"{'='*80}")
    
    overheads = [r['network_overhead_ms'] for r in results if 'error' not in r]
    if overheads:
        avg_overhead = sum(overheads) / len(overheads)
        min_overhead = min(overheads)
        max_overhead = max(overheads)
        variance = max_overhead - min_overhead
        
        print(f"Average Network Overhead: {avg_overhead:.2f}ms ({avg_overhead/1000:.3f}s)")
        print(f"Min Network Overhead:     {min_overhead:.2f}ms ({min_overhead/1000:.3f}s)")
        print(f"Max Network Overhead:     {max_overhead:.2f}ms ({max_overhead/1000:.3f}s)")
        print(f"Variance:                 {variance:.2f}ms ({variance/1000:.3f}s)")
        
        if variance < 200:  # Less than 200ms variance
            print(f"\n✅ Network overhead is CONSISTENT (variance < 200ms)")
            print(f"   This confirms network overhead is ~constant across languages")
        else:
            print(f"\n⚠️  Network overhead varies significantly")
            print(f"   This may indicate other factors affecting timing")
    
    # Compare execution times
    print(f"\n{'='*80}")
    print("⚡ Execution Time Comparison")
    print(f"{'='*80}")
    
    exec_times = {r['test_name']: r['execution_time_ms'] for r in results if 'error' not in r}
    
    if 'Python O(n²)' in exec_times and 'Python O(n log n)' in exec_times:
        py_n2 = exec_times['Python O(n²)']
        py_opt = exec_times['Python O(n log n)']
        speedup = py_n2 / py_opt if py_opt > 0 else 0
        print(f"Python O(n²):     {py_n2:.0f}ms ({py_n2/1000:.3f}s)")
        print(f"Python O(n log n): {py_opt:.0f}ms ({py_opt/1000:.3f}s)")
        print(f"Speedup: {speedup:.2f}x faster with optimized algorithm ⚡")
    
    if 'Python O(n²)' in exec_times and 'C++ O(n²)' in exec_times:
        py_n2 = exec_times['Python O(n²)']
        cpp_n2 = exec_times['C++ O(n²)']
        speedup = py_n2 / cpp_n2 if cpp_n2 > 0 else 0
        print(f"\nPython O(n²): {py_n2:.0f}ms ({py_n2/1000:.3f}s)")
        print(f"C++ O(n²):    {cpp_n2:.0f}ms ({cpp_n2/1000:.3f}s)")
        print(f"Speedup: {speedup:.2f}x faster with C++ ⚡")
    
    print(f"\n{'='*80}")
    
    # Save results
    results_file = f"timing_verification_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"💾 Results saved to: {results_file}")

if __name__ == "__main__":
    main()



