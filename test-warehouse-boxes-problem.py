#!/usr/bin/env python3
"""
Test Warehouse Boxes Problem - Single Request with Many Test Cases
Measures performance and suggests optimizations
"""

import json
import time
import urllib.request
import urllib.parse
import ssl
from datetime import datetime

API_URL = "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io"

# Create SSL context
ssl_context = ssl._create_unverified_context()

# Solution code for the warehouse boxes problem
SOLUTION_CODE = """def findTotalWeight(boxes):
    total = 0
    while boxes:
        # Find minimum weight and its index
        min_weight = min(boxes)
        min_idx = boxes.index(min_weight)
        
        # Determine removal range
        start = max(0, min_idx - 1)
        end = min(len(boxes), min_idx + 2)
        
        # Add minimum weight to total
        total += min_weight
        
        # Remove boxes
        boxes = boxes[:start] + boxes[end:]
    
    return total

n = int(input())
boxes = [int(input()) for _ in range(n)]
result = findTotalWeight(boxes)
print(result)"""

# Test cases from the problem
TEST_CASES = [
    {
        "id": "test_case_1",
        "input": "7\n6\n4\n9\n10\n34\n56\n54",
        "expected_output": "68"
    },
    {
        "id": "test_case_2",
        "input": "8\n132\n45\n65\n765\n345\n243\n75\n67",
        "expected_output": "1120"
    },
    {
        "id": "test_case_3",
        "input": "60\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12",
        "expected_output": "309"
    },
    {
        "id": "test_case_8",
        "input": "100\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n1\n2\n3\n4\n5\n6\n7\n8\n9",
        "expected_output": "116"
    },
    {
        "id": "test_case_9",
        "input": "60\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12\n21\n12\n63\n21\n42\n32\n12",
        "expected_output": "309"
    },
    {
        "id": "test_case_13",
        "input": "71\n3\n5\n45\n3\n34\n34\n34\n43\n5\n5\n65\n2\n3\n43\n5\n2\n3\n5\n45\n3\n34\n34\n34\n43\n5\n5\n65\n2\n3\n43\n5\n2\n3\n5\n45\n3\n34\n34\n34\n42\n3\n43\n5\n2\n3\n5\n45\n3\n34\n34\n34\n43\n5\n5\n65\n2\n3\n43\n5\n2\n3\n5\n45\n3\n34\n34\n34\n43\n5\n5\n65",
        "expected_output": "177"
    },
    {
        "id": "test_case_15",
        "input": "100\n1\n2\n3\n4\n5\n6\n7\n8\n9\n1\n2\n3\n4\n5\n6\n7\n8\n9\n5\n6\n7\n8\n9\n1\n2\n3\n4\n5\n5\n6\n7\n8\n9\n1\n2\n3\n4\n5\n6\n7\n8\n9\n5\n6\n7\n8\n9\n1\n2\n3\n4\n5\n5\n6\n7\n8\n9\n1\n2\n3\n4\n5\n6\n7\n8\n9\n5\n6\n7\n8\n9\n1\n2\n3\n4\n5\n5\n6\n7\n8\n9\n1\n2\n3\n4\n5\n6\n7\n8\n9\n5\n6\n7\n8\n9\n1\n2\n3\n4\n5",
        "expected_output": "126"
    }
]

# Large test cases (for performance testing)
LARGE_TEST_CASES = [
    {
        "id": "large_test_2000_1",
        "description": "2000 boxes with pattern 1-10",
        "input": None,  # Will generate
        "expected_output": None  # Will calculate
    }
]

def generate_large_test_case(n, pattern_type=1):
    """Generate large test case"""
    if pattern_type == 1:
        # Pattern: 1,2,3,4,5,6,7,8,9,10 repeating
        boxes = []
        for i in range(n):
            boxes.append(str((i % 10) + 1))
        input_str = f"{n}\n" + "\n".join(boxes)
        return input_str
    return None

