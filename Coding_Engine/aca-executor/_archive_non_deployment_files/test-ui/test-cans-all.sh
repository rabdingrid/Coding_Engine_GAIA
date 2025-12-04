#!/bin/bash
# Quick test script for C++ cans problem

EXECUTOR_URL="https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io"

CODE='#include <bits/stdc++.h>
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
    cout << result << "\n";
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
}'

echo "🧪 Testing C++ Code - All Test Cases"
echo "===================================="
echo ""

test_case() {
    local test_num=$1
    local input=$2
    local expected=$3
    
    echo -n "Test $test_num: "
    
    result=$(curl -s -X POST "$EXECUTOR_URL/execute" \
      -H "Content-Type: application/json" \
      -d "{\"language\":\"cpp\",\"code\":\"$CODE\",\"test_cases\":[{\"input\":\"$input\",\"expected_output\":\"$expected\"}]}")
    
    if echo "$result" | python3 -c "import sys,json; d=json.load(sys.stdin); exit(0 if d.get('test_results',[{}])[0].get('passed') else 1)" 2>/dev/null; then
        output=$(echo "$result" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['test_results'][0].get('actual_output','').strip())" 2>/dev/null)
        time=$(echo "$result" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['metadata'].get('execution_time_ms',0))" 2>/dev/null)
        echo "✅ PASSED | Output: $output | Expected: $expected | Time: ${time}ms"
    else
        error=$(echo "$result" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('error','Unknown error')[:50])" 2>/dev/null || echo "Failed")
        echo "❌ FAILED | Error: $error"
    fi
}

# Test cases
test_case 1 "7\n6\n4\n9\n10\n34\n56\n54" "68"
test_case 2 "8\n132\n45\n65\n765\n345\n243\n75\n67" "1120"
test_case 3 "60\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12" "309"
test_case 4 "100\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9" "116"

echo ""
echo "✅ Testing complete!"

