#!/usr/bin/env python3
"""
Load Test: 500 Dummy Users with Detailed Metrics
Each user submits 1 DSA question with 20 test cases (including 3 long test cases)
Different languages distributed across users
Outputs detailed table with all metrics
"""

import subprocess
import json
import time
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import tempfile
import os
import csv

API_URL = "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io"

# DSA Question: Sum of Array Elements
# 20 test cases: 3 long ones + 17 regular ones
DSA_QUESTION = {
    "python": {
        "code": """n = int(input())
arr = list(map(int, input().split()))
result = sum(arr)
print(result)""",
        "test_cases": [
            {"id": "tc_1", "input": "5\n1 2 3 4 5", "expected_output": "15\n"},
            {"id": "tc_2", "input": "10\n1 1 1 1 1 1 1 1 1 1", "expected_output": "10\n"},
            {"id": "tc_3", "input": "3\n100 200 300", "expected_output": "600\n"},
            {"id": "tc_4", "input": "1\n42", "expected_output": "42\n"},
            {"id": "tc_5", "input": "7\n-1 2 -3 4 -5 6 -7", "expected_output": "-4\n"},
            {"id": "tc_6", "input": "4\n0 0 0 0", "expected_output": "0\n"},
            {"id": "tc_7", "input": "6\n1 10 100 1000 10000 100000", "expected_output": "111111\n"},
            {"id": "tc_8", "input": "8\n5 10 15 20 25 30 35 40", "expected_output": "180\n"},
            {"id": "tc_9", "input": "2\n999 1", "expected_output": "1000\n"},
            {"id": "tc_10", "input": "9\n1 2 3 4 5 6 7 8 9", "expected_output": "45\n"},
            {"id": "tc_11", "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12", "expected_output": "78\n"},
            {"id": "tc_12", "input": "15\n1 1 1 1 1 1 1 1 1 1 1 1 1 1 1", "expected_output": "15\n"},
            {"id": "tc_13", "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20", "expected_output": "210\n"},
            {"id": "tc_14", "input": "25\n" + " ".join(["1"] * 25), "expected_output": "25\n"},
            {"id": "tc_15", "input": "30\n" + " ".join([str(i) for i in range(1, 31)]), "expected_output": "465\n"},
            # Long test cases (3)
            {"id": "tc_16", "input": "100\n" + " ".join([str(i) for i in range(1, 101)]), "expected_output": "5050\n"},
            {"id": "tc_17", "input": "200\n" + " ".join([str(i) for i in range(1, 201)]), "expected_output": "20100\n"},
            {"id": "tc_18", "input": "500\n" + " ".join([str(i) for i in range(1, 501)]), "expected_output": "125250\n"},
            {"id": "tc_19", "input": "50\n" + " ".join([str(i*10) for i in range(1, 51)]), "expected_output": "12750\n"},
            {"id": "tc_20", "input": "75\n" + " ".join([str(i*2) for i in range(1, 76)]), "expected_output": "5700\n"}
        ]
    },
    "cpp": {
        "code": """#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }
    long long sum = 0;
    for (int i = 0; i < n; i++) {
        sum += arr[i];
    }
    cout << sum << endl;
    return 0;
}""",
        "test_cases": [
            {"id": "tc_1", "input": "5\n1 2 3 4 5", "expected_output": "15\n"},
            {"id": "tc_2", "input": "10\n1 1 1 1 1 1 1 1 1 1", "expected_output": "10\n"},
            {"id": "tc_3", "input": "3\n100 200 300", "expected_output": "600\n"},
            {"id": "tc_4", "input": "1\n42", "expected_output": "42\n"},
            {"id": "tc_5", "input": "7\n-1 2 -3 4 -5 6 -7", "expected_output": "-4\n"},
            {"id": "tc_6", "input": "4\n0 0 0 0", "expected_output": "0\n"},
            {"id": "tc_7", "input": "6\n1 10 100 1000 10000 100000", "expected_output": "111111\n"},
            {"id": "tc_8", "input": "8\n5 10 15 20 25 30 35 40", "expected_output": "180\n"},
            {"id": "tc_9", "input": "2\n999 1", "expected_output": "1000\n"},
            {"id": "tc_10", "input": "9\n1 2 3 4 5 6 7 8 9", "expected_output": "45\n"},
            {"id": "tc_11", "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12", "expected_output": "78\n"},
            {"id": "tc_12", "input": "15\n1 1 1 1 1 1 1 1 1 1 1 1 1 1 1", "expected_output": "15\n"},
            {"id": "tc_13", "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20", "expected_output": "210\n"},
            {"id": "tc_14", "input": "25\n" + " ".join(["1"] * 25), "expected_output": "25\n"},
            {"id": "tc_15", "input": "30\n" + " ".join([str(i) for i in range(1, 31)]), "expected_output": "465\n"},
            # Long test cases (3)
            {"id": "tc_16", "input": "100\n" + " ".join([str(i) for i in range(1, 101)]), "expected_output": "5050\n"},
            {"id": "tc_17", "input": "200\n" + " ".join([str(i) for i in range(1, 201)]), "expected_output": "20100\n"},
            {"id": "tc_18", "input": "500\n" + " ".join([str(i) for i in range(1, 501)]), "expected_output": "125250\n"},
            {"id": "tc_19", "input": "50\n" + " ".join([str(i*10) for i in range(1, 51)]), "expected_output": "12750\n"},
            {"id": "tc_20", "input": "75\n" + " ".join([str(i*2) for i in range(1, 76)]), "expected_output": "5700\n"}
        ]
    },
    "java": {
        "code": """import java.util.*;
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        long sum = 0;
        for (int i = 0; i < n; i++) {
            sum += sc.nextInt();
        }
        System.out.println(sum);
    }
}""",
        "test_cases": [
            {"id": "tc_1", "input": "5\n1 2 3 4 5", "expected_output": "15\n"},
            {"id": "tc_2", "input": "10\n1 1 1 1 1 1 1 1 1 1", "expected_output": "10\n"},
            {"id": "tc_3", "input": "3\n100 200 300", "expected_output": "600\n"},
            {"id": "tc_4", "input": "1\n42", "expected_output": "42\n"},
            {"id": "tc_5", "input": "7\n-1 2 -3 4 -5 6 -7", "expected_output": "-4\n"},
            {"id": "tc_6", "input": "4\n0 0 0 0", "expected_output": "0\n"},
            {"id": "tc_7", "input": "6\n1 10 100 1000 10000 100000", "expected_output": "111111\n"},
            {"id": "tc_8", "input": "8\n5 10 15 20 25 30 35 40", "expected_output": "180\n"},
            {"id": "tc_9", "input": "2\n999 1", "expected_output": "1000\n"},
            {"id": "tc_10", "input": "9\n1 2 3 4 5 6 7 8 9", "expected_output": "45\n"},
            {"id": "tc_11", "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12", "expected_output": "78\n"},
            {"id": "tc_12", "input": "15\n1 1 1 1 1 1 1 1 1 1 1 1 1 1 1", "expected_output": "15\n"},
            {"id": "tc_13", "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20", "expected_output": "210\n"},
            {"id": "tc_14", "input": "25\n" + " ".join(["1"] * 25), "expected_output": "25\n"},
            {"id": "tc_15", "input": "30\n" + " ".join([str(i) for i in range(1, 31)]), "expected_output": "465\n"},
            # Long test cases (3)
            {"id": "tc_16", "input": "100\n" + " ".join([str(i) for i in range(1, 101)]), "expected_output": "5050\n"},
            {"id": "tc_17", "input": "200\n" + " ".join([str(i) for i in range(1, 201)]), "expected_output": "20100\n"},
            {"id": "tc_18", "input": "500\n" + " ".join([str(i) for i in range(1, 501)]), "expected_output": "125250\n"},
            {"id": "tc_19", "input": "50\n" + " ".join([str(i*10) for i in range(1, 51)]), "expected_output": "12750\n"},
            {"id": "tc_20", "input": "75\n" + " ".join([str(i*2) for i in range(1, 76)]), "expected_output": "5700\n"}
        ]
    },
    "javascript": {
        "code": """const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});
let lines = [];
rl.on('line', (line) => {
    lines.push(line);
});
rl.on('close', () => {
    const n = parseInt(lines[0]);
    const arr = lines[1].split(' ').map(Number);
    const sum = arr.reduce((a, b) => a + b, 0);
    console.log(sum);
    process.exit(0);
});""",
        "test_cases": [
            {"id": "tc_1", "input": "5\n1 2 3 4 5", "expected_output": "15\n"},
            {"id": "tc_2", "input": "10\n1 1 1 1 1 1 1 1 1 1", "expected_output": "10\n"},
            {"id": "tc_3", "input": "3\n100 200 300", "expected_output": "600\n"},
            {"id": "tc_4", "input": "1\n42", "expected_output": "42\n"},
            {"id": "tc_5", "input": "7\n-1 2 -3 4 -5 6 -7", "expected_output": "-4\n"},
            {"id": "tc_6", "input": "4\n0 0 0 0", "expected_output": "0\n"},
            {"id": "tc_7", "input": "6\n1 10 100 1000 10000 100000", "expected_output": "111111\n"},
            {"id": "tc_8", "input": "8\n5 10 15 20 25 30 35 40", "expected_output": "180\n"},
            {"id": "tc_9", "input": "2\n999 1", "expected_output": "1000\n"},
            {"id": "tc_10", "input": "9\n1 2 3 4 5 6 7 8 9", "expected_output": "45\n"},
            {"id": "tc_11", "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12", "expected_output": "78\n"},
            {"id": "tc_12", "input": "15\n1 1 1 1 1 1 1 1 1 1 1 1 1 1 1", "expected_output": "15\n"},
            {"id": "tc_13", "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20", "expected_output": "210\n"},
            {"id": "tc_14", "input": "25\n" + " ".join(["1"] * 25), "expected_output": "25\n"},
            {"id": "tc_15", "input": "30\n" + " ".join([str(i) for i in range(1, 31)]), "expected_output": "465\n"},
            # Long test cases (3)
            {"id": "tc_16", "input": "100\n" + " ".join([str(i) for i in range(1, 101)]), "expected_output": "5050\n"},
            {"id": "tc_17", "input": "200\n" + " ".join([str(i) for i in range(1, 201)]), "expected_output": "20100\n"},
            {"id": "tc_18", "input": "500\n" + " ".join([str(i) for i in range(1, 501)]), "expected_output": "125250\n"},
            {"id": "tc_19", "input": "50\n" + " ".join([str(i*10) for i in range(1, 51)]), "expected_output": "12750\n"},
            {"id": "tc_20", "input": "75\n" + " ".join([str(i*2) for i in range(1, 76)]), "expected_output": "5700\n"}
        ]
    },
    "csharp": {
        "code": """using System;
class Program {
    static void Main() {
        int n = int.Parse(Console.ReadLine());
        string[] arr = Console.ReadLine().Split();
        long sum = 0;
        for (int i = 0; i < n; i++) {
            sum += long.Parse(arr[i]);
        }
        Console.WriteLine(sum);
    }
}""",
        "test_cases": [
            {"id": "tc_1", "input": "5\n1 2 3 4 5", "expected_output": "15\n"},
            {"id": "tc_2", "input": "10\n1 1 1 1 1 1 1 1 1 1", "expected_output": "10\n"},
            {"id": "tc_3", "input": "3\n100 200 300", "expected_output": "600\n"},
            {"id": "tc_4", "input": "1\n42", "expected_output": "42\n"},
            {"id": "tc_5", "input": "7\n-1 2 -3 4 -5 6 -7", "expected_output": "-4\n"},
            {"id": "tc_6", "input": "4\n0 0 0 0", "expected_output": "0\n"},
            {"id": "tc_7", "input": "6\n1 10 100 1000 10000 100000", "expected_output": "111111\n"},
            {"id": "tc_8", "input": "8\n5 10 15 20 25 30 35 40", "expected_output": "180\n"},
            {"id": "tc_9", "input": "2\n999 1", "expected_output": "1000\n"},
            {"id": "tc_10", "input": "9\n1 2 3 4 5 6 7 8 9", "expected_output": "45\n"},
            {"id": "tc_11", "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12", "expected_output": "78\n"},
            {"id": "tc_12", "input": "15\n1 1 1 1 1 1 1 1 1 1 1 1 1 1 1", "expected_output": "15\n"},
            {"id": "tc_13", "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20", "expected_output": "210\n"},
            {"id": "tc_14", "input": "25\n" + " ".join(["1"] * 25), "expected_output": "25\n"},
            {"id": "tc_15", "input": "30\n" + " ".join([str(i) for i in range(1, 31)]), "expected_output": "465\n"},
            # Long test cases (3)
            {"id": "tc_16", "input": "100\n" + " ".join([str(i) for i in range(1, 101)]), "expected_output": "5050\n"},
            {"id": "tc_17", "input": "200\n" + " ".join([str(i) for i in range(1, 201)]), "expected_output": "20100\n"},
            {"id": "tc_18", "input": "500\n" + " ".join([str(i) for i in range(1, 501)]), "expected_output": "125250\n"},
            {"id": "tc_19", "input": "50\n" + " ".join([str(i*10) for i in range(1, 51)]), "expected_output": "12750\n"},
            {"id": "tc_20", "input": "75\n" + " ".join([str(i*2) for i in range(1, 76)]), "expected_output": "5700\n"}
        ]
    }
}

