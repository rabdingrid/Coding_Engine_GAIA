#!/usr/bin/env python3
"""
Test Binary Manipulation question in all 5 languages concurrently
"""

import asyncio
import asyncpg
import json
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request
import urllib.parse

API_BASE_URL = "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io"

# Binary Manipulation - minOperations function
# Given n, find minimum operations to reduce binary representation to 0

SOLUTIONS = {
    "python": """def minOperations(n):
    # Convert to binary string
    binary = bin(n)[2:]
    n_bits = len(binary)
    
    # Count operations needed
    # For each bit position, we need to flip it to 0
    # Rule 1: Can flip bit i if bit i+1 is 1 and all bits from i+2 are 0
    # Rule 2: Can always flip rightmost bit
    
    # Dynamic programming approach
    # dp[i] = min operations to make bits from i to end all zeros
    dp = [0] * (n_bits + 1)
    
    for i in range(n_bits - 1, -1, -1):
        if binary[i] == '0':
            dp[i] = dp[i + 1]
        else:
            # Need to flip this bit
            # Option 1: Use rule 2 (rightmost) - 1 operation
            # Option 2: Use rule 1 - need to check if we can
            if i == n_bits - 1:
                # Rightmost bit
                dp[i] = 1 + dp[i + 1]
            else:
                # Check if we can use rule 1
                can_use_rule1 = False
                if i + 1 < n_bits and binary[i + 1] == '1':
                    # Check if all bits from i+2 are 0
                    all_zeros = True
                    for j in range(i + 2, n_bits):
                        if binary[j] != '0':
                            all_zeros = False
                            break
                    if all_zeros:
                        can_use_rule1 = True
                
                if can_use_rule1:
                    # Use rule 1: flip bit i (costs 1), then need to handle rest
                    dp[i] = 1 + dp[i + 1]
                else:
                    # Must use rule 2: flip rightmost, then recursively handle
                    # Actually, we need to flip this bit using rule 2
                    # But rule 2 only works on rightmost, so we need to work backwards
                    dp[i] = 1 + dp[i + 1]
    
    return dp[0]""",
    
    "cpp": """#include <bits/stdc++.h>
using namespace std;

long long minOperations(long long n) {
    string binary = "";
    long long temp = n;
    while (temp > 0) {
        binary = (temp % 2 == 0 ? "0" : "1") + binary;
        temp /= 2;
    }
    if (binary.empty()) binary = "0";
    
    int n_bits = binary.length();
    vector<long long> dp(n_bits + 1, 0);
    
    for (int i = n_bits - 1; i >= 0; i--) {
        if (binary[i] == '0') {
            dp[i] = dp[i + 1];
        } else {
            if (i == n_bits - 1) {
                dp[i] = 1 + dp[i + 1];
            } else {
                bool can_use_rule1 = false;
                if (i + 1 < n_bits && binary[i + 1] == '1') {
                    bool all_zeros = true;
                    for (int j = i + 2; j < n_bits; j++) {
                        if (binary[j] != '0') {
                            all_zeros = false;
                            break;
                        }
                    }
                    if (all_zeros) can_use_rule1 = true;
                }
                dp[i] = 1 + dp[i + 1];
            }
        }
    }
    
    return dp[0];
}""",
    
    "java": """import java.io.*;
import java.util.*;

class Result {
    public static long minOperations(long n) {
        StringBuilder binary = new StringBuilder();
        long temp = n;
        while (temp > 0) {
            binary.insert(0, (temp % 2 == 0 ? "0" : "1"));
            temp /= 2;
        }
        if (binary.length() == 0) binary.append("0");
        
        int nBits = binary.length();
        long[] dp = new long[nBits + 1];
        
        for (int i = nBits - 1; i >= 0; i--) {
            if (binary.charAt(i) == '0') {
                dp[i] = dp[i + 1];
            } else {
                if (i == nBits - 1) {
                    dp[i] = 1 + dp[i + 1];
                } else {
                    boolean canUseRule1 = false;
                    if (i + 1 < nBits && binary.charAt(i + 1) == '1') {
                        boolean allZeros = true;
                        for (int j = i + 2; j < nBits; j++) {
                            if (binary.charAt(j) != '0') {
                                allZeros = false;
                                break;
                            }
                        }
                        if (allZeros) canUseRule1 = true;
                    }
                    dp[i] = 1 + dp[i + 1];
                }
            }
        }
        
        return dp[0];
    }
}""",
    
    "javascript": """function minOperations(n) {
    let binary = "";
    let temp = n;
    while (temp > 0) {
        binary = (temp % 2 === 0 ? "0" : "1") + binary;
        temp = Math.floor(temp / 2);
    }
    if (binary === "") binary = "0";
    
    const nBits = binary.length;
    const dp = new Array(nBits + 1).fill(0);
    
    for (let i = nBits - 1; i >= 0; i--) {
        if (binary[i] === '0') {
            dp[i] = dp[i + 1];
        } else {
            if (i === nBits - 1) {
                dp[i] = 1 + dp[i + 1];
            } else {
                let canUseRule1 = false;
                if (i + 1 < nBits && binary[i + 1] === '1') {
                    let allZeros = true;
                    for (let j = i + 2; j < nBits; j++) {
                        if (binary[j] !== '0') {
                            allZeros = false;
                            break;
                        }
                    }
                    if (allZeros) canUseRule1 = true;
                }
                dp[i] = 1 + dp[i + 1];
            }
        }
    }
    
    return dp[0];
}""",
    
    "csharp": """using System;
using System.Collections.Generic;
using System.Linq;

class Result {
    public static long minOperations(long n) {
        string binary = "";
        long temp = n;
        while (temp > 0) {
            binary = (temp % 2 == 0 ? "0" : "1") + binary;
            temp /= 2;
        }
        if (binary == "") binary = "0";
        
        int nBits = binary.Length;
        long[] dp = new long[nBits + 1];
        
        for (int i = nBits - 1; i >= 0; i--) {
            if (binary[i] == '0') {
                dp[i] = dp[i + 1];
            } else {
                if (i == nBits - 1) {
                    dp[i] = 1 + dp[i + 1];
                } else {
                    bool canUseRule1 = false;
                    if (i + 1 < nBits && binary[i + 1] == '1') {
                        bool allZeros = true;
                        for (int j = i + 2; j < nBits; j++) {
                            if (binary[j] != '0') {
                                allZeros = false;
                                break;
                            }
                        }
                        if (allZeros) canUseRule1 = true;
                    }
                    dp[i] = 1 + dp[i + 1];
                }
            }
        }
        
        return dp[0];
    }
}"""
}

