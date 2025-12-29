#!/usr/bin/env python3
"""
Load Testing Script: Multiple Dummy Users with Real DSA Questions
Purpose: Test executor performance, replica scaling, and queue handling
Shows: Container usage, CPU, memory, execution time per user
"""

import json
import time
import concurrent.futures
import sys
import subprocess
from datetime import datetime
from collections import defaultdict
import argparse
import urllib.request
import urllib.parse
import urllib.error

# Configuration
TEST_UI_URL = "http://localhost:3001"  # Test UI server
EXECUTOR_URL = None  # Will be fetched dynamically
NUM_USERS = 30  # Default number of concurrent users
MAX_WORKERS = 30  # Thread pool size

# Sample code solutions for different question types
SOLUTIONS = {
    "python": {
        "two_sum": """def twoSum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

# Read input
line = input().strip()
if line.startswith('['):
    # JSON array format
    import json
    nums = json.loads(line)
    target = int(input().strip())
else:
    # Space-separated format
    parts = line.split()
    nums = [int(x) for x in parts[:-1]]
    target = int(parts[-1])

result = twoSum(nums, target)
print(result)""",
        
        "climbing_stairs": """def climbStairs(n):
    if n <= 2:
        return n
    a, b = 1, 2
    for i in range(3, n + 1):
        a, b = b, a + b
    return b

n = int(input().strip())
print(climbStairs(n))""",
        
        "max_subarray": """def maxSubArray(nums):
    max_sum = nums[0]
    current_sum = nums[0]
    for i in range(1, len(nums)):
        current_sum = max(nums[i], current_sum + nums[i])
        max_sum = max(max_sum, current_sum)
    return max_sum

# Read input
line = input().strip()
if line.startswith('['):
    import json
    nums = json.loads(line)
else:
    nums = [int(x) for x in line.split()]

print(maxSubArray(nums))""",
        
        "longest_substring": """def lengthOfLongestSubstring(s):
    if not s:
        return 0
    char_map = {}
    max_len = 0
    start = 0
    for end in range(len(s)):
        if s[end] in char_map and char_map[s[end]] >= start:
            start = char_map[s[end]] + 1
        char_map[s[end]] = end
        max_len = max(max_len, end - start + 1)
    return max_len

try:
    s = input().strip()
except EOFError:
    s = ""
print(lengthOfLongestSubstring(s))""",
        
        "default": """# Simple computation
n = int(input().strip())
result = sum(range(1, n + 1))
print(result)"""
    },
    
    "java": {
        "climbing_stairs": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner s = new Scanner(System.in);
        int n = s.nextInt();
        if (n <= 2) {
            System.out.println(n);
            return;
        }
        int a = 1, b = 2;
        for (int i = 3; i <= n; i++) {
            int t = a + b;
            a = b;
            b = t;
        }
        System.out.println(b);
    }
}""",
        
        "default": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner s = new Scanner(System.in);
        int n = s.nextInt();
        int sum = 0;
        for (int i = 1; i <= n; i++) {
            sum += i;
        }
        System.out.println(sum);
    }
}"""
    },
    
    "javascript": {
        "max_subarray": """const readline = require('readline');
const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

rl.on('line', (line) => {
  let nums;
  try {
    nums = JSON.parse(line.trim());
  } catch (e) {
    nums = line.trim().split(' ').map(Number);
  }
  
  let maxSum = nums[0];
  let currentSum = nums[0];
  for (let i = 1; i < nums.length; i++) {
    currentSum = Math.max(nums[i], currentSum + nums[i]);
    maxSum = Math.max(maxSum, currentSum);
  }
  console.log(maxSum);
  rl.close();
});""",
        
        "default": """const readline = require('readline');
const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

rl.on('line', (line) => {
  const n = parseInt(line.trim());
  let sum = 0;
  for (let i = 1; i <= n; i++) {
    sum += i;
  }
  console.log(sum);
  rl.close();
});"""
    },
    
    "cpp": {
        "two_sum": """#include <bits/stdc++.h>
using namespace std;

int main() {
    vector<int> nums;
    int num;
    while (cin >> num) {
        nums.push_back(num);
    }
    int target = nums.back();
    nums.pop_back();
    
    map<int, int> seen;
    for (int i = 0; i < nums.size(); i++) {
        int complement = target - nums[i];
        if (seen.find(complement) != seen.end()) {
            cout << "[" << seen[complement] << "," << i << "]" << endl;
            return 0;
        }
        seen[nums[i]] = i;
    }
    cout << "[]" << endl;
    return 0;
}""",
        
        "default": """#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int sum = 0;
    for (int i = 1; i <= n; i++) {
        sum += i;
    }
    cout << sum << endl;
    return 0;
}"""
    }
}

