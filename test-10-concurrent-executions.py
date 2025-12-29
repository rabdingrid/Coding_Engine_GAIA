#!/usr/bin/env python3
"""
Test 100 Concurrent Executions
Each request tests the same simple code with 5 test cases
Measures performance, latency, and throughput
"""

import json
import time
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import statistics
import ssl

API_URL = "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io"

# Create SSL context that doesn't verify certificates (for testing)
ssl_context = ssl._create_unverified_context()

# Simple test code - same for all 10 requests (using user's exact format)
TEST_CODE = {
    "language": "python",
    "code": "def solve(n):\n    return n * 2\n\nn = int(input())\nprint(solve(n))",
    "test_cases": [
        {"id": "test_1", "input": "5", "expected_output": "10"},
        {"id": "test_2", "input": "10", "expected_output": "20"},
        {"id": "test_3", "input": "100", "expected_output": "200"},
        {"id": "test_4", "input": "50", "expected_output": "100"},
        {"id": "test_5", "input": "25", "expected_output": "50"}
    ]
}

def execute_request(request_id):
    """Execute a single request to the API"""
    start_time = time.time()
    request_start_timestamp = datetime.utcnow().isoformat()
    
    try:
        data = json.dumps({
            "language": TEST_CODE["language"],
            "code": TEST_CODE["code"],
            "test_cases": TEST_CODE["test_cases"],
            "sample_test_cases": [],
            "user_id": f"user_{request_id}",
            "question_id": f"q{request_id}"
        }).encode('utf-8')
        
        req = urllib.request.Request(
            f"{API_URL}/runall",
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=300, context=ssl_context) as response:
            result = json.loads(response.read().decode('utf-8'))
            end_time = time.time()
            request_end_timestamp = datetime.utcnow().isoformat()
            duration = end_time - start_time
            
            return {
                "request_id": request_id,
                "status": "success",
                "start_time": request_start_timestamp,
                "end_time": request_end_timestamp,
                "total_duration_s": round(duration, 3),
                "total_duration_ms": round(duration * 1000, 2),
                "total_tests": result["summary"]["total_tests"],
                "passed": result["summary"]["passed"],
                "failed": result["summary"]["failed"],
                "all_passed": result["summary"]["all_passed"],
                "pass_percentage": result["summary"]["pass_percentage"],
                "execution_time_ms": result["metadata"]["execution_time_ms"],
                "cpu_usage_percent": result["metadata"]["cpu_usage_percent"],
                "memory_usage_mb": result["metadata"]["memory_usage_mb"],
                "replica": result["metadata"].get("replica", "unknown"),
                "container_id": result["metadata"].get("container_id", "unknown"),
                "error": None
            }
    except urllib.error.HTTPError as e:
        end_time = time.time()
        request_end_timestamp = datetime.utcnow().isoformat()
        duration = end_time - start_time
        error_body = e.read().decode('utf-8')[:200] if e.fp else str(e)
        return {
            "request_id": request_id,
            "status": "error",
            "start_time": request_start_timestamp,
            "end_time": request_end_timestamp,
            "total_duration_s": round(duration, 3),
            "total_duration_ms": round(duration * 1000, 2),
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "all_passed": False,
            "pass_percentage": 0,
            "execution_time_ms": 0,
            "cpu_usage_percent": 0,
            "memory_usage_mb": 0,
            "replica": "N/A",
            "container_id": "N/A",
            "error": f"HTTP {e.code}: {error_body}"
        }
    except Exception as e:
        end_time = time.time()
        request_end_timestamp = datetime.utcnow().isoformat()
        duration = end_time - start_time
        return {
            "request_id": request_id,
            "status": "exception",
            "start_time": request_start_timestamp,
            "end_time": request_end_timestamp,
            "total_duration_s": round(duration, 3),
            "total_duration_ms": round(duration * 1000, 2),
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "all_passed": False,
            "pass_percentage": 0,
            "execution_time_ms": 0,
            "cpu_usage_percent": 0,
            "memory_usage_mb": 0,
            "replica": "N/A",
            "container_id": "N/A",
            "error": str(e)
        }

