#!/usr/bin/env python3
"""
Test script to simulate the external backend request format
and verify it works with the FastAPI code execution service
"""

import requests
import json
import sys
import os

# Configuration
EXECUTOR_SERVICE_URL = os.getenv(
    'EXECUTOR_SERVICE_URL',
    'https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io'
)

# Simulate the external backend request format
EXTERNAL_BACKEND_REQUEST = {
    "question_id": "22c620aa-b462-4ca5-adee-74ef95598862",
    "language": "cpp",
    "code": """#include <bits/stdc++.h>
using namespace std;

string ltrim(const string &);
string rtrim(const string &);

vector<int> countBetween(vector<int> arr, vector<int> low, vector<int> high) {
    int n = arr.size();
    int q = low.size();
    vector<int> result(q);
    // Sort array for binary search
    sort(arr.begin(), arr.end());
    for (int i = 0; i < q; i++) {
        // first index >= low[i]
        int left = lower_bound(arr.begin(), arr.end(), low[i]) - arr.begin();
        // first index > high[i]
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
    "mode": "run"
}


def check_service_health():
    """Check if the code execution service is accessible"""
    print("🔍 Checking service health...")
    try:
        response = requests.get(f"{EXECUTOR_SERVICE_URL}/health", timeout=10)
        if response.status_code == 200:
            print(f"✅ Service is healthy: {response.json()}")
            return True
        else:
            print(f"❌ Service returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot reach service: {e}")
        print(f"   URL: {EXECUTOR_SERVICE_URL}")
        return False


def convert_external_request_to_fastapi_format(external_request):
    """
    Convert external backend request format to FastAPI format.
    
    In a real scenario, you would fetch test cases from your database
    using the question_id. For this test, we'll use sample test cases.
    """
    # NOTE: In your actual backend, you would do:
    # question = db.questions.find_one({id: external_request['question_id']})
    # sample_test_cases = question.sample_test_cases
    
    # For testing, we'll create sample test cases
    sample_test_cases = [
        {
            "id": "sample_1",
            "input": "5\n1 2 3 4 5\n2\n1 3\n2 4",
            "expected_output": "2\n3"
        }
    ]
    
    fastapi_request = {
        "language": external_request["language"],
        "code": external_request["code"],
        "sample_test_cases": sample_test_cases,  # ✅ Required!
        "question_id": external_request["question_id"],
        "user_id": "test_user"  # Optional
    }
    
    return fastapi_request


def test_run_endpoint():
    """Test the /run endpoint with correct format"""
    print("\n🧪 Testing /run endpoint...")
    
    # Convert external request format to FastAPI format
    fastapi_request = convert_external_request_to_fastapi_format(EXTERNAL_BACKEND_REQUEST)
    
    print(f"📤 Sending request to: {EXECUTOR_SERVICE_URL}/run")
    print(f"📋 Request format:")
    print(json.dumps({
        "language": fastapi_request["language"],
        "code": fastapi_request["code"][:50] + "...",
        "sample_test_cases": fastapi_request["sample_test_cases"],
        "question_id": fastapi_request["question_id"]
    }, indent=2))
    
    try:
        response = requests.post(
            f"{EXECUTOR_SERVICE_URL}/run",
            json=fastapi_request,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        print(f"\n📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Request successful!")
            print(f"   Execution ID: {result.get('execution_id')}")
            print(f"   Summary: {result.get('summary')}")
            return True
        elif response.status_code == 503:
            print("❌ 503 Service Unavailable")
            print("   This means the service is not running or overloaded")
            print(f"   Response: {response.text}")
            return False
        elif response.status_code == 400:
            print("❌ 400 Bad Request")
            print("   Check if request format is correct")
            print(f"   Response: {response.text}")
            return False
        else:
            print(f"❌ Unexpected status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out (60s)")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False


def main():
    print("=" * 60)
    print("🔧 External Backend Request Format Test")
    print("=" * 60)
    
    # Step 1: Check service health
    if not check_service_health():
        print("\n❌ Service is not accessible. Please check:")
        print("   1. Is the service running?")
        print("   2. Is the URL correct?")
        print("   3. Is there a network/firewall issue?")
        sys.exit(1)
    
    # Step 2: Test the request
    success = test_run_endpoint()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ Test passed! Your external backend should work with this format.")
    else:
        print("❌ Test failed! Check the error messages above.")
        print("\n💡 Next steps:")
        print("   1. Update your external backend to fetch test cases from database")
        print("   2. Format request with 'sample_test_cases' array")
        print("   3. See TROUBLESHOOT_503_ERROR.md for details")
    print("=" * 60)


if __name__ == "__main__":
    main()



