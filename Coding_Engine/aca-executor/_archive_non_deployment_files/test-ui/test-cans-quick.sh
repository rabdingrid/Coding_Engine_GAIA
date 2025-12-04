#!/bin/bash
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

echo "🧪 Testing C++ Code with Test Cases..."
echo ""

# Test Case 1
echo "Test 1: Input: 7 cans"
curl -s -X POST "$EXECUTOR_URL/execute" \
  -H "Content-Type: application/json" \
  -d "{\"language\":\"cpp\",\"code\":\"$CODE\",\"test_cases\":[{\"input\":\"7\\n6\\n4\\n9\\n10\\n34\\n56\\n54\",\"expected_output\":\"68\"}]}" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"✅ Test 1: {d['test_results'][0]['passed']} | Output: {d['test_results'][0].get('actual_output','N/A')[:20]} | Time: {d['metadata']['execution_time_ms']}ms\")" 2>/dev/null

# Test Case 2
echo "Test 2: Input: 8 cans"
curl -s -X POST "$EXECUTOR_URL/execute" \
  -H "Content-Type: application/json" \
  -d "{\"language\":\"cpp\",\"code\":\"$CODE\",\"test_cases\":[{\"input\":\"8\\n132\\n45\\n65\\n765\\n345\\n243\\n75\\n67\",\"expected_output\":\"1120\"}]}" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"✅ Test 2: {d['test_results'][0]['passed']} | Output: {d['test_results'][0].get('actual_output','N/A')[:20]} | Time: {d['metadata']['execution_time_ms']}ms\")" 2>/dev/null

echo ""
echo "✅ Quick tests complete!"
