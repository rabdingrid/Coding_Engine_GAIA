#!/bin/bash

SERVICE_URL="https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io"

echo "=========================================="
echo "🧪 Testing Deployed C++ Batch Optimization"
echo "=========================================="
echo ""

# Test with 17 test cases
echo "📤 Testing with 17 C++ test cases..."
echo "   URL: $SERVICE_URL/runall"
echo ""

START_TIME=$(date +%s.%N)

RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}\nTIME_TOTAL:%{time_total}" \
  -X POST "$SERVICE_URL/runall" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "cpp",
    "code": "#include <bits/stdc++.h>\nusing namespace std;\n\nstring ltrim(const string &);\nstring rtrim(const string &);\n\nvector<int> countBetween(vector<int> arr, vector<int> low, vector<int> high) {\n    int n = arr.size();\n    int q = low.size();\n    vector<int> result(q);\n    sort(arr.begin(), arr.end());\n    for (int i = 0; i < q; i++) {\n        int left = lower_bound(arr.begin(), arr.end(), low[i]) - arr.begin();\n        int right = upper_bound(arr.begin(), arr.end(), high[i]) - arr.begin();\n        result[i] = right - left;\n    }\n    return result;\n}\n\nint main()\n{\n    string n_temp;\n    getline(cin, n_temp);\n    int n = stoi(ltrim(rtrim(n_temp)));\n    vector<int> arr(n);\n    for (int i = 0; i < n; i++) {\n        string arr_item_temp;\n        getline(cin, arr_item_temp);\n        int arr_item = stoi(ltrim(rtrim(arr_item_temp)));\n        arr[i] = arr_item;\n    }\n    string q_temp;\n    getline(cin, q_temp);\n    int q = stoi(ltrim(rtrim(q_temp)));\n    vector<int> low(q);\n    for (int i = 0; i < q; i++) {\n        string low_item_temp;\n        getline(cin, low_item_temp);\n        int low_item = stoi(ltrim(rtrim(low_item_temp)));\n        low[i] = low_item;\n    }\n    string q_temp2;\n    getline(cin, q_temp2);\n    int q2 = stoi(ltrim(rtrim(q_temp2)));\n    vector<int> high(q2);\n    for (int i = 0; i < q2; i++) {\n        string high_item_temp;\n        getline(cin, high_item_temp);\n        int high_item = stoi(ltrim(rtrim(high_item_temp)));\n        high[i] = high_item;\n    }\n    vector<int> result = countBetween(arr, low, high);\n    for (size_t i = 0; i < result.size(); i++) {\n        cout << result[i];\n        if (i != result.size() - 1) {\n            cout << \"\\n\";\n        }\n    }\n    cout << \"\\n\";\n    return 0;\n}\n\nstring ltrim(const string &str) {\n    string s(str);\n    s.erase(\n        s.begin(),\n        find_if(s.begin(), s.end(), not1(ptr_fun<int, int>(isspace)))\n    );\n    return s;\n}\n\nstring rtrim(const string &str) {\n    string s(str);\n    s.erase(\n        find_if(s.rbegin(), s.rend(), not1(ptr_fun<int, int>(isspace))).base(),\n        s.end()\n    );\n    return s;\n}",
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
  }')

END_TIME=$(date +%s.%N)
ELAPSED=$(echo "$END_TIME - $START_TIME" | bc)

HTTP_CODE=$(echo "$RESPONSE" | grep "HTTP_CODE:" | cut -d: -f2)
TIME_TOTAL=$(echo "$RESPONSE" | grep "TIME_TOTAL:" | cut -d: -f2)
BODY=$(echo "$RESPONSE" | sed '/HTTP_CODE:/d' | sed '/TIME_TOTAL:/d')

echo "📥 Response received"
echo "   HTTP Code: $HTTP_CODE"
echo "   Total Time: ${TIME_TOTAL}s"
echo ""

if [ "$HTTP_CODE" = "200" ]; then
    echo "$BODY" | python3 -m json.tool > /tmp/deployed_test_response.json 2>/dev/null
    
    if [ -f /tmp/deployed_test_response.json ]; then
        TOTAL_TESTS=$(python3 -c "import json; d=json.load(open('/tmp/deployed_test_response.json')); print(d.get('summary', {}).get('total_tests', 0))" 2>/dev/null)
        PASSED=$(python3 -c "import json; d=json.load(open('/tmp/deployed_test_response.json')); print(d.get('summary', {}).get('passed', 0))" 2>/dev/null)
        EXEC_TIME=$(python3 -c "import json; d=json.load(open('/tmp/deployed_test_response.json')); print(d.get('metadata', {}).get('execution_time_ms', 0))" 2>/dev/null)
        
        echo "✅ Test Results:"
        echo "   Total Tests: $TOTAL_TESTS"
        echo "   Passed: $PASSED"
        echo "   Server Execution Time: ${EXEC_TIME}ms"
        echo ""
        
        # Performance check
        TIME_FLOAT=$(echo "$TIME_TOTAL" | awk '{print $1}')
        if (( $(echo "$TIME_FLOAT < 10" | bc -l) )); then
            echo "🎉 SUCCESS! Total time: ${TIME_TOTAL}s (Target: <10s)"
            echo ""
            echo "📊 Performance Comparison:"
            echo "   Before optimization: ~24s"
            echo "   After optimization: ${TIME_TOTAL}s"
            echo "   Improvement: $(echo "scale=1; (24 - $TIME_FLOAT) / 24 * 100" | bc)% faster ✅"
        else
            echo "⚠️  Total time: ${TIME_TOTAL}s (Target: <10s)"
        fi
    else
        echo "Response preview:"
        echo "$BODY" | head -10
    fi
else
    echo "❌ Request failed"
    echo "$BODY" | head -20
fi

echo ""
echo "=========================================="


