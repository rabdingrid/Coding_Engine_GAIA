#!/bin/bash
# Store the two execution results you just got

API_BASE_URL="http://localhost:3001/api"

echo "📊 Storing Your Execution Results in Monitoring Dashboard..."
echo ""

# Store first execution
echo "1. Storing first execution (container: fshhk)..."
RESULT1='{"code":"public class Main { public static void main(String[] args) { java.util.Scanner s = new java.util.Scanner(System.in); int n = s.nextInt(); if (n <= 2) { System.out.println(n); return; } int a = 1, b = 2; for (int i = 3; i <= n; i++) { int t = a + b; a = b; b = t; } System.out.println(b); } }","execution_id":"f2db2ed4-a86a-4424-9e3e-e41e7eb25be6","language":"java","metadata":{"container_id":"ai-ta-ra-code-executor2--0000021-5554db4ff-fshhk","cpu_usage_percent":212.74,"execution_time_ms":3396,"memory_usage_bytes":41410560,"memory_usage_mb":39.49,"replica":"unknown","security":"enabled","timeout":5},"question_id":"15","submission_id":"bac5f1a9-8a69-4113-ba53-23c00dacc17f","summary":{"all_passed":true,"failed":0,"pass_percentage":100.0,"passed":5,"total_tests":5},"test_results":[{"actual_output":"2\n","cpu_usage_percent":194.3,"error":null,"execution_time_ms":65,"expected_output":"2","input":"2","memory_usage_bytes":40857600,"passed":true,"status":"passed","test_case_id":"test_1","test_case_number":1},{"actual_output":"3\n","cpu_usage_percent":194.1,"error":null,"execution_time_ms":67,"expected_output":"3","input":"3","memory_usage_bytes":40828928,"passed":true,"status":"passed","test_case_id":"test_2","test_case_number":2},{"actual_output":"5\n","cpu_usage_percent":192.5,"error":null,"execution_time_ms":68,"expected_output":"5","input":"4","memory_usage_bytes":41410560,"passed":true,"status":"passed","test_case_id":"test_3","test_case_number":3},{"actual_output":"8\n","cpu_usage_percent":288.6,"error":null,"execution_time_ms":81,"expected_output":"8","input":"5","memory_usage_bytes":40611840,"passed":true,"status":"passed","test_case_id":"test_4","test_case_number":4},{"actual_output":"1\n","cpu_usage_percent":194.2,"error":null,"execution_time_ms":96,"expected_output":"1","input":"1","memory_usage_bytes":40693760,"passed":true,"status":"passed","test_case_id":"test_5","test_case_number":5}],"timestamp":"2025-11-29T10:23:02.634288","user_id":"user_1_climbing_stairs"}'

echo "$RESULT1" | curl -s -X POST "${API_BASE_URL}/monitoring/store" \
  -H "Content-Type: application/json" \
  -d @- > /dev/null && echo "  ✅ Stored!" || echo "  ❌ Failed"

# Store second execution
echo ""
echo "2. Storing second execution (container: gf2zz)..."
RESULT2='{"code":"public class Main { public static void main(String[] args) { java.util.Scanner s = new java.util.Scanner(System.in); int n = s.nextInt(); if (n <= 2) { System.out.println(n); return; } int a = 1, b = 2; for (int i = 3; i <= n; i++) { int t = a + b; a = b; b = t; } System.out.println(b); } }","execution_id":"edd09bfd-cf5b-43de-bc6b-4c0562e8bb8b","language":"java","metadata":{"container_id":"ai-ta-ra-code-executor2--0000021-5554db4ff-gf2zz","cpu_usage_percent":211.74,"execution_time_ms":3269,"memory_usage_bytes":41480192,"memory_usage_mb":39.56,"replica":"unknown","security":"enabled","timeout":5},"question_id":"15","submission_id":"e6ba00eb-5607-4beb-b866-973a4da630ee","summary":{"all_passed":true,"failed":0,"pass_percentage":100.0,"passed":5,"total_tests":5},"test_results":[{"actual_output":"2\n","cpu_usage_percent":191.9,"error":null,"execution_time_ms":78,"expected_output":"2","input":"2","memory_usage_bytes":41480192,"passed":true,"status":"passed","test_case_id":"test_1","test_case_number":1},{"actual_output":"3\n","cpu_usage_percent":193.6,"error":null,"execution_time_ms":79,"expected_output":"3","input":"3","memory_usage_bytes":40755200,"passed":true,"status":"passed","test_case_id":"test_2","test_case_number":2},{"actual_output":"5\n","cpu_usage_percent":284.7,"error":null,"execution_time_ms":88,"expected_output":"5","input":"4","memory_usage_bytes":40792064,"passed":true,"status":"passed","test_case_id":"test_3","test_case_number":3},{"actual_output":"8\n","cpu_usage_percent":194.5,"error":null,"execution_time_ms":61,"expected_output":"8","input":"5","memory_usage_bytes":41172992,"passed":true,"status":"passed","test_case_id":"test_4","test_case_number":4},{"actual_output":"1\n","cpu_usage_percent":194.0,"error":null,"execution_time_ms":73,"expected_output":"1","input":"1","memory_usage_bytes":40730624,"passed":true,"status":"passed","test_case_id":"test_5","test_case_number":5}],"timestamp":"2025-11-29T10:23:16.820515","user_id":"user_1_climbing_stairs"}'

echo "$RESULT2" | curl -s -X POST "${API_BASE_URL}/monitoring/store" \
  -H "Content-Type: application/json" \
  -d @- > /dev/null && echo "  ✅ Stored!" || echo "  ❌ Failed"

echo ""
echo "✅ Both executions stored!"
echo ""
echo "💡 Open monitoring-dashboard.html and refresh to see both results"
echo "   (They should appear at the top, newest first)"


