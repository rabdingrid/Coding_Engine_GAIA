#!/usr/bin/env python3
"""
Test Endpoint Inspection question with correct solutions in all languages
"""

import json
import urllib.request
import urllib.parse
import time

API_URL = "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io"

# Correct solutions for each language
SOLUTIONS = {
    "python": """def getMinChecks(endpoint, m, k):
    n = len(endpoint)
    min_checks = float('inf')
    count_min = 0
    
    # Try removing each endpoint
    for remove_idx in range(n):
        # Create set of remaining problematic endpoints
        remaining = set(endpoint[i] for i in range(n) if i != remove_idx)
        
        # Simulate traversal
        inspections = 0
        last_inspection = 0
        
        for pos in range(1, m + 1):
            must_check = False
            
            # Check if this position has a known issue
            if pos in remaining:
                must_check = True
            
            # Check if k seconds have passed
            if pos - last_inspection >= k:
                must_check = True
            
            if must_check:
                inspections += 1
                last_inspection = pos
        
        # Update minimum
        if inspections < min_checks:
            min_checks = inspections
            count_min = 1
        elif inspections == min_checks:
            count_min += 1
    
    return [min_checks, count_min]

endpoint_count = int(input().strip())
endpoint = []
for _ in range(endpoint_count):
    endpoint_item = int(input().strip())
    endpoint.append(endpoint_item)
m = int(input().strip())
k = int(input().strip())
result = getMinChecks(endpoint, m, k)
print('\\n'.join(map(str, result)))""",

    "cpp": """#include <bits/stdc++.h>
using namespace std;

string ltrim(const string &);
string rtrim(const string &);

vector<int> getMinChecks(vector<int> endpoint, int m, int k) {
    int n = endpoint.size();
    int min_checks = INT_MAX;
    int count_min = 0;
    
    // Try removing each endpoint
    for (int remove_idx = 0; remove_idx < n; remove_idx++) {
        set<int> remaining;
        for (int i = 0; i < n; i++) {
            if (i != remove_idx) {
                remaining.insert(endpoint[i]);
            }
        }
        
        // Simulate traversal
        int inspections = 0;
        int last_inspection = 0;
        
        for (int pos = 1; pos <= m; pos++) {
            bool must_check = false;
            
            // Check if this position has a known issue
            if (remaining.find(pos) != remaining.end()) {
                must_check = true;
            }
            
            // Check if k seconds have passed
            if (pos - last_inspection >= k) {
                must_check = true;
            }
            
            if (must_check) {
                inspections++;
                last_inspection = pos;
            }
        }
        
        // Update minimum
        if (inspections < min_checks) {
            min_checks = inspections;
            count_min = 1;
        } else if (inspections == min_checks) {
            count_min++;
        }
    }
    
    return {min_checks, count_min};
}

int main()
{
    string endpoint_count_temp;
    getline(cin, endpoint_count_temp);
    int endpoint_count = stoi(ltrim(rtrim(endpoint_count_temp)));
    vector<int> endpoint(endpoint_count);
    for (int i = 0; i < endpoint_count; i++) {
        string endpoint_item_temp;
        getline(cin, endpoint_item_temp);
        int endpoint_item = stoi(ltrim(rtrim(endpoint_item_temp)));
        endpoint[i] = endpoint_item;
    }
    string m_temp;
    getline(cin, m_temp);
    int m = stoi(ltrim(rtrim(m_temp)));
    string k_temp;
    getline(cin, k_temp);
    int k = stoi(ltrim(rtrim(k_temp)));
    vector<int> result = getMinChecks(endpoint, m, k);
    for (size_t i = 0; i < result.size(); i++) {
        cout << result[i];
        if (i != result.size() - 1) {
            cout << "\\n";
        }
    }
    cout << "\\n";
    return 0;
}

string ltrim(const string &str) {
    string s(str);
    s.erase(
        s.begin(),
        find_if(s.begin(), s.end(), not1(ptr_fun<int, int>(isspace)))
    );
    return s;
}

string rtrim(const string &str) {
    string s(str);
    s.erase(
        find_if(s.rbegin(), s.rend(), not1(ptr_fun<int, int>(isspace))).base(),
        s.end()
    );
    return s;
}""",

    "java": """import java.io.*;
import java.math.*;
import java.security.*;
import java.text.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.function.*;
import java.util.regex.*;
import java.util.stream.*;
import static java.util.stream.Collectors.joining;
import static java.util.stream.Collectors.toList;

class Result {
    public static List<Integer> getMinChecks(List<Integer> endpoint, int m, int k) {
        int n = endpoint.size();
        int minChecks = Integer.MAX_VALUE;
        int countMin = 0;
        
        // Try removing each endpoint
        for (int removeIdx = 0; removeIdx < n; removeIdx++) {
            Set<Integer> remaining = new HashSet<>();
            for (int i = 0; i < n; i++) {
                if (i != removeIdx) {
                    remaining.add(endpoint.get(i));
                }
            }
            
            // Simulate traversal
            int inspections = 0;
            int lastInspection = 0;
            
            for (int pos = 1; pos <= m; pos++) {
                boolean mustCheck = false;
                
                // Check if this position has a known issue
                if (remaining.contains(pos)) {
                    mustCheck = true;
                }
                
                // Check if k seconds have passed
                if (pos - lastInspection >= k) {
                    mustCheck = true;
                }
                
                if (mustCheck) {
                    inspections++;
                    lastInspection = pos;
                }
            }
            
            // Update minimum
            if (inspections < minChecks) {
                minChecks = inspections;
                countMin = 1;
            } else if (inspections == minChecks) {
                countMin++;
            }
        }
        
        return Arrays.asList(minChecks, countMin);
    }
}

class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(System.in));
        int endpointCount = Integer.parseInt(bufferedReader.readLine().trim());
        List<Integer> endpoint = IntStream.range(0, endpointCount).mapToObj(i -> {
            try {
                return bufferedReader.readLine().replaceAll("\\\\s+$", "");
            } catch (IOException ex) {
                throw new RuntimeException(ex);
            }
        })
            .map(String::trim)
            .map(Integer::parseInt)
            .collect(toList());
        int m = Integer.parseInt(bufferedReader.readLine().trim());
        int k = Integer.parseInt(bufferedReader.readLine().trim());
        List<Integer> result = Result.getMinChecks(endpoint, m, k);
        System.out.println(
            result.stream()
                .map(Object::toString)
                .collect(joining("\\n"))
        );
        bufferedReader.close();
    }
}""",

    "javascript": """function getMinChecks(endpoint, m, k) {
    const n = endpoint.length;
    let minChecks = Infinity;
    let countMin = 0;
    
    // Try removing each endpoint
    for (let removeIdx = 0; removeIdx < n; removeIdx++) {
        const remaining = new Set();
        for (let i = 0; i < n; i++) {
            if (i !== removeIdx) {
                remaining.add(endpoint[i]);
            }
        }
        
        // Simulate traversal
        let inspections = 0;
        let lastInspection = 0;
        
        for (let pos = 1; pos <= m; pos++) {
            let mustCheck = false;
            
            // Check if this position has a known issue
            if (remaining.has(pos)) {
                mustCheck = true;
            }
            
            // Check if k seconds have passed
            if (pos - lastInspection >= k) {
                mustCheck = true;
            }
            
            if (mustCheck) {
                inspections++;
                lastInspection = pos;
            }
        }
        
        // Update minimum
        if (inspections < minChecks) {
            minChecks = inspections;
            countMin = 1;
        } else if (inspections === minChecks) {
            countMin++;
        }
    }
    
    return [minChecks, countMin];
}

const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false
});

const lines = [];
rl.on('line', (line) => {
    lines.push(line);
});

rl.on('close', () => {
    const endpointCount = parseInt(lines[0].trim(), 10);
    let endpoint = [];
    for (let i = 1; i <= endpointCount; i++) {
        endpoint.push(parseInt(lines[i].trim(), 10));
    }
    const m = parseInt(lines[endpointCount + 1].trim(), 10);
    const k = parseInt(lines[endpointCount + 2].trim(), 10);
    const result = getMinChecks(endpoint, m, k);
    console.log(result.join('\\n'));
});""",

    "csharp": """using System.CodeDom.Compiler;
using System.Collections.Generic;
using System.Collections;
using System.ComponentModel;
using System.Diagnostics.CodeAnalysis;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.Serialization;
using System.Text.RegularExpressions;
using System.Text;
using System;

class Result {
    public static List<int> getMinChecks(List<int> endpoint, int m, int k)
    {
        int n = endpoint.Count;
        int minChecks = int.MaxValue;
        int countMin = 0;
        
        // Try removing each endpoint
        for (int removeIdx = 0; removeIdx < n; removeIdx++) {
            HashSet<int> remaining = new HashSet<int>();
            for (int i = 0; i < n; i++) {
                if (i != removeIdx) {
                    remaining.Add(endpoint[i]);
                }
            }
            
            // Simulate traversal
            int inspections = 0;
            int lastInspection = 0;
            
            for (int pos = 1; pos <= m; pos++) {
                bool mustCheck = false;
                
                // Check if this position has a known issue
                if (remaining.Contains(pos)) {
                    mustCheck = true;
                }
                
                // Check if k seconds have passed
                if (pos - lastInspection >= k) {
                    mustCheck = true;
                }
                
                if (mustCheck) {
                    inspections++;
                    lastInspection = pos;
                }
            }
            
            // Update minimum
            if (inspections < minChecks) {
                minChecks = inspections;
                countMin = 1;
            } else if (inspections == minChecks) {
                countMin++;
            }
        }
        
        return new List<int> { minChecks, countMin };
    }
}

class Solution {
    public static void Main(string[] args)
    {
        int endpointCount = Convert.ToInt32(Console.ReadLine().Trim());
        List<int> endpoint = new List<int>();
        for (int i = 0; i < endpointCount; i++)
        {
            int endpointItem = Convert.ToInt32(Console.ReadLine().Trim());
            endpoint.Add(endpointItem);
        }
        int m = Convert.ToInt32(Console.ReadLine().Trim());
        int k = Convert.ToInt32(Console.ReadLine().Trim());
        List<int> result = Result.getMinChecks(endpoint, m, k);
        Console.WriteLine(String.Join("\\n", result));
    }
}"""
}

