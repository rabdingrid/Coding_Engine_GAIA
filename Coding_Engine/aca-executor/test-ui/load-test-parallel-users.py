#!/usr/bin/env python3
"""
Load Test: Parallel Users with Question 39 (Warehouse Box Removal)
Simulates multiple users submitting the same question in different languages
Tests queue system, wait times, and parallel execution capacity
"""

import time
import json
from datetime import datetime
from typing import List, Dict, Any
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request
import urllib.parse
import urllib.error

# Configuration
API_URL = "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io"
QUESTIONS_API_URL = "http://localhost:3002"  # Local questions API
QUESTION_NUMBER = 39  # Warehouse Box Removal

# Test cases for Warehouse Box Removal (sample)
TEST_CASES = [
    {
        "id": "test_1",
        "input": "7\n6\n4\n9\n10\n34\n56\n54",
        "expected_output": "68\n"
    },
    {
        "id": "test_2",
        "input": "8\n132\n45\n65\n765\n345\n243\n75\n67",
        "expected_output": "1120\n"
    }
]

# Code solutions in different languages
CODE_SOLUTIONS = {
    "cpp": """#include <bits/stdc++.h>
using namespace std;

string ltrim(const string &);
string rtrim(const string &);

int findTotalWeight(vector<int> cans) {
    int total = 0;
    while (!cans.empty()) {
        int minVal = INT_MAX;
        int idx = -1;
        for (int i = 0; i < cans.size(); i++) {
            if (cans[i] < minVal) {
                minVal = cans[i];
                idx = i;
            }
        }
        total += minVal;
        int start = max(0, idx - 1);
        int end = min((int)cans.size() - 1, idx + 1);
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
    
    "java": """import java.util.*;

public class Main {
    public static int findTotalWeight(List<Integer> cans) {
        int total = 0;
        while (!cans.isEmpty()) {
            int minVal = Integer.MAX_VALUE;
            int idx = -1;
            for (int i = 0; i < cans.size(); i++) {
                if (cans.get(i) < minVal) {
                    minVal = cans.get(i);
                    idx = i;
                }
            }
            total += minVal;
            int start = Math.max(0, idx - 1);
            int end = Math.min(cans.size() - 1, idx + 1);
            for (int i = end; i >= start; i--) {
                cans.remove(i);
            }
        }
        return total;
    }
    
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int cansCount = Integer.parseInt(sc.nextLine().trim());
        List<Integer> cans = new ArrayList<>();
        for (int i = 0; i < cansCount; i++) {
            cans.add(Integer.parseInt(sc.nextLine().trim()));
        }
        int result = findTotalWeight(cans);
        System.out.println(result);
    }
}""",
    
    "javascript": """const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

let input = [];
rl.on('line', (line) => {
    input.push(line);
});

rl.on('close', () => {
    const cansCount = parseInt(input[0]);
    const cans = [];
    for (let i = 1; i <= cansCount; i++) {
        cans.push(parseInt(input[i]));
    }
    
    function findTotalWeight(cans) {
        let total = 0;
        while (cans.length > 0) {
            let minVal = Infinity;
            let idx = -1;
            for (let i = 0; i < cans.length; i++) {
                if (cans[i] < minVal) {
                    minVal = cans[i];
                    idx = i;
                }
            }
            total += minVal;
            const start = Math.max(0, idx - 1);
            const end = Math.min(cans.length - 1, idx + 1);
            cans.splice(start, end - start + 1);
        }
        return total;
    }
    
    const result = findTotalWeight(cans);
    console.log(result);
    process.exit(0);
});""",
    
    "csharp": """using System;
using System.Collections.Generic;
using System.Linq;

class Program {
    static int FindTotalWeight(List<int> cans) {
        int total = 0;
        while (cans.Count > 0) {
            int minVal = int.MaxValue;
            int idx = -1;
            for (int i = 0; i < cans.Count; i++) {
                if (cans[i] < minVal) {
                    minVal = cans[i];
                    idx = i;
                }
            }
            total += minVal;
            int start = Math.Max(0, idx - 1);
            int end = Math.Min(cans.Count - 1, idx + 1);
            cans.RemoveRange(start, end - start + 1);
        }
        return total;
    }
    
    static void Main() {
        int cansCount = int.Parse(Console.ReadLine().Trim());
        List<int> cans = new List<int>();
        for (int i = 0; i < cansCount; i++) {
            cans.Add(int.Parse(Console.ReadLine().Trim()));
        }
        int result = FindTotalWeight(cans);
        Console.WriteLine(result);
    }
}""",
    
    "python": """def find_total_weight(cans):
    total = 0
    cans = cans.copy()
    while cans:
        min_val = min(cans)
        idx = cans.index(min_val)
        total += min_val
        start = max(0, idx - 1)
        end = min(len(cans) - 1, idx + 1)
        del cans[start:end+1]
    return total

def main():
    cans_count = int(input().strip())
    cans = []
    for _ in range(cans_count):
        cans.append(int(input().strip()))
    result = find_total_weight(cans)
    print(result)

