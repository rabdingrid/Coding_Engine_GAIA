#!/usr/bin/env python3
"""
Test Graph Question (Number of Islands) with All 5 Languages
Then test with multiple concurrent users to verify queue handling
"""

import json
import time
import concurrent.futures
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime
from collections import defaultdict

# Configuration
EXECUTOR_URL = "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io"
TEST_UI_URL = "http://localhost:3001"

# Number of Islands - Graph Question Solutions
SOLUTIONS = {
    "python": """def numIslands(grid):
    if not grid:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    islands = 0
    
    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == '0':
            return
        grid[r][c] = '0'
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
    
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '1':
                islands += 1
                dfs(i, j)
    
    return islands

# Read input
rows = int(input())
cols = int(input())
grid = []
for i in range(rows):
    row = input().split()
    grid.append(row)

print(numIslands(grid))""",

    "java": """import java.util.*;

public class Main {
    public int numIslands(char[][] grid) {
        if (grid == null || grid.length == 0) return 0;
        
        int rows = grid.length;
        int cols = grid[0].length;
        int islands = 0;
        
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (grid[i][j] == '1') {
                    islands++;
                    dfs(grid, i, j, rows, cols);
                }
            }
        }
        return islands;
    }
    
    private void dfs(char[][] grid, int r, int c, int rows, int cols) {
        if (r < 0 || r >= rows || c < 0 || c >= cols || grid[r][c] == '0') {
            return;
        }
        
        grid[r][c] = '0';
        dfs(grid, r + 1, c, rows, cols);
        dfs(grid, r - 1, c, rows, cols);
        dfs(grid, r, c + 1, rows, cols);
        dfs(grid, r, c - 1, rows, cols);
    }
    
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int rows = sc.nextInt();
        int cols = sc.nextInt();
        sc.nextLine(); // Consume newline after cols
        
        char[][] grid = new char[rows][cols];
        
        for (int i = 0; i < rows; i++) {
            String line = sc.nextLine().trim();
            String[] values = line.split("\\s+");
            for (int j = 0; j < cols && j < values.length; j++) {
                grid[i][j] = values[j].charAt(0);
            }
        }
        
        Main sol = new Main();
        System.out.println(sol.numIslands(grid));
    }
}""",

    "cpp": """#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    int numIslands(vector<vector<char>>& grid) {
        if (grid.empty() || grid[0].empty()) return 0;
        
        int rows = grid.size();
        int cols = grid[0].size();
        int islands = 0;
        
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (grid[i][j] == '1') {
                    islands++;
                    dfs(grid, i, j);
                }
            }
        }
        return islands;
    }
    
private:
    void dfs(vector<vector<char>>& grid, int r, int c) {
        int rows = grid.size();
        int cols = grid[0].size();
        
        if (r < 0 || r >= rows || c < 0 || c >= cols || grid[r][c] == '0') {
            return;
        }
        
        grid[r][c] = '0';
        dfs(grid, r + 1, c);
        dfs(grid, r - 1, c);
        dfs(grid, r, c + 1);
        dfs(grid, r, c - 1);
    }
};

int main() {
    int rows, cols;
    cin >> rows >> cols;
    vector<vector<char>> grid(rows, vector<char>(cols));
    
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            cin >> grid[i][j];
        }
    }
    
    Solution sol;
    cout << sol.numIslands(grid) << endl;
    return 0;
}""",

    "javascript": """function numIslands(grid) {
    if (!grid || grid.length === 0) return 0;
    
    const rows = grid.length;
    const cols = grid[0].length;
    let islands = 0;
    
    function dfs(r, c) {
        if (r < 0 || r >= rows || c < 0 || c >= cols || grid[r][c] === '0') {
            return;
        }
        grid[r][c] = '0';
        dfs(r + 1, c);
        dfs(r - 1, c);
        dfs(r, c + 1);
        dfs(r, c - 1);
    }
    
    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < cols; j++) {
            if (grid[i][j] === '1') {
                islands++;
                dfs(i, j);
            }
        }
    }
    
    return islands;
}

const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

let input = [];
rl.on('line', (line) => {
    input.push(line);
    if (input.length >= 2) {
        const rows = parseInt(input[0]);
        const cols = parseInt(input[1]);
        if (input.length >= rows + 2) {
            const grid = [];
            for (let i = 2; i < rows + 2; i++) {
                if (input[i]) {
                    grid.push(input[i].trim().split(/\\s+/));
                }
            }
            if (grid.length === rows) {
                console.log(numIslands(grid));
                rl.close();
            }
        }
    }
});""",

    "csharp": """using System;
using System.Collections.Generic;

public class Solution {
    public int NumIslands(char[][] grid) {
        if (grid == null || grid.Length == 0) return 0;
        
        int rows = grid.Length;
        int cols = grid[0].Length;
        int islands = 0;
        
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (grid[i][j] == '1') {
                    islands++;
                    DFS(grid, i, j, rows, cols);
                }
            }
        }
        return islands;
    }
    
    private void DFS(char[][] grid, int r, int c, int rows, int cols) {
        if (r < 0 || r >= rows || c < 0 || c >= cols || grid[r][c] == '0') {
            return;
        }
        
        grid[r][c] = '0';
        DFS(grid, r + 1, c, rows, cols);
        DFS(grid, r - 1, c, rows, cols);
        DFS(grid, r, c + 1, rows, cols);
        DFS(grid, r, c - 1, rows, cols);
    }
    
    public static void Main() {
        int rows = int.Parse(Console.ReadLine());
        int cols = int.Parse(Console.ReadLine());
        char[][] grid = new char[rows][];
        
        for (int i = 0; i < rows; i++) {
            string line = Console.ReadLine();
            if (string.IsNullOrEmpty(line)) {
                line = Console.ReadLine();
            }
            string[] values = line.Trim().Split(new char[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
            grid[i] = new char[cols];
            for (int j = 0; j < cols && j < values.Length; j++) {
                grid[i][j] = values[j][0];
            }
        }
        
        Solution sol = new Solution();
        Console.WriteLine(sol.NumIslands(grid));
    }
}"""
}

