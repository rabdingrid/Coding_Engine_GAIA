#!/usr/bin/env python3
"""
Fix C++ code and measure exact response time
"""

import json
import time
import urllib.request
import ssl
from datetime import datetime

API_URL = "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/runall"
ssl_context = ssl._create_unverified_context()

# Fixed C++ code - The issue seems to be with the algorithm logic
# Based on expected outputs, this might be a different problem
# Let me try a corrected version that matches the expected outputs

# Original code (produces wrong outputs)
ORIGINAL_CPP = """#include <bits/stdc++.h>
using namespace std;

string ltrim(const string &);
string rtrim(const string &);

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
    cout << result << "\\n";
    return 0;
}

string ltrim(const string &str) {
    string s(str);
    s.erase(s.begin(), find_if(s.begin(), s.end(), [](unsigned char ch) {
        return !isspace(ch);
    }));
    return s;
}

string rtrim(const string &str) {
    string s(s);
    s.erase(find_if(s.rbegin(), s.rend(), [](unsigned char ch) {
        return !isspace(ch);
    }).base(), s.end());
    return s;
}"""

# Fixed C++ code - Based on expected outputs, this might need different logic
# Let me analyze: input 13 -> expected 9, got 6
# The pattern suggests it might be counting something different
# Let me try a fix that might work better

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

# Wait, looking at expected outputs again:
# Input 13 -> Expected 9, Got 6
# Input 11 -> Expected 13, Got 6  
# Input 156 -> Expected 232, Got 11
# Input 2089 -> Expected 4046, Got 15

# The expected outputs are HIGHER than inputs, which suggests this might be
# a different problem entirely. But since user asked to "fix" it, let me
# try to understand what the correct algorithm should be.

# Actually, let me check if there's a pattern:
# Maybe it's counting bits? Or something else?
# Let me try a different approach - maybe it's about binary representation operations?

# For now, let me fix the syntax errors first (rtrim had a bug: `string s(s)` should be `string s(str)`)

def test_code(code, code_name, test_cases):
    """Test code and measure exact timing"""
    print(f"\n{'='*80}")
    print(f"🧪 Testing: {code_name}")
    print(f"{'='*80}")
    
    payload = {
        "language": "cpp",
        "code": code,
        "test_cases": test_cases,
        "sample_test_cases": [],
        "user_id": "fix_test_user",
        "question_id": "fix_test"
    }
    
    # Measure exact timing
    start_time = time.time()
    start_timestamp = datetime.now()
    
    try:
        # Serialize payload
        serialize_start = time.time()
        data = json.dumps(payload).encode('utf-8')
        serialize_time = (time.time() - serialize_start) * 1000
        
        # Create request
        req_start = time.time()
        req = urllib.request.Request(
            API_URL,
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        req_time = (time.time() - req_start) * 1000
        
        # Send request and receive response
        network_start = time.time()
        with urllib.request.urlopen(req, timeout=600, context=ssl_context) as response:
            network_time = (time.time() - network_start) * 1000
            
            # Parse response
            parse_start = time.time()
            result_json = response.read().decode('utf-8')
            result = json.loads(result_json)
            parse_time = (time.time() - parse_start) * 1000
        
        end_time = time.time()
        end_timestamp = datetime.now()
        total_time = (end_time - start_time) * 1000
        
        # Extract execution time from response
        execution_time = result.get('metadata', {}).get('execution_time_ms', 0)
        network_overhead = total_time - execution_time
        
        print(f"\n⏱️  EXACT TIMING BREAKDOWN:")
        print(f"{'='*80}")
        print(f"Start Time:        {start_timestamp.strftime('%H:%M:%S.%f')}")
        print(f"End Time:          {end_timestamp.strftime('%H:%M:%S.%f')}")
        print(f"")
        print(f"Total Time:        {total_time:.2f}ms ({total_time/1000:.3f}s)")
        print(f"├─ Serialize:      {serialize_time:.2f}ms")
        print(f"├─ Request Prep:    {req_time:.2f}ms")
        print(f"├─ Network (Total): {network_time:.2f}ms")
        print(f"│  ├─ Send:         ~{network_time * 0.3:.2f}ms (estimated)")
        print(f"│  ├─ Process:      {execution_time}ms (server execution)")
        print(f"│  └─ Receive:      ~{network_time * 0.3:.2f}ms (estimated)")
        print(f"└─ Parse Response: {parse_time:.2f}ms")
        print(f"")
        print(f"Server Execution:  {execution_time}ms ({execution_time/1000:.3f}s)")
        print(f"Network Overhead:  {network_overhead:.2f}ms ({network_overhead/1000:.3f}s)")
        print(f"Overhead %:        {network_overhead/total_time*100:.1f}%")
        
        # Show test results
        print(f"\n📊 TEST RESULTS:")
        print(f"{'='*80}")
        summary = result.get('summary', {})
        print(f"Total Tests: {summary.get('total_tests', 0)}")
        print(f"Passed: {summary.get('passed', 0)}")
        print(f"Failed: {summary.get('failed', 0)}")
        print(f"Pass Rate: {summary.get('pass_percentage', 0)}%")
        
        print(f"\n📋 Individual Test Results:")
        test_results = result.get('test_results', [])
        for tr in test_results:
            status = "✅" if tr.get('passed', False) else "❌"
            print(f"  {status} {tr['test_case_id']}: "
                  f"Input={tr['input']}, Expected={tr['expected_output']}, "
                  f"Got={tr.get('actual_output', '').strip()}, "
                  f"Time={tr.get('execution_time_ms', 0)}ms")
        
        return {
            'code_name': code_name,
            'total_time_ms': total_time,
            'total_time_s': total_time / 1000,
            'execution_time_ms': execution_time,
            'execution_time_s': execution_time / 1000,
            'network_overhead_ms': network_overhead,
            'network_overhead_s': network_overhead / 1000,
            'serialize_time_ms': serialize_time,
            'network_time_ms': network_time,
            'parse_time_ms': parse_time,
            'start_time': start_timestamp.isoformat(),
            'end_time': end_timestamp.isoformat(),
            'passed': summary.get('passed', 0),
            'total_tests': summary.get('total_tests', 0),
            'test_results': test_results
        }
    except Exception as e:
        total_time = (time.time() - start_time) * 1000
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'code_name': code_name,
            'error': str(e),
            'total_time_ms': total_time
        }

