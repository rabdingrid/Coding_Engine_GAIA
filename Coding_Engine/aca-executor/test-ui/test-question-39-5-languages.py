#!/usr/bin/env python3
"""
Test Question 39: Warehouse Box Removal
5 Users in PARALLEL - Each using different language (C++, Java, Python, JavaScript, C#)
"""

import subprocess
import json
import time
from datetime import datetime
import tempfile
import os
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

API_URL = "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io"

# Question 39: Warehouse Box Removal
# Test cases from the problem
QUESTION_39 = {
    "cpp": {
        "code": """#include <bits/stdc++.h>
using namespace std;

string ltrim(const string &);
string rtrim(const string &);

int findTotalWeight(vector<int> cans) {
    int total = 0;
    while (!cans.empty()) {
        int minVal = INT_MAX;
        int idx = -1;
        // find earliest minimum
        for (int i = 0; i < cans.size(); i++) {
            if (cans[i] < minVal) {
                minVal = cans[i];
                idx = i;
            }
        }
        total += minVal;
        // remove neighbors
        int start = max(0, idx - 1);
        int end = min((int)cans.size() - 1, idx + 1);
        // remove backwards to avoid shifting issues
        for (int i = end; i >= start; i--) {
            cans.erase(cans.begin() + i);
        }
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
}""",
        "test_cases": [
            {"id": "sample_1", "input": "7\n6\n4\n9\n10\n34\n56\n54", "expected_output": "68\n"},
            {"id": "sample_2", "input": "8\n132\n45\n65\n765\n345\n243\n75\n67", "expected_output": "1120\n"},
            {"id": "test_1", "input": "5\n5\n4\n1\n3\n2", "expected_output": "3\n"}
        ]
    },
    "java": {
        "code": """import java.util.*;

public class Main {
    public static int findTotalWeight(ArrayList<Integer> cans) {
        int total = 0;
        while (!cans.isEmpty()) {
            int minVal = Integer.MAX_VALUE;
            int idx = -1;
            // find earliest minimum
            for (int i = 0; i < cans.size(); i++) {
                if (cans.get(i) < minVal) {
                    minVal = cans.get(i);
                    idx = i;
                }
            }
            total += minVal;
            // remove neighbors
            int start = Math.max(0, idx - 1);
            int end = Math.min(cans.size() - 1, idx + 1);
            // remove backwards to avoid shifting issues
            for (int i = end; i >= start; i--) {
                cans.remove(i);
            }
        }
        return total;
    }
    
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int cans_count = sc.nextInt();
        ArrayList<Integer> cans = new ArrayList<>();
        for (int i = 0; i < cans_count; i++) {
            cans.add(sc.nextInt());
        }
        int result = findTotalWeight(cans);
        System.out.println(result);
    }
}""",
        "test_cases": [
            {"id": "sample_1", "input": "7\n6\n4\n9\n10\n34\n56\n54", "expected_output": "68\n"},
            {"id": "sample_2", "input": "8\n132\n45\n65\n765\n345\n243\n75\n67", "expected_output": "1120\n"},
            {"id": "test_1", "input": "5\n5\n4\n1\n3\n2", "expected_output": "3\n"}
        ]
    },
    "python": {
        "code": """def find_total_weight(cans):
    total = 0
    cans = cans[:]  # make a copy
    while cans:
        min_val = min(cans)
        idx = cans.index(min_val)  # finds earliest minimum
        total += min_val
        # remove neighbors
        start = max(0, idx - 1)
        end = min(len(cans) - 1, idx + 1)
        # remove backwards to avoid shifting issues
        for i in range(end, start - 1, -1):
            cans.pop(i)
    return total

n = int(input())
cans = []
for _ in range(n):
    cans.append(int(input()))
result = find_total_weight(cans)
print(result)""",
        "test_cases": [
            {"id": "sample_1", "input": "7\n6\n4\n9\n10\n34\n56\n54", "expected_output": "68\n"},
            {"id": "sample_2", "input": "8\n132\n45\n65\n765\n345\n243\n75\n67", "expected_output": "1120\n"},
            {"id": "test_1", "input": "5\n5\n4\n1\n3\n2", "expected_output": "3\n"}
        ]
    },
    "javascript": {
        "code": """const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

function findTotalWeight(cans) {
    let total = 0;
    cans = [...cans];  // make a copy
    while (cans.length > 0) {
        let minVal = Math.min(...cans);
        let idx = cans.indexOf(minVal);  // finds earliest minimum
        total += minVal;
        // remove neighbors
        let start = Math.max(0, idx - 1);
        let end = Math.min(cans.length - 1, idx + 1);
        // remove backwards to avoid shifting issues
        for (let i = end; i >= start; i--) {
            cans.splice(i, 1);
        }
    }
    return total;
}

let lines = [];
rl.on('line', (line) => {
    lines.push(line);
});

rl.on('close', () => {
    const n = parseInt(lines[0]);
    const cans = [];
    for (let i = 1; i <= n; i++) {
        cans.push(parseInt(lines[i]));
    }
    const result = findTotalWeight(cans);
    console.log(result);
    process.exit(0);
});""",
        "test_cases": [
            {"id": "sample_1", "input": "7\n6\n4\n9\n10\n34\n56\n54", "expected_output": "68\n"},
            {"id": "sample_2", "input": "8\n132\n45\n65\n765\n345\n243\n75\n67", "expected_output": "1120\n"},
            {"id": "test_1", "input": "5\n5\n4\n1\n3\n2", "expected_output": "3\n"}
        ]
    },
    "csharp": {
        "code": """using System;
using System.Collections.Generic;
using System.Linq;

class Program {
    static int FindTotalWeight(List<int> cans) {
        int total = 0;
        cans = new List<int>(cans);  // make a copy
        while (cans.Count > 0) {
            int minVal = cans.Min();
            int idx = cans.IndexOf(minVal);  // finds earliest minimum
            total += minVal;
            // remove neighbors
            int start = Math.Max(0, idx - 1);
            int end = Math.Min(cans.Count - 1, idx + 1);
            // remove backwards to avoid shifting issues
            for (int i = end; i >= start; i--) {
                cans.RemoveAt(i);
            }
        }
        return total;
    }
    
    static void Main() {
        int n = int.Parse(Console.ReadLine());
        List<int> cans = new List<int>();
        for (int i = 0; i < n; i++) {
            cans.Add(int.Parse(Console.ReadLine()));
        }
        int result = FindTotalWeight(cans);
        Console.WriteLine(result);
    }
}""",
        "test_cases": [
            {"id": "sample_1", "input": "7\n6\n4\n9\n10\n34\n56\n54", "expected_output": "68\n"},
            {"id": "sample_2", "input": "8\n132\n45\n65\n765\n345\n243\n75\n67", "expected_output": "1120\n"},
            {"id": "test_1", "input": "5\n5\n4\n1\n3\n2", "expected_output": "3\n"}
        ]
    }
}