if __name__ == "__main__":
    main()"""
}

def fetch_question(question_id: str) -> Dict[str, Any]:
    """Fetch question from questions API"""
    try:
        req = urllib.request.Request(f"{QUESTIONS_API_URL}/api/questions/{question_id}")
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                return json.loads(response.read().decode())
            else:
                print(f"⚠️  Failed to fetch question {question_id}: {response.status}")
                return None
    except Exception as e:
        print(f"⚠️  Error fetching question: {e}")
        return None

def submit_code(user_id: str, language: str, code: str, 
               test_cases: List[Dict], question_id: str) -> Dict[str, Any]:
    """Submit code for a single user"""
    start_time = time.time()
    
    payload = {
        "language": language,
        "code": code,
        "test_cases": test_cases,
        "user_id": user_id,
        "question_id": question_id,
        "timeout": 5
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            f"{API_URL}/runall",
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            wait_time = (time.time() - start_time) * 1000  # Wait time in ms
            
            if response.status == 200:
                result = json.loads(response.read().decode())
                execution_time = result.get('metadata', {}).get('execution_time_ms', 0)
                container_id = result.get('metadata', {}).get('container_id', 'unknown')
                replica = result.get('metadata', {}).get('replica', 'unknown')
                summary = result.get('summary', {})
                
                return {
                    "user_id": user_id,
                    "language": language,
                    "status": "success",
                    "wait_time_ms": wait_time,
                    "execution_time_ms": execution_time,
                    "container_id": container_id,
                    "replica": replica,
                    "summary": summary,
                    "all_passed": summary.get('all_passed', False),
                    "error": None
                }
            else:
                error_text = response.read().decode()[:200]
                return {
                    "user_id": user_id,
                    "language": language,
                    "status": "error",
                    "wait_time_ms": wait_time,
                    "execution_time_ms": 0,
                    "container_id": "unknown",
                    "replica": "unknown",
                    "summary": {},
                    "all_passed": False,
                    "error": f"HTTP {response.status}: {error_text}"
                }
    except urllib.error.URLError as e:
        if 'timed out' in str(e).lower():
            return {
                "user_id": user_id,
                "language": language,
                "status": "timeout",
                "wait_time_ms": (time.time() - start_time) * 1000,
                "execution_time_ms": 0,
                "container_id": "unknown",
                "replica": "unknown",
                "summary": {},
                "all_passed": False,
                "error": "Request timeout (>60s)"
            }
        else:
            return {
                "user_id": user_id,
                "language": language,
                "status": "error",
                "wait_time_ms": (time.time() - start_time) * 1000,
                "execution_time_ms": 0,
                "container_id": "unknown",
                "replica": "unknown",
                "summary": {},
                "all_passed": False,
                "error": str(e)
            }
    except Exception as e:
        return {
            "user_id": user_id,
            "language": language,
            "status": "error",
            "wait_time_ms": (time.time() - start_time) * 1000,
            "execution_time_ms": 0,
            "container_id": "unknown",
            "replica": "unknown",
            "summary": {},
            "all_passed": False,
            "error": str(e)
        }

def run_load_test(num_users: int = 10):
    """Run load test with multiple parallel users"""
    print("=" * 80)
    print("🚀 PARALLEL USER LOAD TEST")
    print("=" * 80)
    print(f"Question: #{QUESTION_NUMBER} (Warehouse Box Removal)")
    print(f"Users: {num_users}")
    print(f"Languages: {', '.join(CODE_SOLUTIONS.keys())}")
    print(f"API URL: {API_URL}")
    print("=" * 80)
    print()
    
    # Fetch question to get actual test cases
    print(f"📋 Fetching question {QUESTION_NUMBER}...")
    question = fetch_question(str(QUESTION_NUMBER))
    
    if not question:
        # Try fetching all questions and find question 39 by title
        print("⚠️  Could not fetch by ID, trying to find by title...")
        try:
            req = urllib.request.Request(f"{QUESTIONS_API_URL}/api/questions")
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    all_questions = json.loads(response.read().decode())
                    # Find question with "Warehouse" in title
                    question = next((q for q in all_questions if 'warehouse' in q.get('title', '').lower() or 'box' in q.get('title', '').lower()), None)
                    if question:
                        print(f"✅ Found question by title: {question.get('title', 'Unknown')}")
        except Exception as e:
            print(f"⚠️  Error fetching questions: {e}")
    
    if not question:
        print("⚠️  Could not fetch question from API. Using default test cases.")
        test_cases = TEST_CASES
        question_id = "warehouse_box_removal"  # Use a default ID
    else:
        question_id = question.get('id', "warehouse_box_removal")
        # Use actual test cases from question, or fallback to default
        test_cases = question.get('test_cases', TEST_CASES)
        # Filter out file path test cases
        test_cases = [tc for tc in test_cases if tc.get('input') and not tc.get('input', '').startswith('/')]
        if not test_cases:
            test_cases = TEST_CASES
        print(f"✅ Found question: {question.get('title', 'Unknown')}")
        print(f"   Question ID: {question_id}")
        print(f"   Test cases: {len(test_cases)}")
    
    # Prepare user requests
    languages = list(CODE_SOLUTIONS.keys())
    users = []
    
    for i in range(num_users):
        user_id = f"user_{i+1}"
        language = languages[i % len(languages)]  # Rotate through languages
        code = CODE_SOLUTIONS[language]
        users.append({
            "user_id": user_id,
            "language": language,
            "code": code,
            "test_cases": test_cases,
            "question_id": question_id
        })
    
    print(f"\n📊 Test Configuration:")
    print(f"   Total users: {num_users}")
    print(f"   Languages distribution:")
    for lang in languages:
        count = sum(1 for u in users if u['language'] == lang)
        print(f"     - {lang}: {count} users")
    print()
    
    # Execute all requests in parallel using ThreadPoolExecutor
    print("⚡ Starting parallel execution...")
    print(f"   All {num_users} users submitting simultaneously...")
    print()
    
    overall_start = time.time()
    
    with ThreadPoolExecutor(max_workers=num_users) as executor:
        futures = {
            executor.submit(submit_code, u['user_id'], u['language'], u['code'], u['test_cases'], u['question_id']): u
            for u in users
        }
        
        results = []
        completed = 0
        for future in as_completed(futures):
            completed += 1
            result = future.result()
            results.append(result)
            if completed % 5 == 0:
                print(f"   Progress: {completed}/{num_users} requests completed...")
    
    overall_time = (time.time() - overall_start) * 1000
    
    # Analyze results
    print("=" * 80)
    print("📊 RESULTS ANALYSIS")
    print("=" * 80)
    print()
    
    successful = [r for r in results if r['status'] == 'success']
    failed = [r for r in results if r['status'] != 'success']
    
    print(f"✅ Successful: {len(successful)}/{num_users}")
    print(f"❌ Failed: {len(failed)}/{num_users}")
    print()
    
    if successful:
        wait_times = [r['wait_time_ms'] for r in successful]
        execution_times = [r['execution_time_ms'] for r in successful]
        
        print("⏱️  Wait Times (Time until response received):")
        print(f"   Min: {min(wait_times):.0f}ms")
        print(f"   Max: {max(wait_times):.0f}ms")
        print(f"   Avg: {sum(wait_times)/len(wait_times):.0f}ms")
        print(f"   Target: < 5000ms ✅" if max(wait_times) < 5000 else f"   Target: < 5000ms ❌")
        print()
        
        print("⚡ Execution Times (Code execution duration):")
        print(f"   Min: {min(execution_times):.0f}ms")
        print(f"   Max: {max(execution_times):.0f}ms")
        print(f"   Avg: {sum(execution_times)/len(execution_times):.0f}ms")
        print()
        
        # Container/replica distribution
        containers = {}
        replicas = {}
        for r in successful:
            container = r['container_id']
            replica = r['replica']
            containers[container] = containers.get(container, 0) + 1
            replicas[replica] = replicas.get(replica, 0) + 1
        
        print("🔄 Container Distribution:")
        for container, count in sorted(containers.items(), key=lambda x: x[1], reverse=True):
            print(f"   {container}: {count} requests")
        print()
        
        print("🔄 Replica Distribution:")
        for replica, count in sorted(replicas.items(), key=lambda x: x[1], reverse=True):
            print(f"   {replica}: {count} requests")
        print()
        
        # Parallel execution analysis
        print("📈 Parallel Execution Analysis:")
        print(f"   Total time for {num_users} requests: {overall_time:.0f}ms")
        print(f"   If sequential: {sum(execution_times):.0f}ms")
        print(f"   Parallel efficiency: {sum(execution_times)/overall_time*100:.1f}%")
        print(f"   Requests processed in parallel: {num_users}")
        print()
        
        # Test results
        all_passed = [r for r in successful if r['all_passed']]
        print(f"✅ All tests passed: {len(all_passed)}/{len(successful)}")
        print()
    
    if failed:
        print("❌ Failed Requests:")
        for r in failed:
            print(f"   {r['user_id']} ({r['language']}): {r.get('error', 'Unknown error')}")
        print()
    
    # Detailed results table
    print("=" * 80)
    print("📋 DETAILED RESULTS")
    print("=" * 80)
    print(f"{'User':<10} {'Language':<10} {'Status':<10} {'Wait(ms)':<10} {'Exec(ms)':<10} {'Container':<20} {'All Pass':<10}")
    print("-" * 80)
    for r in results:
        status_icon = "✅" if r['status'] == 'success' else "❌"
        pass_icon = "✅" if r.get('all_passed') else "❌"
        print(f"{r['user_id']:<10} {r['language']:<10} {status_icon:<10} {r['wait_time_ms']:<10.0f} {r['execution_time_ms']:<10.0f} {r['container_id'][:20]:<20} {pass_icon:<10}")
    
    print()
    print("=" * 80)
    print("✅ Load test complete!")
    print("=" * 80)

if __name__ == "__main__":
    num_users = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    run_load_test(num_users)

