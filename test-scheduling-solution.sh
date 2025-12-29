#!/bin/bash

SERVICE_URL="https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io"

echo "=========================================="
echo "🧪 Testing Scheduling Problem Solution"
echo "=========================================="
echo ""

# Test Case 0: Example from problem
echo "📤 Test Case 0: n=5, capacity=[2,1,5,3,1], requests=17"
echo "   Expected: 9"
echo ""

RESPONSE=$(curl -s -X POST "$SERVICE_URL/runall" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "cpp",
    "code": "#include <bits/stdc++.h>\nusing namespace std;\n\nstring ltrim(const string &);\nstring rtrim(const string &);\n\nint calculateSchedulingTime(vector<int>& capacity, long long requests) {\n    priority_queue<int> pq;\n    for (int cap : capacity) {\n        pq.push(cap);\n    }\n    long long remaining = requests;\n    int time = 0;\n    while (remaining > 0) {\n        if (pq.empty()) break;\n        int max_capacity = pq.top();\n        pq.pop();\n        long long handled = min((long long)max_capacity, remaining);\n        remaining -= handled;\n        time++;\n        int new_capacity = max_capacity / 2;\n        if (new_capacity > 0) {\n            pq.push(new_capacity);\n        }\n    }\n    return time;\n}\n\nint main() {\n    string capacity_count_temp;\n    getline(cin, capacity_count_temp);\n    int capacity_count = stoi(ltrim(rtrim(capacity_count_temp)));\n    vector<int> capacity(capacity_count);\n    for (int i = 0; i < capacity_count; i++) {\n        string capacity_item_temp;\n        getline(cin, capacity_item_temp);\n        int capacity_item = stoi(ltrim(rtrim(capacity_item_temp)));\n        capacity[i] = capacity_item;\n    }\n    string requests_temp;\n    getline(cin, requests_temp);\n    long long requests = stoll(ltrim(rtrim(requests_temp)));\n    int result = calculateSchedulingTime(capacity, requests);\n    cout << result << \"\\n\";\n    return 0;\n}\n\nstring ltrim(const string &str) {\n    string s(str);\n    s.erase(s.begin(), find_if(s.begin(), s.end(), not1(ptr_fun<int, int>(isspace))));\n    return s;\n}\n\nstring rtrim(const string &str) {\n    string s(str);\n    s.erase(find_if(s.rbegin(), s.rend(), not1(ptr_fun<int, int>(isspace))).base(), s.end());\n    return s;\n}",
    "test_cases": [
      {
        "id": "test_0",
        "input": "5\n2\n1\n5\n3\n1\n17",
        "expected_output": "9"
      },
      {
        "id": "test_1",
        "input": "4\n3\n1\n4\n2\n3",
        "expected_output": "1"
      },
      {
        "id": "test_2",
        "input": "10\n7\n10\n9\n10\n6\n3\n9\n9\n10\n10\n122",
        "expected_output": "20"
      }
    ],
    "sample_test_cases": []
  }')

echo "$RESPONSE" | python3 -m json.tool 2>/dev/null | head -80


