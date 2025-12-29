#!/usr/bin/env python3
"""
Optimized Warehouse Boxes Test - Request Body Splitting Implementation
Demonstrates how to split test cases into batches for faster execution
"""

import json
import time
import urllib.request
import urllib.parse
import ssl
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

API_URL = "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io/runall"
ssl_context = ssl._create_unverified_context()

# Solution code
SOLUTION_CODE = """def findTotalWeight(boxes):
    total = 0
    while boxes:
        min_weight = min(boxes)
        min_idx = boxes.index(min_weight)
        start = max(0, min_idx - 1)
        end = min(len(boxes), min_idx + 2)
        total += min_weight
        boxes = boxes[:start] + boxes[end:]
    return total

n = int(input())
boxes = [int(input()) for _ in range(n)]
result = findTotalWeight(boxes)
print(result)"""

def execute_batch(test_cases_batch, batch_id, user_id="warehouse_user"):
    """Execute a batch of test cases"""
    start_time = time.time()
    
    try:
        data = json.dumps({
            "language": "python",
            "code": SOLUTION_CODE,
            "test_cases": test_cases_batch,
            "sample_test_cases": [],
            "user_id": f"{user_id}_batch_{batch_id}",
            "question_id": "warehouse_boxes"
        }).encode('utf-8')
        
        req = urllib.request.Request(
            f"{API_URL}/runall",
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=600, context=ssl_context) as response:
            result = json.loads(response.read().decode('utf-8'))
            duration = (time.time() - start_time) * 1000
            
            return {
                'batch_id': batch_id,
                'status': 'success',
                'duration_ms': duration,
                'test_count': len(test_cases_batch),
                'passed': result['summary']['passed'],
                'failed': result['summary']['failed'],
                'execution_time_ms': result['metadata']['execution_time_ms'],
                'result': result
            }
    except Exception as e:
        duration = (time.time() - start_time) * 1000
        return {
            'batch_id': batch_id,
            'status': 'error',
            'duration_ms': duration,
            'test_count': len(test_cases_batch),
            'error': str(e)
        }

def optimized_execution(all_test_cases, batch_size=5, max_workers=5):
    """
    Split test cases into batches and execute in parallel
    
    Args:
        all_test_cases: List of all test cases
        batch_size: Number of test cases per batch (default: 5)
        max_workers: Maximum parallel requests (default: 5)
    
    Returns:
        tuple: (results, total_time_ms, summary)
    """
    print("="*80)
    print("🚀 Optimized Execution - Request Body Splitting")
    print("="*80)
    
    start_time = time.time()
    
    # Calculate optimal batch size if not provided
    if batch_size is None:
        if len(all_test_cases) <= 10:
            batch_size = 3
        elif len(all_test_cases) <= 30:
            batch_size = 5
        elif len(all_test_cases) <= 100:
            batch_size = 10
        else:
            batch_size = 15
    
    # Split into batches
    batches = [
        all_test_cases[i:i+batch_size] 
        for i in range(0, len(all_test_cases), batch_size)
    ]
    
    print(f"\n📦 Configuration:")
    print(f"   Total Test Cases: {len(all_test_cases)}")
    print(f"   Batch Size: {batch_size} test cases per batch")
    print(f"   Number of Batches: {len(batches)}")
    print(f"   Max Parallel Requests: {max_workers}")
    
    # Execute batches in parallel
    print(f"\n📤 Executing batches in parallel...\n")
    
    results = []
    with ThreadPoolExecutor(max_workers=min(len(batches), max_workers)) as executor:
        futures = {
            executor.submit(execute_batch, batch, i): i 
            for i, batch in enumerate(batches)
        }
        
        for future in as_completed(futures):
            batch_id = futures[future]
            result = future.result()
            results.append(result)
            
            status_icon = "✅" if result['status'] == 'success' else "❌"
            print(f"{status_icon} Batch {batch_id+1}/{len(batches)}: "
                  f"{result['duration_ms']:.2f}ms "
                  f"({result['test_count']} tests, "
                  f"{result.get('passed', 0)} passed)")
    
    total_time = (time.time() - start_time) * 1000
    
    # Sort results by batch_id
    results.sort(key=lambda x: x['batch_id'])
    
    # Aggregate summary
    total_passed = sum(r.get('passed', 0) for r in results if r['status'] == 'success')
    total_failed = sum(r.get('failed', 0) for r in results if r['status'] == 'success')
    total_tests = len(all_test_cases)
    
    # Calculate statistics
    successful_batches = [r for r in results if r['status'] == 'success']
    avg_batch_time = sum(r['duration_ms'] for r in successful_batches) / len(successful_batches) if successful_batches else 0
    max_batch_time = max((r['duration_ms'] for r in successful_batches), default=0)
    
    print(f"\n{'='*80}")
    print("📊 Results Summary")
    print(f"{'='*80}")
    print(f"Total Time: {total_time:.2f}ms ({total_time/1000:.2f}s)")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_failed}")
    print(f"Success Rate: {total_passed/total_tests*100:.1f}%")
    print(f"\nBatch Performance:")
    print(f"  Average Batch Time: {avg_batch_time:.2f}ms")
    print(f"  Longest Batch Time: {max_batch_time:.2f}ms")
    print(f"  Number of Batches: {len(batches)}")
    print(f"{'='*80}\n")
    
    summary = {
        'total_time_ms': total_time,
        'total_tests': total_tests,
        'passed': total_passed,
        'failed': total_failed,
        'batches': len(batches),
        'avg_batch_time_ms': avg_batch_time,
        'max_batch_time_ms': max_batch_time
    }
    
    return results, total_time, summary

