#!/usr/bin/env python3
"""Test C++ cans problem with all test cases"""

import json
import urllib.request
import urllib.parse
import time

EXECUTOR_URL = "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io"

CODE = """#include <bits/stdc++.h>
using namespace std;
string ltrim(const string &);
string rtrim(const string &);
int findTotalWeight(vector<int> cans) {
    int total = 0;
    while (!cans.empty()) {
        int minWeight = cans[0];
        int minIndex = 0;
        for (int i = 1; i < cans.size(); i++) {
            if (cans[i] < minWeight) {
                minWeight = cans[i];
                minIndex = i;
            }
        }
        total += minWeight;
        int startIdx = max(0, minIndex - 1);
        int endIdx = min((int)cans.size() - 1, minIndex + 1);
        cans.erase(cans.begin() + startIdx, cans.begin() + endIdx + 1);
    }
    return total;
}
int main() {
    string cans_count_temp;
    getline(cin, cans_count_temp);
    int cans_count = stoi(ltrim(rtrim(cans_count_temp)));
    vector<int> cans(cans_count);
    for (int i = 0; i < cans_count; i++) {
        string cans_item_temp;
        getline(cin, cans_item_temp);
        int cans_item = stoi(ltrim(rtrim(cans_item_temp)));
        cans[i] = cans_item;
    }
    int result = findTotalWeight(cans);
    cout << result << "\\n";
    return 0;
}
string ltrim(const string &str) {
    string s(str);
    s.erase(s.begin(), find_if(s.begin(), s.end(), not1(ptr_fun<int, int>(isspace))));
    return s;
}
string rtrim(const string &str) {
    string s(str);
    s.erase(find_if(s.rbegin(), s.rend(), not1(ptr_fun<int, int>(isspace))).base(), s.end());
    return s;
}"""

TEST_CASES = [
    ("7\n6\n4\n9\n10\n34\n56\n54", "68"),
    ("8\n132\n45\n65\n765\n345\n243\n75\n67", "1120"),
    ("60\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12", "309"),
    ("100\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9", "116"),
]

def test_case(test_num, input_data, expected):
    payload = {
        "language": "cpp",
        "code": CODE,
        "test_cases": [{"input": input_data, "expected_output": expected}]
    }
    
    start = time.time()
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(f"{EXECUTOR_URL}/execute", data=data, headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode())
            elapsed = (time.time() - start) * 1000
            
            passed = result.get('test_results', [{}])[0].get('passed', False)
            actual = result.get('test_results', [{}])[0].get('actual_output', '').strip()
            exec_time = result.get('metadata', {}).get('execution_time_ms', 0)
            container = result.get('metadata', {}).get('container_id', 'unknown')[:30]
            
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"Test {test_num}: {status} | Output: {actual} | Expected: {expected} | Exec: {exec_time}ms | Total: {elapsed:.0f}ms | Container: {container}")
            return passed
    except Exception as e:
        print(f"Test {test_num}: ❌ ERROR - {str(e)[:60]}")
        return False

print("🧪 Testing C++ Cans Problem - All Test Cases")
print("=" * 80)
print("")

passed = 0
for i, (input_data, expected) in enumerate(TEST_CASES, 1):
    if test_case(i, input_data, expected):
        passed += 1
    time.sleep(0.5)  # Small delay between tests

print("")
print("=" * 80)
print(f"📊 Results: {passed}/{len(TEST_CASES)} tests passed")
print("=" * 80)