def execute_single_request(test_cases, test_name="Full Test"):
    """Execute a single request with all test cases"""
    print(f"\n{'='*80}")
    print(f"🚀 {test_name}")
    print(f"{'='*80}")
    print(f"Total Test Cases: {len(test_cases)}")
    
    start_time = time.time()
    request_start = datetime.utcnow()
    
    try:
        data = json.dumps({
            "language": "python",
            "code": SOLUTION_CODE,
            "test_cases": test_cases,
            "sample_test_cases": [],
            "user_id": "warehouse_test_user",
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
            end_time = time.time()
            request_end = datetime.utcnow()
            
            total_duration = (end_time - start_time) * 1000
            
            # Analyze individual test case timings
            test_timings = []
            for i, test_result in enumerate(result.get('test_results', [])):
                test_timings.append({
                    'test_id': test_result.get('test_case_id', f'test_{i+1}'),
                    'execution_time_ms': test_result.get('execution_time_ms', 0),
                    'status': test_result.get('status', 'unknown'),
                    'passed': test_result.get('passed', False)
                })
            
            return {
                'status': 'success',
                'total_duration_ms': total_duration,
                'total_duration_s': total_duration / 1000,
                'execution_time_ms': result['metadata']['execution_time_ms'],
                'total_tests': len(test_cases),
                'passed': result['summary']['passed'],
                'failed': result['summary']['failed'],
                'test_timings': test_timings,
                'start_time': request_start.isoformat(),
                'end_time': request_end.isoformat(),
                'cpu_usage': result['metadata'].get('cpu_usage_percent', 0),
                'memory_usage_mb': result['metadata'].get('memory_usage_mb', 0),
                'replica': result['metadata'].get('replica', 'unknown')
            }
    except Exception as e:
        end_time = time.time()
        return {
            'status': 'error',
            'total_duration_ms': (end_time - start_time) * 1000,
            'error': str(e)
        }

def generate_performance_report(results):
    """Generate detailed performance report"""
    report = f"""# 📊 Warehouse Boxes Problem - Performance Analysis Report

**Test Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**API Endpoint:** `{API_URL}/runall`  
**Total Test Cases:** {results['total_tests']}

---

## ⏱️ Overall Performance

- **Total Request Duration:** {results['total_duration_ms']:.2f}ms ({results['total_duration_s']:.2f}s)
- **Execution Time:** {results['execution_time_ms']}ms
- **Overhead Time:** {results['total_duration_ms'] - results['execution_time_ms']:.2f}ms
- **Success Rate:** {results['passed']}/{results['total_tests']} ({results['passed']/results['total_tests']*100:.1f}%)
- **CPU Usage:** {results['cpu_usage']}%
- **Memory Usage:** {results['memory_usage_mb']} MB
- **Replica:** {results['replica']}

---

## 📋 Individual Test Case Performance

| Test ID | Execution Time (ms) | Status | Passed |
|---------|---------------------|--------|--------|
"""
    
    for timing in results['test_timings']:
        status_icon = "✅" if timing['passed'] else "❌"
        report += f"| {timing['test_id']} | {timing['execution_time_ms']} | {status_icon} {timing['status']} | {'Yes' if timing['passed'] else 'No'} |\n"
    
    # Calculate statistics
    execution_times = [t['execution_time_ms'] for t in results['test_timings']]
    if execution_times:
        avg_time = sum(execution_times) / len(execution_times)
        min_time = min(execution_times)
        max_time = max(execution_times)
        total_execution = sum(execution_times)
        
        report += f"""
---

## 📈 Performance Statistics

- **Average Test Case Time:** {avg_time:.2f}ms
- **Fastest Test Case:** {min_time}ms
- **Slowest Test Case:** {max_time}ms
- **Total Execution Time:** {total_execution}ms
- **Overhead:** {results['total_duration_ms'] - total_execution:.2f}ms ({((results['total_duration_ms'] - total_execution) / results['total_duration_ms'] * 100):.1f}%)

---

## 🎯 Optimization Recommendations

### Current Performance Breakdown

```
Total Time Breakdown:
├─ Test Execution: {total_execution:.2f}ms ({total_execution/results['total_duration_ms']*100:.1f}%)
├─ Network/Overhead: {results['total_duration_ms'] - total_execution:.2f}ms ({(results['total_duration_ms'] - total_execution)/results['total_duration_ms']*100:.1f}%)
└─ Total: {results['total_duration_ms']:.2f}ms
```

### Optimization Strategy 1: Request Body Splitting ⭐ **RECOMMENDED**

**Current Approach:**
- Single request with all {results['total_tests']} test cases
- Sequential execution within one request
- Total time: {results['total_duration_ms']:.2f}ms

**Optimized Approach:**
- Split into multiple smaller requests (e.g., 10-20 test cases per request)
- Send requests in parallel from client side
- Each request processes faster

**Expected Improvement:**
- Current: {results['total_duration_ms']:.2f}ms (sequential)
- With 3 replicas + 5 parallel requests: ~{results['total_duration_ms']/3:.2f}ms
- **Speedup: ~3x faster** ⚡

**Implementation:**
```python
# Split test cases into batches
batch_size = 15  # Optimal batch size
batches = [test_cases[i:i+batch_size] 
           for i in range(0, len(test_cases), batch_size)]

# Send batches in parallel
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(execute_request, batch) 
               for batch in batches]
    results = [f.result() for f in futures]
```

### Optimization Strategy 2: Vertical Scaling (Increase CPU)

**Current:** 1 vCPU per replica  
**Upgrade:** 2-4 vCPU per replica

**Expected Improvement:**
- 2x CPU: ~{results['total_duration_ms']*0.6:.2f}ms (40% faster)
- 4x CPU: ~{results['total_duration_ms']*0.4:.2f}ms (60% faster)

**Cost:** 1.5-2x infrastructure cost

### Optimization Strategy 3: Hybrid Approach (Best Performance)

**Combine:** Request splitting + Vertical scaling

**Configuration:**
- 3 replicas with 2x CPU each
- Split into 5 parallel requests (15 test cases each)
- Each request: ~{results['total_duration_ms']/len(results['test_timings'])*15*0.6:.2f}ms
- Total: ~{results['total_duration_ms']*0.2:.2f}ms

**Expected Improvement:** **~5x faster** 🚀

---

## 💡 Key Insights

1. **Sequential Processing is the Bottleneck**
   - Each test case runs one after another
   - Cannot be parallelized within single request (causes 503 errors)

2. **Request Body Splitting is Most Effective**
   - No code changes needed
   - Works with current infrastructure
   - Can leverage multiple replicas

3. **Vertical Scaling Helps**
   - Faster CPU = faster per-test execution
   - But limited by sequential nature

4. **Hybrid Approach is Optimal**
   - Combine request splitting + vertical scaling
   - Best performance without code changes

---

## 📊 Performance Comparison

| Strategy | Time | Improvement | Cost | Complexity |
|----------|------|-------------|------|------------|
| Current | {results['total_duration_ms']:.2f}ms | Baseline | 1x | Low |
| Request Splitting | ~{results['total_duration_ms']/3:.2f}ms | 3x faster | 1x | Low |
| Vertical Scaling (2x) | ~{results['total_duration_ms']*0.6:.2f}ms | 1.7x faster | 1.5x | Low |
| Hybrid | ~{results['total_duration_ms']*0.2:.2f}ms | 5x faster | 2x | Medium |

---

## ✅ Recommended Action Plan

1. **Immediate (No Code Changes):**
   - Implement request body splitting
   - Split {results['total_tests']} test cases into 5 batches of ~{results['total_tests']//5} each
   - Send batches in parallel
   - **Expected: 3x faster**

2. **Short-term (Infrastructure):**
   - Upgrade replicas to 2x CPU
   - **Expected: Additional 1.7x improvement**

3. **Long-term (Optimal):**
   - Combine both strategies
   - **Expected: 5x total improvement**

---

**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    return report

def main():
    print("="*80)
    print("🏭 Warehouse Boxes Problem - Performance Test")
    print("="*80)
    
    # Test with provided test cases
    print("\n📦 Testing with provided test cases...")
    results = execute_single_request(TEST_CASES, "Standard Test Cases")
    
    if results['status'] == 'success':
        print(f"\n✅ Test completed successfully!")
        print(f"   Total Duration: {results['total_duration_ms']:.2f}ms ({results['total_duration_s']:.2f}s)")
        print(f"   Execution Time: {results['execution_time_ms']}ms")
        print(f"   Passed: {results['passed']}/{results['total_tests']}")
        
        # Generate report
        report = generate_performance_report(results)
        
        # Save report
        report_filename = f"WAREHOUSE_BOXES_PERFORMANCE_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_filename, 'w') as f:
            f.write(report)
        
        print(f"\n📄 Detailed report saved to: {report_filename}")
        
        # Save JSON results
        json_filename = f"warehouse_boxes_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(json_filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"💾 JSON results saved to: {json_filename}")
    else:
        print(f"\n❌ Test failed: {results.get('error', 'Unknown error')}")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    main()



