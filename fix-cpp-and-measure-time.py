#!/usr/bin/env python3
"""
Fix C++ code and measure exact response time with detailed breakdown
"""

import json
import time
import urllib.request
import ssl
from datetime import datetime

API_URL = "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/runall"
ssl_context = ssl._create_unverified_context()

# Test cases
TEST_CASES = [
    {"id": "test_case_000", "input": "13", "expected_output": "9"},
    {"id": "test_case_001", "input": "11", "expected_output": "13"},
    {"id": "test_case_002", "input": "156", "expected_output": "232"},
    {"id": "test_case_003", "input": "2089", "expected_output": "4046"}
]

# Fixed C++ code - Fixed the rtrim bug and simplified
FIXED_CPP = """#include <iostream>
#include <string>
#include <algorithm>
#include <cctype>

using namespace std;

string ltrim(const string &str) {
    string s(str);
    s.erase(s.begin(), find_if(s.begin(), s.end(), [](unsigned char ch) {
        return !isspace(ch);
    }));
    return s;
}

string rtrim(const string &str) {
    string s(str);
    s.erase(find_if(s.rbegin(), s.rend(), [](unsigned char ch) {
        return !isspace(ch);
    }).base(), s.end());
    return s;
}

long long minOperations(long long n) {
    long long operations = 0;
    while (n > 0) {
        if (n % 2 == 0) {
            n /= 2;
        } else {
            n -= 1;
        }
        operations++;
    }
    return operations;
}

int main() {
    string n_temp;
    getline(cin, n_temp);
    long long n = stoll(ltrim(rtrim(n_temp)));
    long long result = minOperations(n);
    cout << result << endl;
    return 0;
}"""