LANGUAGES = ["python", "cpp", "java", "javascript", "csharp"]

def submit_request(user_id, language, question_data):
    """Submit a request for a single user"""
    start_time = time.time()
    start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    
    payload = {
        "language": language,
        "code": question_data["code"],
        "test_cases": question_data["test_cases"],
        "user_id": f"user_{user_id}",
        "question_id": f"sum_array_{language}",
        "timeout": 10
    }
    
    # Write payload to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(payload, f)
        temp_file = f.name
    
    try:
        # Execute curl command
        curl_cmd = [
            'curl', '-s', '-w', '\nHTTP_CODE:%{http_code}\nTIME_TOTAL:%{time_total}',
            '-X', 'POST',
            '-H', 'Content-Type: application/json',
            '-d', f'@{temp_file}',
            '--max-time', '180',  # 3 minute timeout
            API_URL + '/runall'
        ]
        
        result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=185)
        
        end_time = time.time()
        end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        wait_time_ms = int((end_time - start_time) * 1000)
        
        # Parse response
        output = result.stdout
        http_code = None
        time_total = None
        body = output
        
        for line in output.split('\n'):
            if line.startswith('HTTP_CODE:'):
                http_code = line.split(':', 1)[1].strip()
            elif line.startswith('TIME_TOTAL:'):
                time_total = float(line.split(':', 1)[1].strip())
        
        # Remove curl metadata lines from body
        body_lines = [l for l in output.split('\n') if not l.startswith('HTTP_CODE:') and not l.startswith('TIME_TOTAL:')]
        body = '\n'.join(body_lines)
        
        # Parse JSON response
        container_id = "unknown"
        replica = "unknown"
        exec_time = 0
        all_passed = False
        passed_count = 0
        total_count = 0
        cpu_usage = 0.0
        memory_usage = 0
        
        if http_code == "200" and body:
            try:
                response_data = json.loads(body)
                metadata = response_data.get('metadata', {})
                container_id = metadata.get('container_id', 'unknown')
                replica = metadata.get('replica', 'unknown')
                exec_time = metadata.get('test_execution_time_ms', metadata.get('execution_time_ms', 0))
                summary = response_data.get('summary', {})
                all_passed = summary.get('all_passed', False)
                passed_count = summary.get('passed', 0)
                total_count = summary.get('total', len(question_data["test_cases"]))
                
                # Get CPU and memory from first test result (if available)
                test_results = response_data.get('test_results', [])
                if test_results:
                    first_result = test_results[0]
                    cpu_usage = first_result.get('cpu_usage_percent', 0.0)
                    memory_usage = first_result.get('memory_usage_bytes', 0)
            except Exception as e:
                pass
        
        return {
            "user_id": f"user_{user_id}",
            "language": language,
            "http_code": http_code or "error",
            "wait_time_ms": wait_time_ms,
            "exec_time_ms": exec_time,
            "container_id": container_id,
            "replica": replica,
            "all_passed": all_passed,
            "passed_count": passed_count,
            "total_count": total_count,
            "cpu_usage_percent": cpu_usage,
            "memory_usage_bytes": memory_usage,
            "time_total": time_total or 0,
            "success": http_code == "200",
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp,
            "duration_ms": wait_time_ms
        }
    except subprocess.TimeoutExpired:
        end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        return {
            "user_id": f"user_{user_id}",
            "language": language,
            "http_code": "timeout",
            "wait_time_ms": int((time.time() - start_time) * 1000),
            "exec_time_ms": 0,
            "container_id": "unknown",
            "replica": "unknown",
            "all_passed": False,
            "passed_count": 0,
            "total_count": len(question_data["test_cases"]),
            "cpu_usage_percent": 0.0,
            "memory_usage_bytes": 0,
            "time_total": 0,
            "success": False,
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp,
            "duration_ms": int((time.time() - start_time) * 1000)
        }
    except Exception as e:
        end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        return {
            "user_id": f"user_{user_id}",
            "language": language,
            "http_code": "error",
            "wait_time_ms": int((time.time() - start_time) * 1000),
            "exec_time_ms": 0,
            "container_id": "unknown",
            "replica": "unknown",
            "all_passed": False,
            "passed_count": 0,
            "total_count": len(question_data["test_cases"]),
            "cpu_usage_percent": 0.0,
            "memory_usage_bytes": 0,
            "time_total": 0,
            "success": False,
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp,
            "duration_ms": int((time.time() - start_time) * 1000),
            "error": str(e)
        }
    finally:
        try:
            os.unlink(temp_file)
        except:
            pass