# Test case for Number of Islands
# Format: rows, cols, then grid as space-separated values per row
TEST_CASE = {
    "input": "3\n3\n1 1 0\n1 0 0\n0 0 1",
    "expected_output": "2"
}

# Simpler test case for better compatibility
SIMPLE_TEST_CASE = {
    "input": "4\n5\n1 1 1 1 0\n1 1 0 1 0\n1 1 0 0 0\n0 0 0 0 0",
    "expected_output": "1"
}

def execute_code(language, code, test_input, user_id):
    """Execute code for a user"""
    start_time = time.time()
    result = {
        "user_id": user_id,
        "language": language,
        "start_time": start_time,
        "status": "pending"
    }
    
    try:
        payload = {
            "language": language,
            "code": code,
            "test_cases": [{
                "input": test_input,
                "expected_output": SIMPLE_TEST_CASE["expected_output"]
            }]
        }
        
        data_json = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            f"{EXECUTOR_URL}/execute",
            data=data_json,
            headers={"Content-Type": "application/json"},
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            data = json.loads(response.read().decode())
            end_time = time.time()
            
            result["end_time"] = end_time
            result["duration"] = end_time - start_time
            result["status"] = "success"
            
            # Extract metadata
            metadata = data.get('metadata', {})
            summary = data.get('summary', {})
            test_results = data.get('test_results', [])
            
            result["execution_time_ms"] = metadata.get('execution_time_ms', 0)
            result["container_id"] = metadata.get('container_id', 'unknown')
            result["cpu_usage_percent"] = metadata.get('cpu_usage_percent', 0)
            result["memory_usage_mb"] = metadata.get('memory_usage_mb', 0)
            result["all_passed"] = summary.get('all_passed', False)
            result["passed_tests"] = summary.get('passed', 0)
            result["total_tests"] = summary.get('total_tests', 0)
            result["test_passed"] = test_results[0].get('passed', False) if test_results else False
            
    except urllib.error.HTTPError as e:
        result["status"] = "error"
        result["error"] = f"HTTP {e.code}: {e.read().decode()[:100]}"
        result["end_time"] = time.time()
        result["duration"] = result["end_time"] - result["start_time"]
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