def generate_markdown_report(results, total_duration, test_start_time, num_requests):
    """Generate a detailed markdown report"""
    successful = [r for r in results if r["status"] == "success"]
    failed = [r for r in results if r["status"] != "success"]
    
    # Calculate statistics
    if successful:
        durations = [r["total_duration_ms"] for r in successful]
        execution_times = [r["execution_time_ms"] for r in successful]
        cpu_usages = [r["cpu_usage_percent"] for r in successful]
        memory_usages = [r["memory_usage_mb"] for r in successful]
        
        avg_duration = statistics.mean(durations)
        min_duration = min(durations)
        max_duration = max(durations)
        std_duration = statistics.stdev(durations) if len(durations) > 1 else 0
        median_duration = statistics.median(durations)
        
        avg_execution = statistics.mean(execution_times)
        avg_cpu = statistics.mean(cpu_usages)
        avg_memory = statistics.mean(memory_usages)
        max_memory = max(memory_usages)
    else:
        avg_duration = min_duration = max_duration = std_duration = median_duration = 0
        avg_execution = avg_cpu = avg_memory = max_memory = 0
    
    # Sort results by request_id for consistent display
    results_sorted = sorted(results, key=lambda x: x["request_id"])
    
    md = f"""# 🚀 {num_requests} Concurrent Execution Performance Test Report

## 📊 Test Overview

**Test Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**API Endpoint:** `{API_URL}/runall`  
**Total Concurrent Requests:** {num_requests}  
**Test Cases per Request:** 5  
**Total Test Cases Executed:** {len(results) * 5}

---

## ⏱️ Performance Summary

### Overall Metrics
- **Total Test Duration:** {round(total_duration, 3)}s ({round(total_duration * 1000, 2)}ms)
- **Successful Requests:** {len(successful)} / {len(results)}
- **Failed Requests:** {len(failed)} / {len(results)}
- **Success Rate:** {round(len(successful) / len(results) * 100, 2)}%

### Response Time Statistics (for successful requests)
- **Average Response Time:** {round(avg_duration, 2)}ms
- **Median Response Time:** {round(median_duration, 2)}ms
- **Minimum Response Time:** {round(min_duration, 2)}ms
- **Maximum Response Time:** {round(max_duration, 2)}ms
- **Standard Deviation:** {round(std_duration, 2)}ms

### Throughput
- **Requests per Second:** {round(len(successful) / total_duration, 2)} req/s
- **Average Test Cases per Second:** {round((len(successful) * 5) / total_duration, 2)} tests/s

### Resource Utilization
- **Average CPU Usage:** {round(avg_cpu, 2)}%
- **Average Memory Usage:** {round(avg_memory, 2)} MB
- **Maximum Memory Usage:** {round(max_memory, 2)} MB
- **Average Execution Time:** {round(avg_execution, 2)}ms

---

## 📋 Detailed Request Results Summary

| Req ID | Status | Duration (ms) | Tests | Passed | Failed | Pass % | Exec Time (ms) | CPU % | Memory (MB) | Replica |
|--------|--------|---------------|-------|--------|--------|--------|----------------|-------|-------------|---------|
"""
    
    # For large number of requests, show first 20, last 20, and summary
    if len(results_sorted) > 50:
        for r in results_sorted[:20]:
            status_icon = "✅" if r["status"] == "success" else "❌"
            md += f"| {r['request_id']} | {status_icon} {r['status']} | {r['total_duration_ms']} | {r['total_tests']} | {r['passed']} | {r['failed']} | {r['pass_percentage']}% | {r['execution_time_ms']} | {r['cpu_usage_percent']} | {r['memory_usage_mb']} | {r['replica']} |\n"
        
        md += f"| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |\n"
        md += f"| *({len(results_sorted) - 40} more requests)* | | | | | | | | | | |\n"
        md += f"| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |\n"
        
        for r in results_sorted[-20:]:
            status_icon = "✅" if r["status"] == "success" else "❌"
            md += f"| {r['request_id']} | {status_icon} {r['status']} | {r['total_duration_ms']} | {r['total_tests']} | {r['passed']} | {r['failed']} | {r['pass_percentage']}% | {r['execution_time_ms']} | {r['cpu_usage_percent']} | {r['memory_usage_mb']} | {r['replica']} |\n"
    else:
        for r in results_sorted:
            status_icon = "✅" if r["status"] == "success" else "❌"
            md += f"| {r['request_id']} | {status_icon} {r['status']} | {r['total_duration_ms']} | {r['total_tests']} | {r['passed']} | {r['failed']} | {r['pass_percentage']}% | {r['execution_time_ms']} | {r['cpu_usage_percent']} | {r['memory_usage_mb']} | {r['replica']} |\n"
    
    md += "\n---\n\n"
    
    # For large number of requests, skip individual details
    if len(results_sorted) <= 20:
        md += "## 🔍 Individual Request Details\n\n"
        for r in results_sorted:
            status_emoji = "✅" if r["status"] == "success" else "❌"
            md += f"### Request #{r['request_id']} {status_emoji}\n\n"
            md += f"- **Status:** {r['status']}\n"
            md += f"- **Start Time:** {r['start_time']}\n"
            md += f"- **End Time:** {r['end_time']}\n"
            md += f"- **Total Duration:** {r['total_duration_ms']}ms ({r['total_duration_s']}s)\n"
            md += f"- **Execution Time:** {r['execution_time_ms']}ms\n"
            md += f"- **Total Tests:** {r['total_tests']}\n"
            md += f"- **Passed:** {r['passed']} ({r['pass_percentage']}%)\n"
            md += f"- **Failed:** {r['failed']}\n"
            md += f"- **All Passed:** {'Yes' if r['all_passed'] else 'No'}\n"
            md += f"- **CPU Usage:** {r['cpu_usage_percent']}%\n"
            md += f"- **Memory Usage:** {r['memory_usage_mb']} MB\n"
            md += f"- **Replica:** {r['replica']}\n"
            md += f"- **Container ID:** {r['container_id']}\n"
            
            if r["error"]:
                md += f"- **Error:** {r['error']}\n"
            
            md += "\n"
        
        md += "---\n\n"
    else:
        md += f"*Individual request details omitted for brevity ({len(results_sorted)} requests). See JSON file for complete data.*\n\n---\n\n"
    
    # Replica distribution
    if successful:
        replicas = {}
        for r in successful:
            replica = r["replica"]
            replicas[replica] = replicas.get(replica, 0) + 1
        
        md += "## 🖥️ Replica Distribution\n\n"
        md += "| Replica | Requests Handled |\n"
        md += "|---------|------------------|\n"
        for replica, count in sorted(replicas.items()):
            md += f"| {replica} | {count} |\n"
        md += "\n---\n\n"
    
    # Error details
    if failed:
        md += "## ❌ Failed Requests Details\n\n"
        for r in failed:
            md += f"### Request #{r['request_id']}\n"
            md += f"- **Error Type:** {r['status']}\n"
            md += f"- **Error Message:** {r['error']}\n"
            md += f"- **Duration:** {r['total_duration_ms']}ms\n"
            md += "\n"
        md += "---\n\n"
    
    # Test configuration
    md += "## ⚙️ Test Configuration\n\n"
    md += "```json\n"
    md += json.dumps({
        "language": TEST_CODE["language"],
        "total_test_cases": len(TEST_CODE["test_cases"]),
        "concurrent_requests": num_requests,
        "api_endpoint": f"{API_URL}/runall",
        "timeout": "300s"
    }, indent=2)
    md += "\n```\n\n"
    
    # Conclusion
    md += "---\n\n"
    md += "## 📝 Conclusion\n\n"
    
    if len(successful) == len(results):
        md += "✅ **All requests completed successfully!**\n\n"
        if avg_duration < 1000:
            md += f"- System is performing well with an average response time of {round(avg_duration, 2)}ms\n"
        elif avg_duration < 3000:
            md += f"- System is performing acceptably with an average response time of {round(avg_duration, 2)}ms\n"
        else:
            md += f"- System response time of {round(avg_duration, 2)}ms may need optimization\n"
        
        if std_duration < avg_duration * 0.2:
            md += "- Response times are consistent (low standard deviation)\n"
        else:
            md += "- Response times show some variance (higher standard deviation)\n"
        
        md += f"- System can handle {round(len(successful) / total_duration, 2)} requests per second\n"
    else:
        md += f"⚠️ **{len(failed)} out of {len(results)} requests failed**\n\n"
        md += "Please review the error details above.\n"
    
    md += "\n---\n\n"
    md += f"**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    
    return md