LANGUAGES = ["cpp", "java", "python", "javascript", "csharp"]

def test_user(user_id, language):
    """Test a single user with specific language"""
    start_time = time.time()
    start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    
    payload = {
        "language": language,
        "code": QUESTION_39[language]["code"],
        "test_cases": QUESTION_39[language]["test_cases"]
    }
    
    # Write to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(payload, f)
        temp_file = f.name
    
    try:
        # Simple curl request
        curl_cmd = [
            'curl', '-s', '-w', '\nHTTP_CODE:%{http_code}\nTIME_TOTAL:%{time_total}',
            '-X', 'POST',
            '-H', 'Content-Type: application/json',
            '-d', f'@{temp_file}',
            '--max-time', '60',
            API_URL + '/runall'
        ]
        
        result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=65)
        
        end_time = time.time()
        end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        duration_ms = int((end_time - start_time) * 1000)
        
        # Parse HTTP code and time
        http_code = "unknown"
        time_total = 0.0
        for line in result.stdout.split('\n'):
            if line.startswith('HTTP_CODE:'):
                http_code = line.split(':', 1)[1].strip()
            elif line.startswith('TIME_TOTAL:'):
                time_total = float(line.split(':', 1)[1].strip())
        
        # Parse JSON response
        body = '\n'.join([l for l in result.stdout.split('\n') if not l.startswith('HTTP_CODE:') and not l.startswith('TIME_TOTAL:')])
        success = False
        passed = 0
        total = 0
        all_passed = False
        container_id = "unknown"
        replica_id = "unknown"
        execution_time_ms = 0
        cpu_usage = 0.0
        memory_usage = 0
        test_results_detail = []
        
        if http_code == "200" and body:
            try:
                data = json.loads(body)
                metadata = data.get('metadata', {})
                container_id = metadata.get('container_id', 'unknown')
                replica_id = metadata.get('replica', 'unknown')
                execution_time_ms = metadata.get('execution_time_ms', metadata.get('test_execution_time_ms', 0))
                cpu_usage = metadata.get('cpu_usage_percent', 0.0)
                memory_usage = metadata.get('memory_usage_bytes', 0)
                
                summary = data.get('summary', {})
                passed = summary.get('passed', 0)
                total = summary.get('total', len(QUESTION_39[language]["test_cases"]))
                all_passed = summary.get('all_passed', False)
                
                # Get detailed test results
                test_results_detail = data.get('test_results', [])
                
                success = True
            except Exception as e:
                pass
        
        return {
            'user_id': f"user_{user_id}",
            'language': language,
            'start_timestamp': start_timestamp,
            'end_timestamp': end_timestamp,
            'duration_ms': duration_ms,
            'http_code': http_code,
            'success': success,
            'container_id': container_id,
            'replica_id': replica_id,
            'execution_time_ms': execution_time_ms,
            'cpu_usage_percent': cpu_usage,
            'memory_usage_bytes': memory_usage,
            'test_cases_passed': passed,
            'test_cases_total': total,
            'all_passed': all_passed,
            'time_total': time_total,
            'test_results': test_results_detail
        }
    except subprocess.TimeoutExpired:
        end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        return {
            'user_id': f"user_{user_id}",
            'language': language,
            'start_timestamp': start_timestamp,
            'end_timestamp': end_timestamp,
            'duration_ms': int((time.time() - start_time) * 1000),
            'http_code': 'timeout',
            'success': False,
            'container_id': 'unknown',
            'replica_id': 'unknown',
            'execution_time_ms': 0,
            'cpu_usage_percent': 0.0,
            'memory_usage_bytes': 0,
            'test_cases_passed': 0,
            'test_cases_total': len(QUESTION_39[language]["test_cases"]),
            'all_passed': False,
            'time_total': 0.0,
            'test_results': []
        }
    except Exception as e:
        end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        return {
            'user_id': f"user_{user_id}",
            'language': language,
            'start_timestamp': start_timestamp,
            'end_timestamp': end_timestamp,
            'duration_ms': int((time.time() - start_time) * 1000),
            'http_code': 'error',
            'success': False,
            'container_id': 'unknown',
            'replica_id': 'unknown',
            'execution_time_ms': 0,
            'cpu_usage_percent': 0.0,
            'memory_usage_bytes': 0,
            'test_cases_passed': 0,
            'test_cases_total': len(QUESTION_39[language]["test_cases"]),
            'all_passed': False,
            'time_total': 0.0,
            'test_results': [],
            'error': str(e)
        }
    finally:
        try:
            os.unlink(temp_file)
        except:
            pass