def test_all_languages():
    """Test Number of Islands with all 5 languages"""
    print("🧪 Testing Graph Question: Number of Islands")
    print("=" * 70)
    print(f"Test Case: {SIMPLE_TEST_CASE['input']}")
    print(f"Expected Output: {SIMPLE_TEST_CASE['expected_output']}")
    print("=" * 70)
    print()
    
    results = {}
    
    for lang in ["python", "java", "cpp", "javascript", "csharp"]:
        print(f"📝 Testing {lang.upper()}...")
        result = execute_code(lang, SOLUTIONS[lang], SIMPLE_TEST_CASE["input"], f"test_{lang}")
        results[lang] = result
        
        status_icon = "✅" if result.get("test_passed") else "❌"
        print(f"   {status_icon} {lang.upper()}: {result['status']} "
              f"({result.get('execution_time_ms', 0)}ms, "
              f"CPU: {result.get('cpu_usage_percent', 0):.1f}%, "
              f"Mem: {result.get('memory_usage_mb', 0):.1f}MB)")
        if result.get("test_passed"):
            print(f"   ✅ Test passed!")
        elif result.get("error"):
            print(f"   ❌ Error: {result.get('error', 'Unknown')[:50]}")
        print()
    
    return results

def test_concurrent_users(num_users=30, languages=None):
    """Test with multiple concurrent users"""
    if languages is None:
        languages = ["python", "java", "cpp", "javascript", "csharp"]
    
    print("🚀 Testing Concurrent Users with Queue Handling")
    print("=" * 70)
    print(f"Number of Users: {num_users}")
    print(f"Languages: {', '.join(languages)}")
    print(f"Question: Number of Islands (Graph)")
    print("=" * 70)
    print()
    
    # Distribute users across languages
    users_per_lang = num_users // len(languages)
    remaining = num_users % len(languages)
    
    user_tasks = []
    user_id = 1
    
    for lang in languages:
        count = users_per_lang + (1 if remaining > 0 else 0)
        remaining -= 1
        for i in range(count):
            user_tasks.append({
                "user_id": f"user_{user_id:03d}",
                "language": lang,
                "code": SOLUTIONS[lang],
                "test_input": SIMPLE_TEST_CASE["input"]
            })
            user_id += 1
    
    print(f"👥 Prepared {len(user_tasks)} user requests")
    dist_str = ', '.join([f"{lang}: {sum(1 for u in user_tasks if u['language'] == lang)}" for lang in languages])
    print(f"   Distribution: {dist_str}")
    print()
    print("⚡ Executing all requests concurrently...")
    print("   (This will test queue handling)")
    print("-" * 70)
    
    start_time = time.time()
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_users) as executor:
        futures = []
        for task in user_tasks:
            future = executor.submit(
                execute_code,
                task["language"],
                task["code"],
                task["test_input"],
                task["user_id"]
            )
            futures.append(future)
        
        completed = 0
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            completed += 1
            if completed % 5 == 0:
                print(f"   [{completed}/{num_users}] {result['user_id']}: "
                      f"{result['status']} ({result.get('execution_time_ms', 0)}ms, "
                      f"CPU: {result.get('cpu_usage_percent', 0):.1f}%)")
    
    end_time = time.time()
    total_duration = end_time - start_time
    
    print("-" * 70)
    print()
    
    # Analyze results
    successful = [r for r in results if r["status"] == "success"]
    failed = [r for r in results if r["status"] != "success"]
    passed = [r for r in successful if r.get("test_passed")]
    
    # Container distribution
    containers = defaultdict(list)
    for r in successful:
        containers[r.get("container_id", "unknown")].append(r)
    
    # Language distribution
    lang_stats = defaultdict(lambda: {"total": 0, "passed": 0, "failed": 0})
    for r in results:
        lang = r["language"]
        lang_stats[lang]["total"] += 1
        if r.get("test_passed"):
            lang_stats[lang]["passed"] += 1
        else:
            lang_stats[lang]["failed"] += 1
    
    # Print summary
    print("=" * 70)
    print("📊 CONCURRENT TEST RESULTS SUMMARY")
    print("=" * 70)
    print()
    print(f"🎯 Overall Statistics:")
    print(f"   Total Users: {num_users}")
    print(f"   Successful Requests: {len(successful)} ({len(successful)/num_users*100:.1f}%)")
    print(f"   Failed Requests: {len(failed)} ({len(failed)/num_users*100:.1f}%)")
    print(f"   Tests Passed: {len(passed)} ({len(passed)/num_users*100:.1f}%)")
    print(f"   Total Duration: {total_duration:.2f}s")
    print(f"   Average Duration per User: {total_duration/num_users:.2f}s")
    print()
    
    if successful:
        avg_time = sum(r.get("execution_time_ms", 0) for r in successful) / len(successful)
        avg_cpu = sum(r.get("cpu_usage_percent", 0) for r in successful) / len(successful)
        avg_mem = sum(r.get("memory_usage_mb", 0) for r in successful) / len(successful)
        
        print(f"⚡ Performance Metrics:")
        print(f"   Average Execution Time: {avg_time:.2f}ms")
        print(f"   Average CPU Usage: {avg_cpu:.1f}%")
        print(f"   Average Memory Usage: {avg_mem:.2f}MB")
        print()
    
    print(f"📦 Container Distribution:")
    print(f"   Unique Containers Used: {len(containers)}")
    for container_id, container_results in sorted(containers.items(), key=lambda x: len(x[1]), reverse=True):
        container_name = container_id[:50] + "..." if len(container_id) > 50 else container_id
        avg_cpu = sum(r.get("cpu_usage_percent", 0) for r in container_results) / len(container_results)
        avg_mem = sum(r.get("memory_usage_mb", 0) for r in container_results) / len(container_results)
        print(f"   {container_name}: {len(container_results)} requests | "
              f"Avg CPU: {avg_cpu:.1f}% | Avg Mem: {avg_mem:.1f}MB")
    print()
    
    print(f"💻 Language Distribution:")
    for lang in languages:
        stats = lang_stats[lang]
        pass_rate = (stats["passed"] / stats["total"] * 100) if stats["total"] > 0 else 0
        print(f"   {lang.upper()}: {stats['total']} requests | "
              f"Passed: {stats['passed']} ({pass_rate:.1f}%) | "
              f"Failed: {stats['failed']}")
    print()
    
    # Detailed results table
    print("=" * 70)
    print("👥 DETAILED USER RESULTS")
    print("=" * 70)
    print(f"{'User ID':<15} {'Language':<12} {'Status':<10} {'Time(ms)':<10} "
          f"{'CPU%':<8} {'Mem(MB)':<10} {'Container':<30} {'Test':<8}")
    print("-" * 70)
    
    for r in sorted(results, key=lambda x: x["start_time"]):
        user_id = r["user_id"]
        lang = r["language"]
        status = "✅" if r.get("test_passed") else "❌"
        status_text = r["status"]
        time_ms = r.get("execution_time_ms", 0)
        cpu = r.get("cpu_usage_percent", 0)
        mem = r.get("memory_usage_mb", 0)
        container = (r.get("container_id", "unknown")[:28] + "..") if len(r.get("container_id", "")) > 30 else r.get("container_id", "unknown")
        test_status = "✅" if r.get("test_passed") else "❌"
        
        print(f"{user_id:<15} {lang:<12} {status_text:<10} {time_ms:<10.0f} "
              f"{cpu:<8.1f} {mem:<10.1f} {container:<30} {test_status:<8}")
    
    print()
    print("=" * 70)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"graph_test_results_{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump({
            "test_type": "graph_question_all_languages_concurrent",
            "question": "Number of Islands",
            "total_users": num_users,
            "languages": languages,
            "summary": {
                "total_users": num_users,
                "successful": len(successful),
                "failed": len(failed),
                "passed": len(passed),
                "total_duration": total_duration,
                "containers_used": len(containers)
            },
            "results": results
        }, f, indent=2)
    
    print(f"💾 Detailed results saved to: {filename}")
    print("=" * 70)
    
    return results

if __name__ == "__main__":
    import sys
    
    # Test all languages first
    print("=" * 70)
    print("STEP 1: Testing All Languages Individually")
    print("=" * 70)
    print()
    lang_results = test_all_languages()
    
    print()
    print("=" * 70)
    print("STEP 2: Testing Concurrent Users (Queue Handling)")
    print("=" * 70)
    print()
    
    # Test with concurrent users
    num_users = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    concurrent_results = test_concurrent_users(num_users)
    
    print()
    print("🎉 Testing Complete!")
    print()
    print("Summary:")
    print(f"  ✅ Languages tested: {len([r for r in lang_results.values() if r.get('test_passed')])}/5")
    print(f"  ✅ Concurrent users: {len([r for r in concurrent_results if r['status'] == 'success'])}/{num_users}")
    print(f"  ✅ Queue handling: {'Working' if len([r for r in concurrent_results if r['status'] == 'success']) > num_users * 0.9 else 'Check results'}")