def main():
    NUM_REQUESTS = 100  # Number of concurrent requests to test
    
    print("=" * 80)
    print(f"🚀 {NUM_REQUESTS} Concurrent Execution Performance Test")
    print("=" * 80)
    print(f"API URL: {API_URL}")
    print(f"Concurrent Requests: {NUM_REQUESTS}")
    print(f"Test Cases per Request: {len(TEST_CODE['test_cases'])}")
    print(f"Total Test Cases: {NUM_REQUESTS * len(TEST_CODE['test_cases'])}")
    print("=" * 80)
    print()
    
    # Test health first
    try:
        print("🔍 Checking service health...")
        req = urllib.request.Request(f"{API_URL}/health", method='GET')
        with urllib.request.urlopen(req, timeout=30, context=ssl_context) as response:
            health = json.loads(response.read().decode('utf-8'))
            print(f"✅ Service is healthy: {health}")
    except Exception as e:
        print(f"⚠️  Health check failed: {e}")
        print("Continuing with test anyway...\n")
    
    print(f"\n📤 Sending {NUM_REQUESTS} concurrent requests...\n")
    
    test_start_time = datetime.utcnow()
    start_time = time.time()
    results = []
    completed_count = 0
    
    # Execute all requests concurrently
    with ThreadPoolExecutor(max_workers=NUM_REQUESTS) as executor:
        futures = {executor.submit(execute_request, i): i for i in range(1, NUM_REQUESTS + 1)}
        
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            completed_count += 1
            status_icon = "✅" if result["status"] == "success" else "❌"
            
            # Print progress every 10 requests or for failures
            if completed_count % 10 == 0 or result["status"] != "success":
                print(f"{status_icon} [{completed_count}/{NUM_REQUESTS}] Request #{result['request_id']}: {result['status']} - "
                      f"{result['total_duration_ms']}ms (Exec: {result['execution_time_ms']}ms, "
                      f"Tests: {result['passed']}/{result['total_tests']})")
    
    end_time = time.time()
    total_duration = end_time - start_time
    
    print("\n" + "=" * 80)
    print("📊 QUICK SUMMARY")
    print("=" * 80)
    
    successful = [r for r in results if r["status"] == "success"]
    failed = [r for r in results if r["status"] != "success"]
    
    print(f"Total Requests: {len(results)}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")
    print(f"Total Duration: {round(total_duration, 3)}s")
    print(f"Average Duration: {round(total_duration / len(results), 3)}s per request")
    
    if successful:
        avg_response = sum(r["total_duration_ms"] for r in successful) / len(successful)
        median_response = statistics.median([r["total_duration_ms"] for r in successful])
        print(f"Average Response Time: {round(avg_response, 2)}ms")
        print(f"Median Response Time: {round(median_response, 2)}ms")
        print(f"Throughput: {round(len(successful) / total_duration, 2)} req/s")
        
        total_tests = sum(r["total_tests"] for r in successful)
        total_passed = sum(r["passed"] for r in successful)
        print(f"Total Test Cases: {total_tests}")
        print(f"Total Passed: {total_passed}")
        print(f"Pass Rate: {round(total_passed / total_tests * 100, 2)}%")
    
    print("=" * 80)
    
    # Generate markdown report
    print("\n📝 Generating detailed markdown report...")
    markdown_report = generate_markdown_report(results, total_duration, test_start_time, NUM_REQUESTS)
    
    # Save markdown report
    report_filename = f"TEST_REPORT_{NUM_REQUESTS}_CONCURRENT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_filename, 'w') as f:
        f.write(markdown_report)
    
    print(f"✅ Detailed report saved to: {report_filename}")
    
    # Save JSON results
    json_filename = f"test_results_{NUM_REQUESTS}_concurrent_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(json_filename, 'w') as f:
        json.dump({
            "test_start_time": test_start_time.isoformat(),
            "total_duration_s": total_duration,
            "total_requests": len(results),
            "successful_requests": len(successful),
            "failed_requests": len(failed),
            "results": results
        }, f, indent=2)
    
    print(f"✅ JSON results saved to: {json_filename}")
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()