def compare_with_single_request(all_test_cases):
    """Compare optimized vs single request approach"""
    print("\n" + "="*80)
    print("⚖️  Performance Comparison")
    print("="*80)
    
    # Single request
    print("\n📤 Testing Single Request Approach...")
    single_start = time.time()
    single_result = execute_batch(all_test_cases, 0, "single_request")
    single_time = (time.time() - single_start) * 1000
    
    print(f"✅ Single Request: {single_time:.2f}ms")
    
    # Optimized (split)
    print("\n📤 Testing Optimized (Split) Approach...")
    _, optimized_time, _ = optimized_execution(all_test_cases, batch_size=5)
    
    # Comparison
    improvement = single_time / optimized_time
    time_saved = single_time - optimized_time
    
    print(f"\n{'='*80}")
    print("📈 Comparison Results")
    print(f"{'='*80}")
    print(f"Single Request:    {single_time:.2f}ms")
    print(f"Optimized (Split): {optimized_time:.2f}ms")
    print(f"Improvement:       {improvement:.2f}x faster ⚡")
    print(f"Time Saved:        {time_saved:.2f}ms ({time_saved/1000:.2f}s)")
    print(f"{'='*80}\n")

# Example usage
if __name__ == "__main__":
    # Example test cases
    test_cases = [
        {"id": "test_1", "input": "7\n6\n4\n9\n10\n34\n56\n54", "expected_output": "68"},
        {"id": "test_2", "input": "8\n132\n45\n65\n765\n345\n243\n75\n67", "expected_output": "1120"},
        {"id": "test_3", "input": "60\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12", "expected_output": "309"},
        {"id": "test_4", "input": "100\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9", "expected_output": "116"},
        {"id": "test_5", "input": "60\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12", "expected_output": "309"},
        {"id": "test_6", "input": "71\n3\n5\n45\n3\n34\n34\n34\n43\n5\n5\n65\n2\n3\n43\n5\n2\n3\n5\n45\n3\n34\n34\n34\n43\n5\n5\n65\n2\n3\n43\n5\n2\n3\n5\n45\n3\n34\n34\n34\n42\n3\n43\n5\n2\n3\n5\n45\n3\n34\n34\n34\n43\n5\n5\n65\n2\n3\n43\n5\n2\n3\n5\n45\n3\n34\n34\n34\n43\n5\n5\n65", "expected_output": "177"},
        {"id": "test_7", "input": "100\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n2\n3\n4\n5\n6\n7\n8\n9\n5\n6\n7\n8\n9\n1\n2\n3\n4\n5\n5\n6\n7\n8\n9\n1\n2\n3\n4\n5\n6\n7\n8\n9\n5\n6\n7\n8\n9\n1\n2\n3\n4\n5\n5\n6\n7\n8\n9\n1\n2\n3\n4\n5\n6\n7\n8\n9\n5\n6\n7\n8\n9\n1\n2\n3\n4\n5\n5\n6\n7\n8\n9\n1\n2\n3\n4\n5\n6\n7\n8\n9\n5\n6\n7\n8\n9\n1\n2\n3\n4\n5", "expected_output": "126"},
    ]
    
    # Run optimized execution
    results, total_time, summary = optimized_execution(test_cases, batch_size=3)
    
    # Optional: Compare with single request
    # compare_with_single_request(test_cases)



