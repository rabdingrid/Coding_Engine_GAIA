#!/usr/bin/env python3
"""
Test FastAPI Endpoints with Python
Tests /run, /runall, and /submit with 20 test cases each
"""

import json
import urllib.request
import urllib.parse
import sys
import random

BASE_URL = "http://localhost:8000"

def make_request(endpoint, data):
    """Make HTTP POST request"""
    url = f"{BASE_URL}{endpoint}"
    data_json = json.dumps(data).encode('utf-8')
    
    req = urllib.request.Request(
        url,
        data=data_json,
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"❌ HTTP Error {e.code}: {error_body}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def generate_test_cases(count=20, prefix="test"):
    """Generate test cases for sum problem"""
    test_cases = []
    for i in range(1, count + 1):
        a = random.randint(1, 10000)
        b = random.randint(1, 10000)
        sum_val = a + b
        test_cases.append({
            "id": f"{prefix}_{i}",
            "input": f"{a}\n{b}",
            "expected_output": str(sum_val)
        })
    return test_cases

def test_run_endpoint():
    """Test /run endpoint with sample test cases"""
    print("\n" + "="*60)
    print("📝 Test 1: /run endpoint - Sample Test Cases")
    print("="*60)
    
    python_code = """a = int(input())
b = int(input())
print(a + b)"""
    
    sample_test_cases = generate_test_cases(20, "sample")
    
    request_data = {
        "language": "python",
        "code": python_code,
        "sample_test_cases": sample_test_cases,
        "user_id": "test_user_1",
        "question_id": "test_q1",
        "timeout": 5
    }
    
    print(f"Sending request with {len(sample_test_cases)} sample test cases...")
    response = make_request("/run", request_data)
    
    if response:
        print("✅ Request successful!")
        summary = response.get('summary', {})
        print(f"   Total Tests: {summary.get('total_tests', 0)}")
        print(f"   Passed: {summary.get('passed', 0)}")
        print(f"   Failed: {summary.get('failed', 0)}")
        print(f"   Pass Percentage: {summary.get('pass_percentage', 0)}%")
        
        # Show first few test results
        test_results = response.get('test_results', [])
        if test_results:
            print(f"\n   First 3 test results:")
            for tr in test_results[:3]:
                status = tr.get('status', 'unknown')
                passed = tr.get('passed', False)
                status_icon = "✅" if passed else "❌"
                print(f"   {status_icon} {tr.get('test_case_id')}: {status}")
        
        return True
    return False

def test_runall_endpoint():
    """Test /runall endpoint with all test cases"""
    print("\n" + "="*60)
    print("📝 Test 2: /runall endpoint - All Test Cases")
    print("="*60)
    
    python_code = """a = int(input())
b = int(input())
print(a + b)"""
    
    all_test_cases = generate_test_cases(20, "test")
    
    request_data = {
        "language": "python",
        "code": python_code,
        "test_cases": all_test_cases,
        "sample_test_cases": [],
        "user_id": "test_user_1",
        "question_id": "test_q1",
        "timeout": 5
    }
    
    print(f"Sending request with {len(all_test_cases)} test cases...")
    response = make_request("/runall", request_data)
    
    if response:
        print("✅ Request successful!")
        summary = response.get('summary', {})
        print(f"   Total Tests: {summary.get('total_tests', 0)}")
        print(f"   Passed: {summary.get('passed', 0)}")
        print(f"   Failed: {summary.get('failed', 0)}")
        print(f"   Pass Percentage: {summary.get('pass_percentage', 0)}%")
        print(f"   All Passed: {summary.get('all_passed', False)}")
        
        # Show error types if any
        test_results = response.get('test_results', [])
        error_types = {}
        for tr in test_results:
            status = tr.get('status', 'unknown')
            if status not in ['passed']:
                error_types[status] = error_types.get(status, 0) + 1
        
        if error_types:
            print(f"\n   Error Summary:")
            for error_type, count in error_types.items():
                print(f"   - {error_type}: {count}")
        
        return True
    return False

def test_submit_endpoint():
    """Test /submit endpoint with database save"""
    print("\n" + "="*60)
    print("📝 Test 3: /submit endpoint - Save to Database")
    print("="*60)
    
    python_code = """a = int(input())
b = int(input())
print(a + b)"""
    
    submit_test_cases = generate_test_cases(20, "submit_test")
    
    request_data = {
        "language": "python",
        "code": python_code,
        "test_cases": submit_test_cases,
        "sample_test_cases": [],
        "user_id": "test_user_submit_1",
        "question_id": "test_q_submit_1",
        "timeout": 5
    }
    
    print(f"Sending request with {len(submit_test_cases)} test cases...")
    response = make_request("/submit", request_data)
    
    if response:
        print("✅ Request successful!")
        summary = response.get('summary', {})
        metadata = response.get('metadata', {})
        
        print(f"   Total Tests: {summary.get('total_tests', 0)}")
        print(f"   Passed: {summary.get('passed', 0)}")
        print(f"   Failed: {summary.get('failed', 0)}")
        print(f"   Pass Percentage: {summary.get('pass_percentage', 0)}%")
        print(f"   Saved to DB: {metadata.get('saved_to_db', False)}")
        
        if metadata.get('submission_id'):
            print(f"   Submission ID: {metadata.get('submission_id')}")
        
        return True
    return False

def test_error_detection():
    """Test error detection (syntax error, TLE)"""
    print("\n" + "="*60)
    print("📝 Test 4: Error Detection - Syntax Error")
    print("="*60)
    
    syntax_error_code = """print(10  # syntax error"""
    
    request_data = {
        "language": "python",
        "code": syntax_error_code,
        "sample_test_cases": [
            {"id": "error_test_1", "input": "", "expected_output": "10"}
        ],
        "timeout": 5
    }
    
    print("Sending request with syntax error...")
    response = make_request("/run", request_data)
    
    if response:
        print("✅ Request successful!")
        test_results = response.get('test_results', [])
        if test_results:
            tr = test_results[0]
            status = tr.get('status', 'unknown')
            error = tr.get('error', '')
            
            print(f"   Status: {status}")
            if 'syntax' in status.lower() or 'syntax' in error.lower():
                print("   ✅ Syntax error detected correctly!")
            else:
                print(f"   ⚠️  Expected syntax_error, got: {status}")
                print(f"   Error: {error[:100]}")
        
        return True
    return False

def test_health():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("🏥 Health Check")
    print("="*60)
    
    try:
        url = f"{BASE_URL}/health"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            print("✅ Health check passed!")
            print(f"   Status: {data.get('status', 'unknown')}")
            print(f"   Version: {data.get('version', 'unknown')}")
            return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 FastAPI Endpoints Test Suite")
    print("="*60)
    print(f"Base URL: {BASE_URL}")
    
    # Check if service is running
    if not test_health():
        print("\n❌ Service is not running!")
        print("   Start the service with: uvicorn executor-service-fastapi:app --reload")
        sys.exit(1)
    
    # Run all tests
    results = []
    results.append(("Health Check", test_health()))
    results.append(("/run", test_run_endpoint()))
    results.append(("/runall", test_runall_endpoint()))
    results.append(("/submit", test_submit_endpoint()))
    results.append(("Error Detection", test_error_detection()))
    
    # Summary
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(result[1] for result in results)
    if all_passed:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed")
        sys.exit(1)

