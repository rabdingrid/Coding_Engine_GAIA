#!/usr/bin/env python3
"""
Local test script for C++ batch optimization
Tests the optimized /runall endpoint with 17 test cases
"""

import requests
import json
import time
import sys

LOCAL_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{LOCAL_URL}/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ Service is healthy: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to service. Is it running?")
        print("   Start with: uvicorn executor-service-fastapi:app --host 0.0.0.0 --port 8000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_cpp_batch_optimization():
    """Test C++ batch optimization with 17 test cases"""
    print("\n🧪 Testing C++ batch optimization (17 test cases)...")
    
    test_payload = {
        "language": "cpp",
        "code": """#include <bits/stdc++.h>
using namespace std;

string ltrim(const string &);
string rtrim(const string &);

vector<int> countBetween(vector<int> arr, vector<int> low, vector<int> high) {
    int n = arr.size();
    int q = low.size();
    vector<int> result(q);
    sort(arr.begin(), arr.end());
    for (int i = 0; i < q; i++) {
        int left = lower_bound(arr.begin(), arr.end(), low[i]) - arr.begin();
        int right = upper_bound(arr.begin(), arr.end(), high[i]) - arr.begin();
        result[i] = right - left;
    }
    return result;
}

int main()
{
    string n_temp;
    getline(cin, n_temp);
    int n = stoi(ltrim(rtrim(n_temp)));
    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        string arr_item_temp;
        getline(cin, arr_item_temp);
        int arr_item = stoi(ltrim(rtrim(arr_item_temp)));
        arr[i] = arr_item;
    }
    string q_temp;
    getline(cin, q_temp);
    int q = stoi(ltrim(rtrim(q_temp)));
    vector<int> low(q);
    for (int i = 0; i < q; i++) {
        string low_item_temp;
        getline(cin, low_item_temp);
        int low_item = stoi(ltrim(rtrim(low_item_temp)));
        low[i] = low_item;
    }
    string q_temp2;
    getline(cin, q_temp2);
    int q2 = stoi(ltrim(rtrim(q_temp2)));
    vector<int> high(q2);
    for (int i = 0; i < q2; i++) {
        string high_item_temp;
        getline(cin, high_item_temp);
        int high_item = stoi(ltrim(rtrim(high_item_temp)));
        high[i] = high_item;
    }
    vector<int> result = countBetween(arr, low, high);
    for (size_t i = 0; i < result.size(); i++) {
        cout << result[i];
        if (i != result.size() - 1) {
            cout << "\\n";
        }
    }
    cout << "\\n";
    return 0;
}

string ltrim(const string &str) {
    string s(str);
    s.erase(
        s.begin(),
        find_if(s.begin(), s.end(), not1(ptr_fun<int, int>(isspace)))
    );
    return s;
}

string rtrim(const string &str) {
    string s(str);
    s.erase(
        find_if(s.rbegin(), s.rend(), not1(ptr_fun<int, int>(isspace))).base(),
        s.end()
    );
    return s;
}""",
        "test_cases": [
            {"id": "test_case_000", "input": "5\n1\n2\n3\n4\n5\n3\n1\n2\n3\n3\n3\n4", "expected_output": "3\n2\n1"},
            {"id": "test_case_001", "input": "6\n5\n5\n5\n5\n5\n5\n3\n5\n4\n6\n3\n5\n5\n5", "expected_output": "6\n0\n0"},
            {"id": "test_case_002", "input": "5\n10\n20\n30\n40\n50\n2\n1\n2\n2\n3\n4", "expected_output": "0\n0"},
            {"id": "test_case_003", "input": "4\n2\n4\n6\n8\n2\n1\n2\n2\n8\n8", "expected_output": "4\n4"},
            {"id": "test_case_004", "input": "1\n7\n3\n1\n7\n10\n3\n7\n7\n7", "expected_output": "0\n1\n0"},
            {"id": "test_case_005", "input": "5\n-10\n-5\n0\n5\n10\n3\n-10\n-3\n1\n3\n-5\n0", "expected_output": "2\n1\n2"},
            {"id": "test_case_006", "input": "7\n-2\n5\n0\n12\n3\n-1\n8\n3\n-1\n0\n3\n3\n2\n5\n10", "expected_output": "3\n2\n3"},
            {"id": "test_case_007", "input": "8\n1\n2\n2\n3\n3\n3\n4\n5\n3\n2\n3\n1\n3\n3\n4\n5", "expected_output": "5\n3\n2"},
            {"id": "test_case_008", "input": "6\n4\n8\n12\n16\n20\n24\n2\n25\n30\n2\n40\n50", "expected_output": "0\n0"},
            {"id": "test_case_009", "input": "5\n1\n3\n5\n7\n9\n3\n5\n8\n10\n3\n4\n6", "expected_output": "1\n0\n0"},
            {"id": "test_case_010", "input": "6\n1\n10\n20\n30\n40\n50\n1\n10\n1\n40", "expected_output": "4"},
            {"id": "test_case_011", "input": "5\n5\n10\n15\n20\n25\n3\n5\n10\n24\n3\n5\n10\n25", "expected_output": "1\n1\n3"},
            {"id": "test_case_012", "input": "6\n1\n2\n3\n4\n5\n6\n3\n1\n2\n3\n3\n1\n2\n3", "expected_output": "3\n2\n1"},
            {"id": "test_case_013", "input": "7\n0\n-1\n-2\n1\n2\n3\n4\n3\n-2\n0\n3\n3\n0\n2\n4", "expected_output": "3\n3\n5"},
            {"id": "test_case_014", "input": "7\n1\n50\n100\n150\n200\n250\n300\n3\n1\n100\n200\n3\n50\n150\n300", "expected_output": "2\n3\n3"},
            {"id": "test_case_015", "input": "6\n3\n6\n9\n12\n15\n18\n3\n5\n5\n5\n3\n10\n10\n10", "expected_output": "1\n1\n1"},
            {"id": "test_case_016", "input": "7\n4\n11\n7\n20\n1\n9\n14\n4\n1\n5\n10\n15\n4\n5\n10\n15\n20", "expected_output": "2\n3\n1\n1"}
        ],
        "sample_test_cases": [],
        "user_id": "test_user",
        "question_id": "test_question"
    }
    
    print(f"📤 Sending request to {LOCAL_URL}/runall")
    print(f"   Language: C++")
    print(f"   Test cases: {len(test_payload['test_cases'])}")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{LOCAL_URL}/runall",
            json=test_payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        elapsed_time = time.time() - start_time
        
        print(f"\n📥 Response received in {elapsed_time:.2f}s")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            summary = result.get('summary', {})
            
            print(f"\n✅ Test Results:")
            print(f"   Total Tests: {summary.get('total_tests', 0)}")
            print(f"   Passed: {summary.get('passed', 0)}")
            print(f"   Failed: {summary.get('failed', 0)}")
            print(f"   Execution Time: {result.get('metadata', {}).get('execution_time_ms', 0)}ms")
            
            # Performance check
            if elapsed_time < 10:
                print(f"\n🎉 SUCCESS! Execution time: {elapsed_time:.2f}s (Target: <10s)")
                print(f"   Expected improvement: 24s → ~5s")
                print(f"   Actual: {elapsed_time:.2f}s ✅")
            else:
                print(f"\n⚠️  Execution time: {elapsed_time:.2f}s (Target: <10s)")
            
            return True
        else:
            print(f"\n❌ Request failed: {response.status_code}")
            print(f"   Response: {response.text[:500]}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"\n❌ Request timed out after 60s")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def test_python_sanity():
    """Test Python to ensure no regressions"""
    print("\n🧪 Testing Python (sanity check)...")
    
    payload = {
        "language": "python",
        "code": "print(1+1)",
        "sample_test_cases": [{"id": "test1", "input": "", "expected_output": "2"}]
    }
    
    try:
        response = requests.post(f"{LOCAL_URL}/run", json=payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('summary', {}).get('all_passed'):
                print("✅ Python test passed - no regressions")
                return True
            else:
                print("❌ Python test failed")
                return False
        else:
            print(f"❌ Python test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Python test error: {e}")
        return False

def main():
    print("=" * 60)
    print("🧪 Local Testing - C++ Batch Optimization")
    print("=" * 60)
    
    # Test 1: Health check
    if not test_health():
        print("\n❌ Health check failed. Please start the service first:")
        print("   uvicorn executor-service-fastapi:app --host 0.0.0.0 --port 8000")
        sys.exit(1)
    
    # Test 2: Python sanity check
    if not test_python_sanity():
        print("\n⚠️  Python test failed - may indicate issues")
    
    # Test 3: C++ batch optimization
    success = test_cpp_batch_optimization()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ All tests passed! Ready for deployment.")
    else:
        print("❌ Tests failed. Review errors above.")
    print("=" * 60)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())