# Test cases from the first 3 samples
TEST_CASES = [
    {
        "id": "sample_1",
        "input": "3\n3\n5\n8\n8\n2",
        "expected_output": "4\n1"
    },
    {
        "id": "sample_2",
        "input": "4\n2\n8\n9\n10\n10\n9",
        "expected_output": "3\n4"
    },
    {
        "id": "sample_3",
        "input": "8\n4\n7\n5\n6\n8\n1\n3\n2\n8\n3",
        "expected_output": "7\n8"
    }
]

def test_language(language, code):
    """Test a language with the solution"""
    print(f"\n{'='*60}")
    print(f"🧪 Testing {language.upper()}")
    print(f"{'='*60}")
    
    results = []
    
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"\n📝 Test Case {i}:")
        print(f"   Input: {test_case['input'][:50]}...")
        print(f"   Expected: {test_case['expected_output']}")
        
        try:
            # Prepare request
            data = json.dumps({
                "language": language,
                "code": code,
                "sample_test_cases": [test_case],
                "user_id": f"test_user_{language}",
                "question_id": "eaec23b4-be2c-4b65-8745-15c265a56f75"
            }).encode('utf-8')
            
            req = urllib.request.Request(
                f"{API_URL}/run",
                data=data,
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            
            start_time = time.time()
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                duration = time.time() - start_time
                
                test_result = result['test_results'][0] if result['test_results'] else None
                
                if test_result:
                    passed = test_result.get('passed', False)
                    actual = test_result.get('actual_output', '').strip()
                    status = "✅ PASSED" if passed else "❌ FAILED"
                    
                    print(f"   Actual:   {actual}")
                    print(f"   Status:  {status}")
                    print(f"   Time:     {duration:.2f}s")
                    
                    if not passed:
                        error = test_result.get('error', '')
                        if error:
                            print(f"   Error:    {error[:100]}")
                    
                    results.append({
                        "test": i,
                        "passed": passed,
                        "expected": test_case['expected_output'],
                        "actual": actual
                    })
                else:
                    print(f"   ❌ ERROR: No test result returned")
                    results.append({"test": i, "passed": False, "error": "No result"})
        
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')[:200] if e.fp else str(e)
            print(f"   ❌ HTTP ERROR {e.code}: {error_body}")
            results.append({"test": i, "passed": False, "error": f"HTTP {e.code}"})
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
            results.append({"test": i, "passed": False, "error": str(e)})
    
    # Summary
    passed_count = sum(1 for r in results if r.get('passed', False))
    total_count = len(results)
    
    print(f"\n{'='*60}")
    print(f"📊 {language.upper()} Summary: {passed_count}/{total_count} tests passed")
    print(f"{'='*60}")
    
    return passed_count == total_count

def main():
    print("🚀 Testing Endpoint Inspection Question")
    print("=" * 60)
    
    all_results = {}
    
    for language, code in SOLUTIONS.items():
        success = test_language(language, code)
        all_results[language] = success
    
    # Final summary
    print(f"\n{'='*60}")
    print("📋 FINAL SUMMARY")
    print(f"{'='*60}")
    
    for language, success in all_results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"  {language.upper():12} {status}")
    
    all_passed = all(all_results.values())
    print(f"\n{'✅ ALL TESTS PASSED!' if all_passed else '❌ SOME TESTS FAILED'}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()

