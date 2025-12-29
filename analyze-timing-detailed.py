#!/usr/bin/env python3
"""
Analyze timing breakdown from the curl response
"""

import json
import sys
from datetime import datetime

def analyze_timing(response_file='/tmp/curl_response.json'):
    """Analyze timing from the API response"""
    
    try:
        with open(response_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Response file not found: {response_file}")
        return
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return
    
    print("=" * 80)
    print("📊 DETAILED TIMING ANALYSIS - C++ Code Execution (17 Test Cases)")
    print("=" * 80)
    
    # Overall metadata
    metadata = data.get('metadata', {})
    execution_time_ms = metadata.get('execution_time_ms', 0)
    total_tests = data.get('summary', {}).get('total_tests', 0)
    passed = data.get('summary', {}).get('passed', 0)
    failed = data.get('summary', {}).get('failed', 0)
    
    print(f"\n📈 OVERALL SUMMARY")
    print(f"   Total Test Cases: {total_tests}")
    print(f"   Passed: {passed}")
    print(f"   Failed: {failed}")
    print(f"   Total Execution Time: {execution_time_ms}ms ({execution_time_ms/1000:.2f}s)")
    print(f"   Average per Test Case: {execution_time_ms/total_tests:.1f}ms" if total_tests > 0 else "")
    
    # Individual test case timing
    test_results = data.get('test_results', [])
    
    print(f"\n📋 INDIVIDUAL TEST CASE TIMING BREAKDOWN")
    print("-" * 80)
    print(f"{'Test ID':<20} {'Status':<10} {'Time (ms)':<12} {'CPU %':<10} {'Memory (MB)':<12}")
    print("-" * 80)
    
    total_execution_time = 0
    execution_times = []
    
    for test in test_results:
        test_id = test.get('test_case_id', 'unknown')
        status = test.get('status', 'unknown')
        exec_time = test.get('execution_time_ms', 0)
        cpu = test.get('cpu_usage_percent', 0)
        memory_bytes = test.get('memory_usage_bytes', 0)
        memory_mb = memory_bytes / (1024 * 1024) if memory_bytes else 0
        
        total_execution_time += exec_time
        execution_times.append(exec_time)
        
        status_icon = "✅" if status == "passed" else "❌"
        print(f"{test_id:<20} {status_icon} {status:<8} {exec_time:<12} {cpu:<10.1f} {memory_mb:<12.2f}")
    
    print("-" * 80)
    
    # Statistics
    if execution_times:
        execution_times.sort()
        min_time = execution_times[0]
        max_time = execution_times[-1]
        avg_time = sum(execution_times) / len(execution_times)
        median_time = execution_times[len(execution_times) // 2]
        
        print(f"\n📊 TIMING STATISTICS")
        print(f"   Minimum: {min_time}ms")
        print(f"   Maximum: {max_time}ms")
        print(f"   Average: {avg_time:.1f}ms")
        print(f"   Median: {median_time}ms")
        print(f"   Total Execution: {total_execution_time}ms ({total_execution_time/1000:.2f}s)")
    
    # Network vs Execution breakdown
    print(f"\n🌐 NETWORK vs EXECUTION BREAKDOWN")
    print(f"   Total Request Time: ~24.57s (from curl)")
    print(f"   Server Execution Time: {execution_time_ms}ms ({execution_time_ms/1000:.2f}s)")
    print(f"   Network Overhead: ~{24574 - execution_time_ms}ms (~{(24574 - execution_time_ms)/1000:.2f}s)")
    print(f"   Network Overhead %: {((24574 - execution_time_ms) / 24574 * 100):.1f}%")
    
    # Performance insights
    print(f"\n💡 PERFORMANCE INSIGHTS")
    if execution_time_ms < 5000:
        print("   ✅ Excellent: Execution time < 5s")
    elif execution_time_ms < 10000:
        print("   ✅ Good: Execution time < 10s")
    elif execution_time_ms < 20000:
        print("   ⚠️  Moderate: Execution time < 20s")
    else:
        print("   ⚠️  Slow: Execution time > 20s")
    
    if total_tests > 0:
        avg_per_test = execution_time_ms / total_tests
        if avg_per_test < 500:
            print(f"   ✅ Fast per test: {avg_per_test:.1f}ms average")
        elif avg_per_test < 1000:
            print(f"   ✅ Moderate per test: {avg_per_test:.1f}ms average")
        else:
            print(f"   ⚠️  Slow per test: {avg_per_test:.1f}ms average")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    analyze_timing()