def measure_exact_timing():
    """Measure exact timing with detailed breakdown"""
    print("="*80)
    print("⏱️  EXACT TIMING MEASUREMENT")
    print("="*80)
    
    payload = {
        "language": "cpp",
        "code": FIXED_CPP,
        "test_cases": TEST_CASES,
        "sample_test_cases": [],
        "user_id": "timing_test_user",
        "question_id": "timing_test"
    }
    
    # Detailed timing breakdown
    timings = {}
    
    # Step 1: Serialize payload
    timings['serialize_start'] = time.time()
    data = json.dumps(payload).encode('utf-8')
    timings['serialize_end'] = time.time()
    timings['serialize_ms'] = (timings['serialize_end'] - timings['serialize_start']) * 1000
    
    # Step 2: Create request
    timings['request_start'] = time.time()
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    timings['request_end'] = time.time()
    timings['request_prep_ms'] = (timings['request_end'] - timings['request_start']) * 1000
    
    # Step 3: Send request (network)
    timings['network_start'] = time.time()
    start_timestamp = datetime.now()
    
    try:
        with urllib.request.urlopen(req, timeout=600, context=ssl_context) as response:
            timings['response_received'] = time.time()
            
            # Step 4: Read response
            timings['read_start'] = time.time()
            result_json = response.read().decode('utf-8')
            timings['read_end'] = time.time()
            timings['read_ms'] = (timings['read_end'] - timings['read_start']) * 1000
            
            # Step 5: Parse JSON
            timings['parse_start'] = time.time()
            result = json.loads(result_json)
            timings['parse_end'] = time.time()
            timings['parse_ms'] = (timings['parse_end'] - timings['parse_start']) * 1000
            
            timings['network_end'] = time.time()
            timings['total_network_ms'] = (timings['network_end'] - timings['network_start']) * 1000
            
            end_timestamp = datetime.now()
            
            # Extract execution time from response
            execution_time = result.get('metadata', {}).get('execution_time_ms', 0)
            
            # Calculate total time
            total_time = (timings['network_end'] - timings['serialize_start']) * 1000
            network_overhead = total_time - execution_time
            
            # Print detailed breakdown
            print(f"\n📊 DETAILED TIMING BREAKDOWN:")
            print(f"{'='*80}")
            print(f"Start Time:        {start_timestamp.strftime('%H:%M:%S.%f')[:-3]}")
            print(f"End Time:          {end_timestamp.strftime('%H:%M:%S.%f')[:-3]}")
            print(f"")
            print(f"Step-by-Step Timing:")
            print(f"├─ 1. Serialize Payload:     {timings['serialize_ms']:.2f}ms")
            print(f"├─ 2. Prepare Request:       {timings['request_prep_ms']:.2f}ms")
            print(f"├─ 3. Network (Total):       {timings['total_network_ms']:.2f}ms")
            print(f"│  ├─ Send Request:          ~{timings['total_network_ms'] * 0.1:.2f}ms (estimated)")
            print(f"│  ├─ Server Processing:     {execution_time}ms (from response)")
            print(f"│  └─ Receive Response:      ~{timings['total_network_ms'] * 0.1:.2f}ms (estimated)")
            print(f"├─ 4. Read Response:         {timings['read_ms']:.2f}ms")
            print(f"└─ 5. Parse JSON:            {timings['parse_ms']:.2f}ms")
            print(f"")
            print(f"{'='*80}")
            print(f"TOTAL TIME:                  {total_time:.2f}ms ({total_time/1000:.3f}s)")
            print(f"├─ Server Execution:         {execution_time}ms ({execution_time/1000:.3f}s)")
            print(f"└─ Network Overhead:        {network_overhead:.2f}ms ({network_overhead/1000:.3f}s)")
            print(f"   Overhead %:               {network_overhead/total_time*100:.1f}%")
            print(f"{'='*80}")
            
            # Show test results
            print(f"\n📋 TEST RESULTS:")
            print(f"{'='*80}")
            summary = result.get('summary', {})
            print(f"Total Tests: {summary.get('total_tests', 0)}")
            print(f"Passed: {summary.get('passed', 0)}")
            print(f"Failed: {summary.get('failed', 0)}")
            print(f"Pass Rate: {summary.get('pass_percentage', 0)}%")
            
            print(f"\nIndividual Test Case Results:")
            test_results = result.get('test_results', [])
            for tr in test_results:
                status = "✅" if tr.get('passed', False) else "❌"
                print(f"  {status} {tr['test_case_id']}:")
                print(f"     Input:    {tr['input']}")
                print(f"     Expected: {tr['expected_output']}")
                print(f"     Got:      {tr.get('actual_output', '').strip()}")
                print(f"     Time:     {tr.get('execution_time_ms', 0)}ms")
            
            return {
                'total_time_ms': total_time,
                'total_time_s': total_time / 1000,
                'execution_time_ms': execution_time,
                'execution_time_s': execution_time / 1000,
                'network_overhead_ms': network_overhead,
                'network_overhead_s': network_overhead / 1000,
                'timings': timings,
                'start_time': start_timestamp.isoformat(),
                'end_time': end_timestamp.isoformat(),
                'passed': summary.get('passed', 0),
                'total_tests': summary.get('total_tests', 0),
                'test_results': test_results
            }
    except Exception as e:
        total_time = (time.time() - timings['serialize_start']) * 1000
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {'error': str(e), 'total_time_ms': total_time}

def main():
    print("\n🔧 Fixing C++ Code and Measuring Exact Response Time")
    print("="*80)
    
    result = measure_exact_timing()
    
    if 'error' not in result:
        print(f"\n✅ Measurement Complete!")
        print(f"\n📊 SUMMARY:")
        print(f"   Total Response Time: {result['total_time_ms']:.2f}ms ({result['total_time_s']:.3f}s)")
        print(f"   Server Execution:   {result['execution_time_ms']}ms ({result['execution_time_s']:.3f}s)")
        print(f"   Network Overhead:    {result['network_overhead_ms']:.2f}ms ({result['network_overhead_s']:.3f}s)")
        print(f"   Tests Passed:        {result['passed']}/{result['total_tests']}")
        
        # Save results
        results_file = f"exact_timing_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\n💾 Detailed results saved to: {results_file}")

if __name__ == "__main__":
    main()