def main():
    test_cases = [
        {"id": "test_case_000", "input": "13", "expected_output": "9"},
        {"id": "test_case_001", "input": "11", "expected_output": "13"},
        {"id": "test_case_002", "input": "156", "expected_output": "232"},
        {"id": "test_case_003", "input": "2089", "expected_output": "4046"}
    ]
    
    print("="*80)
    print("🔧 Fix and Test C++ Code")
    print("="*80)
    
    # Test original code first
    print("\n📤 Testing Original Code...")
    original_result = test_code(ORIGINAL_CPP, "Original C++ Code", test_cases)
    
    time.sleep(2)
    
    # Test fixed code
    print("\n📤 Testing Fixed Code (Syntax Fixes)...")
    fixed_result = test_code(FIXED_CPP, "Fixed C++ Code", test_cases)
    
    # Summary
    print(f"\n{'='*80}")
    print("📊 COMPARISON")
    print(f"{'='*80}")
    
    if 'error' not in original_result and 'error' not in fixed_result:
        print(f"\nOriginal Code:")
        print(f"  Total Time: {original_result['total_time_ms']:.2f}ms ({original_result['total_time_s']:.3f}s)")
        print(f"  Execution:  {original_result['execution_time_ms']}ms ({original_result['execution_time_s']:.3f}s)")
        print(f"  Passed:     {original_result['passed']}/{original_result['total_tests']}")
        
        print(f"\nFixed Code:")
        print(f"  Total Time: {fixed_result['total_time_ms']:.2f}ms ({fixed_result['total_time_s']:.3f}s)")
        print(f"  Execution:  {fixed_result['execution_time_ms']}ms ({fixed_result['execution_time_s']:.3f}s)")
        print(f"  Passed:     {fixed_result['passed']}/{fixed_result['total_tests']}")
        
        improvement = original_result['total_time_ms'] - fixed_result['total_time_ms']
        print(f"\nImprovement: {improvement:.2f}ms ({improvement/1000:.3f}s)")
    
    # Save results
    results_file = f"cpp_fix_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w') as f:
        json.dump({
            'original': original_result,
            'fixed': fixed_result
        }, f, indent=2)
    
    print(f"\n💾 Results saved to: {results_file}")

if __name__ == "__main__":
    main()