def main():
    num_users = 500
    
    print("=" * 120)
    print("🚀 LOAD TEST: 500 Dummy Users with Detailed Metrics")
    print("=" * 120)
    print(f"API URL: {API_URL}")
    print(f"Total Users: {num_users}")
    print(f"Languages: {', '.join(LANGUAGES)}")
    print(f"Question: Sum of Array Elements (DSA)")
    print(f"Test Cases: 20 per user (including 3 long test cases)")
    print(f"Test Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 120)
    print()
    
    overall_start = time.time()
    overall_start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    
    print("⚡ Starting parallel execution of 500 users...")
    print("   Distributing across all 5 languages...")
    print("   Each user: 1 DSA question with 20 test cases (3 long ones)")
    print()
    
    results = []
    completed = 0
    
    # Distribute users across languages
    user_assignments = []
    for i in range(num_users):
        language = LANGUAGES[i % len(LANGUAGES)]
        user_assignments.append((i+1, language, DSA_QUESTION[language]))
    
    # Submit requests with slight staggering to avoid overwhelming
    with ThreadPoolExecutor(max_workers=500) as executor:
        futures = {}
        for idx, (user_id, language, question_data) in enumerate(user_assignments):
            # Stagger by 10ms per request
            if idx > 0:
                time.sleep(0.01)
            future = executor.submit(submit_request, user_id, language, question_data)
            futures[future] = user_id
        
        for future in as_completed(futures):
            completed += 1
            result = future.result()
            results.append(result)
            
            status_icon = "✅" if result['success'] else "❌"
            if completed % 50 == 0 or not result['success']:
                print(f"   [{completed:3d}/500] {status_icon} {result['user_id']:10s} - {result['language']:10s} - {result['http_code']:3s} - {result['wait_time_ms']:6d}ms - TC: {result['passed_count']}/{result['total_count']}")
    
    overall_time = time.time() - overall_start
    overall_end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    overall_time_ms = int(overall_time * 1000)
    
    print()
    print("✅ All requests completed!")
    print()
    
    # Sort results by user_id for consistent output
    results.sort(key=lambda x: int(x['user_id'].split('_')[1]))
    
    # Write detailed CSV file
    output_file = "LOAD_TEST_500_USERS_DETAILED_RESULTS.csv"
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = [
            'User_ID', 'Language', 'HTTP_Code', 'Success',
            'Start_Timestamp', 'End_Timestamp', 'Duration_ms', 'Execution_Time_ms',
            'Container_ID', 'Replica_ID', 'CPU_Usage_%', 'Memory_Usage_Bytes',
            'Test_Cases_Passed', 'Test_Cases_Total', 'All_Passed'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for r in results:
            writer.writerow({
                'User_ID': r['user_id'],
                'Language': r['language'],
                'HTTP_Code': r['http_code'],
                'Success': 'Yes' if r['success'] else 'No',
                'Start_Timestamp': r['start_timestamp'],
                'End_Timestamp': r['end_timestamp'],
                'Duration_ms': r['duration_ms'],
                'Execution_Time_ms': r['exec_time_ms'],
                'Container_ID': r['container_id'],
                'Replica_ID': r['replica'],
                'CPU_Usage_%': f"{r['cpu_usage_percent']:.2f}",
                'Memory_Usage_Bytes': r['memory_usage_bytes'],
                'Test_Cases_Passed': r['passed_count'],
                'Test_Cases_Total': r['total_count'],
                'All_Passed': 'Yes' if r['all_passed'] else 'No'
            })
    
    print("=" * 120)
    print("📊 RESULTS SUMMARY")
    print("=" * 120)
    print()
    
    total = len(results)
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"📈 Overall Statistics:")
    print(f"   Test Start: {overall_start_timestamp}")
    print(f"   Test End:   {overall_end_timestamp}")
    print(f"   Total Duration: {overall_time_ms}ms ({overall_time:.2f}s)")
    print(f"   Total Requests: {total}")
    print(f"   ✅ Successful: {len(successful)}")
    print(f"   ❌ Failed: {len(failed)}")
    if total > 0:
        success_rate = (len(successful) / total) * 100
        print(f"   Success Rate: {success_rate:.1f}%")
    print()
    
    if successful:
        wait_times = [r['wait_time_ms'] for r in successful]
        exec_times = [r['exec_time_ms'] for r in successful]
        
        print(f"⏱️  Performance Metrics (Successful Requests):")
        print(f"   Wait Time - Min: {min(wait_times)}ms, Max: {max(wait_times)}ms, Avg: {int(sum(wait_times) / len(wait_times))}ms")
        print(f"   Execution Time - Min: {min(exec_times)}ms, Max: {max(exec_times)}ms, Avg: {int(sum(exec_times) / len(exec_times))}ms")
        print()
        
        # Language distribution
        languages = {}
        for r in successful:
            lang = r['language']
            languages[lang] = languages.get(lang, 0) + 1
        
        print("📝 Language Distribution (Successful):")
        for lang in LANGUAGES:
            count = languages.get(lang, 0)
            total_for_lang = sum(1 for r in results if r['language'] == lang)
            success_rate_lang = (count / total_for_lang * 100) if total_for_lang > 0 else 0
            print(f"   {lang:12s}: {count:3d}/{total_for_lang:3d} ({success_rate_lang:.1f}%)")
        print()
        
        # Replica distribution
        replicas = {}
        for r in successful:
            replica = r['replica']
            replicas[replica] = replicas.get(replica, 0) + 1
        
        print("🔄 Replica Distribution:")
        for replica, count in sorted(replicas.items(), key=lambda x: x[1], reverse=True):
            print(f"   {replica}: {count} requests")
        print()
        
        # Test results
        all_passed_count = sum(1 for r in successful if r['all_passed'])
        avg_passed = sum(r['passed_count'] for r in successful) / len(successful) if successful else 0
        print(f"✅ All Tests Passed: {all_passed_count}/{len(successful)}")
        print(f"📊 Average Test Cases Passed: {avg_passed:.1f}/20")
        print()
    
    print("=" * 120)
    print("✅ Load test complete!")
    print("=" * 120)
    print()
    print(f"📄 Detailed results saved to: {output_file}")
    print(f"   Contains: User ID, Language, Timestamps, Duration, Replica ID, CPU, Memory, Test Cases")
    print()

if __name__ == "__main__":
    main()