def main():
    print("=" * 100)
    print("🧪 QUESTION 39 TEST: Warehouse Box Removal")
    print("=" * 100)
    print(f"API: {API_URL}")
    print(f"Endpoint: /runall")
    print(f"Test Cases: 3 per user (2 samples + 1 basic)")
    print(f"Users: 5 (one per language)")
    print(f"Languages: {', '.join(LANGUAGES)}")
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 100)
    print()
    
    overall_start = time.time()
    overall_start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    
    # Test 5 users in PARALLEL (one per language)
    print("📤 Sending 5 requests in PARALLEL (one per language)...")
    print()
    
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(test_user, i+1, LANGUAGES[i]): i+1 
            for i in range(5)
        }
        
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            status = "✅" if result['success'] else "❌"
            print(f"{status} {result['user_id']:10s} - {result['language']:10s} - {result['http_code']:3s} - {result['duration_ms']:5d}ms - TC: {result['test_cases_passed']}/{result['test_cases_total']} - All Passed: {result['all_passed']}")
    
    overall_time = time.time() - overall_start
    overall_end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    
    # Sort by language for consistent output
    results.sort(key=lambda x: LANGUAGES.index(x['language']))
    
    # Write detailed CSV
    csv_filename = "QUESTION_39_5_LANGUAGES_RESULTS.csv"
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = [
            'User_ID', 'Language', 'HTTP_Code', 'Success',
            'Start_Timestamp', 'End_Timestamp', 'Duration_ms', 'Execution_Time_ms',
            'Container_ID', 'Replica_ID', 'CPU_Usage_%', 'Memory_Usage_Bytes',
            'Test_Cases_Passed', 'Test_Cases_Total', 'All_Passed', 'Time_Total'
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
                'Execution_Time_ms': r['execution_time_ms'],
                'Container_ID': r['container_id'],
                'Replica_ID': r['replica_id'],
                'CPU_Usage_%': f"{r['cpu_usage_percent']:.2f}",
                'Memory_Usage_Bytes': r['memory_usage_bytes'],
                'Test_Cases_Passed': r['test_cases_passed'],
                'Test_Cases_Total': r['test_cases_total'],
                'All_Passed': 'Yes' if r['all_passed'] else 'No',
                'Time_Total': f"{r['time_total']:.3f}"
            })
    
    # Summary
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print()
    print("=" * 100)
    print("📊 RESULTS SUMMARY")
    print("=" * 100)
    print()
    print(f"Test Start: {overall_start_timestamp}")
    print(f"Test End:   {overall_end_timestamp}")
    print(f"Total Duration: {int(overall_time * 1000)}ms ({overall_time:.2f}s)")
    print()
    print(f"✅ Successful: {len(successful)}/5")
    print(f"❌ Failed: {len(failed)}/5")
    print()
    
    if successful:
        durations = [r['duration_ms'] for r in successful]
        exec_times = [r['execution_time_ms'] for r in successful if r['execution_time_ms'] > 0]
        
        print(f"⏱️  Performance Metrics (Successful):")
        print(f"   Duration - Min: {min(durations)}ms, Max: {max(durations)}ms, Avg: {int(sum(durations) / len(durations))}ms")
        if exec_times:
            print(f"   Execution - Min: {min(exec_times)}ms, Max: {max(exec_times)}ms, Avg: {int(sum(exec_times) / len(exec_times))}ms")
        print()
        
        # Language breakdown
        print("📝 Language Results:")
        for r in results:
            status = "✅" if r['success'] else "❌"
            all_passed = "✅" if r['all_passed'] else "❌"
            print(f"   {status} {r['language']:10s}: {r['test_cases_passed']}/{r['test_cases_total']} tests passed, All Passed: {all_passed}, Duration: {r['duration_ms']}ms")
        print()
        
        # Container distribution
        containers = {}
        replicas = {}
        for r in successful:
            cid = r['container_id']
            rid = r['replica_id']
            containers[cid] = containers.get(cid, 0) + 1
            replicas[rid] = replicas.get(rid, 0) + 1
        
        if containers:
            print("🔄 Container Distribution:")
            for cid, count in sorted(containers.items(), key=lambda x: x[1], reverse=True):
                print(f"   {cid[:50]}: {count} requests")
            print()
        
        if replicas:
            print("🔄 Replica Distribution:")
            for rid, count in sorted(replicas.items(), key=lambda x: x[1], reverse=True):
                print(f"   {rid}: {count} requests")
            print()
    
    print(f"📄 Detailed CSV saved to: {csv_filename}")
    print("=" * 100)
    print()

if __name__ == "__main__":
    main()
