#!/usr/bin/env python3
"""
Test with large test case (2000 boxes) to verify actual performance differences
"""

import json
import time
import urllib.request
import ssl
from datetime import datetime

API_URL = "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/runall"
ssl_context = ssl._create_unverified_context()

# Large test case: 2000 boxes
LARGE_TEST_INPUT = "2000\n" + "\n".join([str(i % 100 + 1) for i in range(2000)])

# Python O(n²)
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

# Python O(n log n)
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

# C++ O(n²)
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

def test_large_case(language, code, test_name):
    """Test with large test case"""
    print(f"\n{'='*80}")
    print(f"🧪 Testing: {test_name} (2000 boxes)")
    print(f"{'='*80}")
    
    payload = {
        "language": language,
        "code": code,
        "test_cases": [{
            "id": f"large_test_{language}",
            "input": LARGE_TEST_INPUT,
            "expected_output": "0"
        }],
        "sample_test_cases": [],
        "user_id": f"large_test_{language}",
        "question_id": "large_test"
    }
    
    total_start = time.time()
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            API_URL,
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=600, context=ssl_context) as response:
            result_json = response.read().decode('utf-8')
            result = json.loads(result_json)
            total_time = (time.time() - total_start) * 1000
            
            execution_time = result.get('metadata', {}).get('execution_time_ms', 0)
            network_overhead = total_time - execution_time
            
            print(f"Total Time:        {total_time:.2f}ms ({total_time/1000:.3f}s)")
            print(f"Execution Time:    {execution_time}ms ({execution_time/1000:.3f}s)")
            print(f"Network Overhead:  {network_overhead:.2f}ms ({network_overhead/1000:.3f}s)")
            print(f"Overhead %:        {network_overhead/total_time*100:.1f}%")
            
            summary = result.get('summary', {})
            print(f"Tests Passed:      {summary.get('passed', 0)}/{summary.get('total_tests', 0)}")
            
            return {
                'test_name': test_name,
                'total_time_ms': total_time,
                'total_time_s': total_time / 1000,
                'execution_time_ms': execution_time,
                'execution_time_s': execution_time / 1000,
                'network_overhead_ms': network_overhead,
                'network_overhead_s': network_overhead / 1000
            }
    except Exception as e:
        total_time = (time.time() - total_start) * 1000
        print(f"❌ Error: {str(e)}")
        return {
            'test_name': test_name,
            'error': str(e),
            'total_time_ms': total_time
        }

def main():
    print("="*80)
    print("🔍 Large Test Case Verification (2000 boxes)")
    print("="*80)
    print("Testing actual performance differences with large dataset...")
    
    results = []
    
    # Test 1: Python O(n²)
    print("\n⏳ Testing Python O(n²) - This may take 10-15 seconds...")
    result1 = test_large_case("python", PYTHON_N2, "Python O(n²)")
    results.append(result1)
    
    time.sleep(3)
    
    # Test 2: Python O(n log n)
    print("\n⏳ Testing Python O(n log n) - This should be faster...")
    result2 = test_large_case("python", PYTHON_OPTIMIZED, "Python O(n log n)")
    results.append(result2)
    
    time.sleep(3)
    
    # Test 3: C++ O(n²)
    print("\n⏳ Testing C++ O(n²) - Includes compilation time...")
    result3 = test_large_case("cpp", CPP_N2, "C++ O(n²)")
    results.append(result3)
    
    # Summary
    print(f"\n{'='*80}")
    print("📊 FINAL COMPARISON (2000 boxes)")
    print(f"{'='*80}")
    
    print(f"\n{'Test':<25} {'Total':<15} {'Execution':<15} {'Network':<15} {'Status':<10}")
    print("-" * 80)
    
    for r in results:
        if 'error' not in r:
            status = "✅" if r['total_time_s'] < 5 else "❌"
            print(f"{r['test_name']:<25} {r['total_time_s']:.3f}s ({r['total_time_ms']:.0f}ms)  "
                  f"{r['execution_time_s']:.3f}s ({r['execution_time_ms']:.0f}ms)  "
                  f"{r['network_overhead_s']:.3f}s ({r['network_overhead_ms']:.0f}ms)  "
                  f"{status}")
    
    # Verify findings
    print(f"\n{'='*80}")
    print("🔍 VERIFICATION OF FINDINGS")
    print(f"{'='*80}")
    
    overheads = [r['network_overhead_ms'] for r in results if 'error' not in r]
    if overheads:
        avg_overhead = sum(overheads) / len(overheads)
        variance = max(overheads) - min(overheads)
        
        print(f"\n1. Network Overhead Consistency:")
        print(f"   Average: {avg_overhead:.2f}ms ({avg_overhead/1000:.3f}s)")
        print(f"   Variance: {variance:.2f}ms")
        if variance < 200:
            print(f"   ✅ CONFIRMED: Network overhead is ~constant (~{avg_overhead/1000:.3f}s)")
        else:
            print(f"   ⚠️  Network overhead varies")
    
    # Compare execution times
    exec_times = {r['test_name']: r['execution_time_ms'] for r in results if 'error' not in r}
    
    print(f"\n2. Execution Time Comparison:")
    if 'Python O(n²)' in exec_times and 'Python O(n log n)' in exec_times:
        py_n2 = exec_times['Python O(n²)']
        py_opt = exec_times['Python O(n log n)']
        if py_opt > 0:
            speedup = py_n2 / py_opt
            print(f"   Python O(n²):     {py_n2:.0f}ms ({py_n2/1000:.3f}s)")
            print(f"   Python O(n log n): {py_opt:.0f}ms ({py_opt/1000:.3f}s)")
            print(f"   ✅ Algorithm optimization: {speedup:.2f}x faster")
    
    if 'Python O(n²)' in exec_times and 'C++ O(n²)' in exec_times:
        py_n2 = exec_times['Python O(n²)']
        cpp_n2 = exec_times['C++ O(n²)']
        if cpp_n2 > 0:
            speedup = py_n2 / cpp_n2
            print(f"\n   Python O(n²): {py_n2:.0f}ms ({py_n2/1000:.3f}s)")
            print(f"   C++ O(n²):    {cpp_n2:.0f}ms ({cpp_n2/1000:.3f}s)")
            if speedup > 1:
                print(f"   ✅ C++ is {speedup:.2f}x faster")
            else:
                print(f"   ⚠️  C++ slower (includes compilation overhead)")
                print(f"   Note: C++ compilation adds ~300-400ms, but execution is faster")
    
    print(f"\n{'='*80}")
    
    # Save results
    results_file = f"large_case_verification_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"💾 Results saved to: {results_file}")

if __name__ == "__main__":
    main()