def get_executor_url():
    """Get the executor URL from Azure Container App"""
    try:
        result = subprocess.run(
            ['az', 'containerapp', 'show', 
             '--name', 'ai-ta-ra-code-executor2',
             '--resource-group', 'ai-ta-2',
             '--query', 'properties.latestRevisionFqdn',
             '-o', 'tsv'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            url = result.stdout.strip()
            if not url.startswith('http'):
                url = f"https://{url}"
            return url
    except Exception as e:
        print(f"⚠️  Could not fetch executor URL from Azure: {e}")
    
    # Fallback to default
    return "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io"

def get_replica_count():
    """Get current replica count"""
    try:
        result = subprocess.run(
            ['az', 'containerapp', 'show',
             '--name', 'ai-ta-ra-code-executor2',
             '--resource-group', 'ai-ta-2',
             '--query', 'properties.template.scale.minReplicas',
             '-o', 'tsv'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    return "unknown"

def fetch_questions():
    """Fetch questions from the test UI API"""
    try:
        req = urllib.request.Request(f"{TEST_UI_URL}/api/questions")
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            if data.get('success') and data.get('questions'):
                return data['questions']
    except Exception as e:
        print(f"⚠️  Could not fetch questions from {TEST_UI_URL}: {e}")
        print("   Using default questions...")
    
    # Return default questions if API fails
    return [
        {"id": "1", "title": "Two Sum", "difficulty": "Easy"},
        {"id": "2", "title": "Maximum Subarray", "difficulty": "Medium"},
        {"id": "15", "title": "Climbing Stairs", "difficulty": "Easy"},
    ]

def get_question_details(question_id):
    """Get detailed question with test cases"""
    try:
        req = urllib.request.Request(f"{TEST_UI_URL}/api/questions/{question_id}")
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            if data.get('success'):
                return data
    except:
        pass
    return None

def get_code_for_question(question, language="python"):
    """Get appropriate code solution for a question"""
    title_lower = question.get('title', '').lower()
    
    # Map question titles to solution keys
    if 'two sum' in title_lower or 'sum' in title_lower:
        key = "two_sum"
    elif 'climbing' in title_lower or 'stairs' in title_lower:
        key = "climbing_stairs"
    elif 'subarray' in title_lower or 'maximum' in title_lower:
        key = "max_subarray"
    elif 'substring' in title_lower or 'longest' in title_lower:
        key = "longest_substring"
    else:
        key = "default"
    
    solutions = SOLUTIONS.get(language, {})
    return solutions.get(key, solutions.get("default", ""))

def prepare_test_cases(question_data):
    """Prepare test cases from question data"""
    test_cases = []
    
    if question_data and 'test_cases' in question_data:
        for idx, tc in enumerate(question_data['test_cases'][:3]):  # Limit to 3 test cases
            test_cases.append({
                "id": f"test_{idx + 1}",
                "input": tc.get('input', tc.get('stdin', '')),
                "expected_output": tc.get('expected_output', tc.get('stdout', tc.get('output', '')))
            })
    
    # Default test case if none found
    if not test_cases:
        test_cases = [{"id": "test_1", "input": "5", "expected_output": "15"}]
    
    return test_cases

def execute_user_request(user_id, question, language="python", executor_url=None):
    """Execute a single user's request"""
    start_time = time.time()
    result = {
        "user_id": user_id,
        "question_id": question.get('id', 'unknown'),
        "question_title": question.get('title', 'Unknown'),
        "language": language,
        "status": "pending",
        "start_time": start_time,
        "end_time": None,
        "duration": 0,
        "execution_time_ms": 0,
        "container_id": "unknown",
        "cpu_usage_percent": 0,
        "memory_usage_mb": 0,
        "all_passed": False,
        "passed_tests": 0,
        "total_tests": 0,
        "error": None
    }
    
    try:
        # Get question details
        question_data = get_question_details(question.get('id'))
        
        # Prepare code and test cases
        code = get_code_for_question(question, language)
        test_cases = prepare_test_cases(question_data)
        
        if not code:
            result["error"] = "No code solution available"
            result["status"] = "error"
            return result
        
        # Prepare payload
        payload = {
            "language": language,
            "code": code,
            "test_cases": test_cases,
            "user_id": user_id,
            "question_id": str(question.get('id', 'unknown'))
        }
        
        # Execute request
        data_json = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            f"{executor_url}/execute",
            data=data_json,
            headers={"Content-Type": "application/json"},
            method='POST'
        )
        
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                data = json.loads(response.read().decode())
                end_time = time.time()
                result["end_time"] = end_time
                result["duration"] = end_time - start_time
                
                # Extract metadata
                metadata = data.get('metadata', {})
                summary = data.get('summary', {})
                
                result["status"] = "success"
                result["execution_time_ms"] = metadata.get('execution_time_ms', 0)
                result["container_id"] = metadata.get('container_id', 'unknown')
                result["cpu_usage_percent"] = metadata.get('cpu_usage_percent', 0)
                result["memory_usage_mb"] = metadata.get('memory_usage_mb', 0)
                result["all_passed"] = summary.get('all_passed', False)
                result["passed_tests"] = summary.get('passed', 0)
                result["total_tests"] = summary.get('total_tests', 0)
        except urllib.error.HTTPError as e:
            result["status"] = "error"
            result["error"] = f"HTTP {e.code}: {e.read().decode()[:100]}"
            result["end_time"] = time.time()
            result["duration"] = result["end_time"] - result["start_time"]
            return result
            
            # Extract metadata
            metadata = data.get('metadata', {})
            summary = data.get('summary', {})
            

    
    except urllib.error.URLError as e:
        if 'timeout' in str(e).lower():
            result["status"] = "timeout"
            result["error"] = "Request timeout (60s)"
        else:
            result["status"] = "error"
            result["error"] = str(e)[:100]
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)[:100]
        result["end_time"] = time.time()
        result["duration"] = result["end_time"] - result["start_time"]
    
    return result

def print_results_summary(results, start_time, end_time):
    """Print detailed results summary"""
    total_duration = end_time - start_time
    
    print("\n" + "="*100)
    print("📊 LOAD TEST RESULTS SUMMARY")
    print("="*100)
    
    # Overall statistics
    total_users = len(results)
    successful = sum(1 for r in results if r['status'] == 'success')
    failed = total_users - successful
    all_passed = sum(1 for r in results if r.get('all_passed', False))
    
    print(f"\n🎯 Overall Statistics:")
    print(f"   Total Users: {total_users}")
    print(f"   Successful Requests: {successful} ({successful/total_users*100:.1f}%)")
    print(f"   Failed Requests: {failed} ({failed/total_users*100:.1f}%)")
    print(f"   All Tests Passed: {all_passed} ({all_passed/total_users*100:.1f}%)")
    print(f"   Total Duration: {total_duration:.2f}s")
    print(f"   Average Duration per User: {total_duration/total_users:.2f}s")
    
    # Performance metrics
    successful_results = [r for r in results if r['status'] == 'success']
    if successful_results:
        avg_exec_time = sum(r['execution_time_ms'] for r in successful_results) / len(successful_results)
        avg_cpu = sum(r['cpu_usage_percent'] for r in successful_results) / len(successful_results)
        avg_memory = sum(r['memory_usage_mb'] for r in successful_results) / len(successful_results)
        
        print(f"\n⚡ Performance Metrics:")
        print(f"   Average Execution Time: {avg_exec_time:.2f}ms")
        print(f"   Average CPU Usage: {avg_cpu:.2f}%")
        print(f"   Average Memory Usage: {avg_memory:.2f}MB")
        
        min_time = min(r['execution_time_ms'] for r in successful_results)
        max_time = max(r['execution_time_ms'] for r in successful_results)
        print(f"   Min Execution Time: {min_time:.2f}ms")
        print(f"   Max Execution Time: {max_time:.2f}ms")
    
    # Container distribution
    container_usage = defaultdict(int)
    container_cpu = defaultdict(list)
    container_memory = defaultdict(list)
    
    for r in successful_results:
        container_id = r['container_id']
        container_usage[container_id] += 1
        container_cpu[container_id].append(r['cpu_usage_percent'])
        container_memory[container_id].append(r['memory_usage_mb'])
    
    print(f"\n📦 Container Distribution:")
    print(f"   Unique Containers Used: {len(container_usage)}")
    for container_id, count in sorted(container_usage.items(), key=lambda x: x[1], reverse=True):
        avg_cpu = sum(container_cpu[container_id]) / len(container_cpu[container_id]) if container_cpu[container_id] else 0
        avg_mem = sum(container_memory[container_id]) / len(container_memory[container_id]) if container_memory[container_id] else 0
        print(f"   {container_id[:50]}: {count} requests | Avg CPU: {avg_cpu:.1f}% | Avg Mem: {avg_mem:.1f}MB")
    
    # Language distribution
    language_usage = defaultdict(int)
    for r in results:
        language_usage[r['language']] += 1
    
    print(f"\n💻 Language Distribution:")
    for lang, count in sorted(language_usage.items()):
        print(f"   {lang}: {count} requests")
    
    # Detailed user results
    print(f"\n" + "="*100)
    print("👥 DETAILED USER RESULTS")
    print("="*100)
    print(f"{'User ID':<20} {'Question':<25} {'Lang':<8} {'Status':<10} {'Time(ms)':<10} {'CPU%':<8} {'Mem(MB)':<10} {'Container':<30} {'Tests':<10}")
    print("-"*100)
    
    for r in sorted(results, key=lambda x: x['start_time']):
        status_icon = "✅" if r['status'] == 'success' and r.get('all_passed') else "❌" if r['status'] == 'success' else "⚠️"
        tests_str = f"{r.get('passed_tests', 0)}/{r.get('total_tests', 0)}"
        container_short = r['container_id'][:28] + ".." if len(r['container_id']) > 30 else r['container_id']
        
        print(f"{r['user_id']:<20} {r['question_title'][:23]:<25} {r['language']:<8} {status_icon} {r['status']:<7} "
              f"{r['execution_time_ms']:<10.0f} {r['cpu_usage_percent']:<8.1f} {r['memory_usage_mb']:<10.1f} "
              f"{container_short:<30} {tests_str:<10}")
    
    # Errors
    errors = [r for r in results if r.get('error')]
    if errors:
        print(f"\n" + "="*100)
        print("❌ ERRORS")
        print("="*100)
        for r in errors:
            print(f"   {r['user_id']}: {r.get('error', 'Unknown error')}")

def main():
    parser = argparse.ArgumentParser(description='Load test executor with multiple users')
    parser.add_argument('-n', '--users', type=int, default=30, help='Number of concurrent users (default: 30)')
    parser.add_argument('-l', '--language', default='python', choices=['python', 'java', 'javascript', 'cpp'],
                       help='Programming language (default: python)')
    parser.add_argument('--executor-url', help='Executor URL (auto-detected if not provided)')
    parser.add_argument('--test-ui-url', default='http://localhost:3001', help='Test UI URL (default: http://localhost:3001)')
    
    args = parser.parse_args()
    
    global TEST_UI_URL, EXECUTOR_URL, NUM_USERS
    TEST_UI_URL = args.test_ui_url
    NUM_USERS = args.users
    
    print("🚀 Load Testing: Multiple Users with Real DSA Questions")
    print("="*100)
    print(f"📊 Configuration:")
    print(f"   Number of Users: {NUM_USERS}")
    print(f"   Language: {args.language}")
    print(f"   Test UI URL: {TEST_UI_URL}")
    
    # Get executor URL
    if args.executor_url:
        EXECUTOR_URL = args.executor_url
    else:
        print("   Fetching executor URL from Azure...")
        EXECUTOR_URL = get_executor_url()
    
    print(f"   Executor URL: {EXECUTOR_URL}")
    
    # Get initial replica count
    initial_replicas = get_replica_count()
    print(f"   Initial Replicas: {initial_replicas}")
    
    # Fetch questions
    print(f"\n📚 Fetching questions from database...")
    questions = fetch_questions()
    print(f"   Found {len(questions)} questions")
    
    if not questions:
        print("❌ No questions found. Exiting.")
        return
    
    # Prepare user tasks
    print(f"\n👥 Preparing {NUM_USERS} user requests...")
    user_tasks = []
    languages = ['python', 'java', 'javascript', 'cpp'] if args.language == 'all' else [args.language]
    
    for i in range(1, NUM_USERS + 1):
        user_id = f"load_test_user_{i}"
        question = questions[i % len(questions)]  # Cycle through questions
        language = languages[i % len(languages)]  # Cycle through languages
        user_tasks.append((user_id, question, language))
    
    # Execute all requests concurrently
    print(f"\n⚡ Executing {NUM_USERS} concurrent requests...")
    print("   (This may take a while depending on load and replica scaling)")
    print("-"*100)
    
    start_time = time.time()
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(execute_user_request, user_id, question, language, EXECUTOR_URL): (user_id, question, language)
            for user_id, question, language in user_tasks
        }
        
        completed = 0
        for future in concurrent.futures.as_completed(futures):
            completed += 1
            result = future.result()
            results.append(result)
            
            # Progress indicator
            if completed % 5 == 0 or completed == NUM_USERS:
                status_icon = "✅" if result['status'] == 'success' else "❌"
                print(f"   [{completed}/{NUM_USERS}] {result['user_id']}: {status_icon} {result['status']} "
                      f"({result['execution_time_ms']:.0f}ms, CPU: {result['cpu_usage_percent']:.1f}%)")
    
    end_time = time.time()
    
    # Get final replica count
    final_replicas = get_replica_count()
    
    # Print results
    print_results_summary(results, start_time, end_time)
    
    # Replica scaling info
    print(f"\n" + "="*100)
    print("📈 REPLICA SCALING")
    print("="*100)
    print(f"   Initial Replicas: {initial_replicas}")
    print(f"   Final Replicas: {final_replicas}")
    if initial_replicas != final_replicas:
        print(f"   ✅ Replicas scaled from {initial_replicas} to {final_replicas}")
    else:
        print(f"   ℹ️  Replicas remained at {initial_replicas}")
    
    # Save results to file
    output_file = f"load_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump({
            "summary": {
                "total_users": NUM_USERS,
                "successful": sum(1 for r in results if r['status'] == 'success'),
                "failed": sum(1 for r in results if r['status'] != 'success'),
                "total_duration": end_time - start_time,
                "initial_replicas": initial_replicas,
                "final_replicas": final_replicas
            },
            "results": results
        }, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: {output_file}")
    print("="*100)

if __name__ == "__main__":
    main()