async def get_question_data():
    """Get question data from database"""
    import asyncpg
    db_url = 'postgresql://postgresadmin:5oXcNX59QmEl7zmV3DbjemkiJ@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require'
    conn = await asyncpg.connect(db_url)
    try:
        q = await conn.fetchrow("""
            SELECT uuid, boiler_plate, test_cases
            FROM coding_question_bank 
            WHERE uuid = '13725261-21c9-424b-bced-e0be21078aeb'
        """)
        if q:
            bp = json.loads(q['boiler_plate']) if isinstance(q['boiler_plate'], str) else q['boiler_plate']
            tests = json.loads(q['test_cases']) if isinstance(q['test_cases'], str) else q['test_cases']
            return bp, tests
    finally:
        await conn.close()
    return None, None

def test_language(language, boilerplate, solution, test_cases):
    """Test one language"""
    start_time = time.time()
    
    # Combine boilerplate and solution
    if language == "python":
        code = boilerplate.replace("# Write your code here", solution)
    elif language == "cpp":
        # Find function body in solution and insert into boilerplate
        if "{" in solution and "}" in solution:
            func_body = solution.split("{", 1)[1].rsplit("}", 1)[0]
            code = boilerplate.replace("{}", func_body)
        else:
            code = boilerplate
    elif language == "java":
        # Extract Result class methods
        if "class Result" in solution:
            result_class = solution.split("class Result")[1].split("class Main")[0].strip()
            code = boilerplate.replace("// Write your code here", result_class)
        else:
            code = boilerplate
    elif language == "javascript":
        code = boilerplate.replace("// Write your code here", solution)
    elif language == "csharp":
        if "{" in solution and "}" in solution:
            func_body = solution.split("{", 1)[1].rsplit("}", 1)[0]
            code = boilerplate.replace("{}", func_body)
        else:
            code = boilerplate
    
    # Prepare test cases for /runall (as list)
    test_cases_list = []
    for i, tc in enumerate(test_cases[:5]):  # Use first 5 test cases
        test_cases_list.append({
            "id": f"test_case_{i+1}",
            "input": tc["input"],
            "expected_output": tc["expected_output"]
        })
    
    payload = {
        "code": code,
        "language": language,
        "test_cases": test_cases_list
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            f"{API_BASE_URL}/runall",
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            elapsed = time.time() - start_time
            
            return {
                "language": language,
                "status": response.status,
                "result": result,
                "time": elapsed,
                "success": response.status == 200
            }
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else "No error details"
        return {
            "language": language,
            "status": e.code,
            "error": error_body,
            "time": time.time() - start_time,
            "success": False
        }
    except Exception as e:
        return {
            "language": language,
            "status": "error",
            "error": str(e),
            "time": time.time() - start_time,
            "success": False
        }

async def test_all_languages_concurrently():
    """Test all languages concurrently"""
    print("🚀 Testing Binary Manipulation in all 5 languages concurrently...")
    print("=" * 70)
    
    # Get question data
    boilerplates, test_cases = await get_question_data()
    if not boilerplates or not test_cases:
        print("❌ Failed to get question data from database")
        return
    
    print(f"📊 Test cases: {len(test_cases)}")
    print(f"📝 Languages: {list(boilerplates.keys())}")
    print()
    
    # Create tasks for all languages
    tasks = []
    for lang in ["python", "cpp", "java", "javascript", "csharp"]:
        if lang in boilerplates and lang in SOLUTIONS:
            tasks.append((lang, boilerplates[lang], SOLUTIONS[lang], test_cases))
    
    # Run all concurrently using ThreadPoolExecutor
    start_time = time.time()
    results = []
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(test_language, lang, bp, sol, tc): lang
            for lang, bp, sol, tc in tasks
        }
        
        for future in as_completed(futures):
            lang = futures[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                results.append({
                    "language": lang,
                    "status": "error",
                    "error": str(e),
                    "time": 0,
                    "success": False
                })
    
    total_time = time.time() - start_time
    
    # Display results
    print("📊 Results:")
    print("=" * 70)
    print(f"{'Language':<12} {'Status':<8} {'Time (s)':<10} {'Passed':<8} {'Total':<8}")
    print("-" * 70)
    
    for r in sorted(results, key=lambda x: x["language"]):
        lang = r["language"]
        status = "✅ OK" if r["success"] else "❌ FAIL"
        time_taken = f"{r['time']:.2f}"
        
        passed = 0
        total = 0
        if r["success"] and "results" in r.get("result", {}):
            results_data = r["result"]["results"]
            if isinstance(results_data, list):
                for tc_result in results_data:
                    total += 1
                    if tc_result.get("passed", False):
                        passed += 1
            elif isinstance(results_data, dict):
                for tc_result in results_data.values():
                    total += 1
                    if tc_result.get("passed", False):
                        passed += 1
        
        print(f"{lang:<12} {status:<8} {time_taken:<10} {passed:<8} {total:<8}")
        
        if not r["success"]:
            if "error" in r:
                error_msg = r['error'][:100] if len(r['error']) > 100 else r['error']
                print(f"   Error: {error_msg}")
            elif "detail" in r.get("result", {}):
                print(f"   Detail: {r['result']['detail']}")
        elif r["success"]:
            # Show first failure if any
            if "results" in r.get("result", {}):
                results_data = r["result"]["results"]
                if isinstance(results_data, list):
                    for tc in results_data[:1]:  # Show first test case
                        if not tc.get("passed", False):
                            print(f"   First failure: {tc.get('error', 'Unknown error')[:80]}")
                elif isinstance(results_data, dict):
                    for tc_id, tc in list(results_data.items())[:1]:
                        if not tc.get("passed", False):
                            print(f"   First failure: {tc.get('error', 'Unknown error')[:80]}")
    
    print("-" * 70)
    print(f"Total concurrent execution time: {total_time:.2f}s")
    print(f"Languages tested: {len(results)}")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(test_all_languages_concurrently())

