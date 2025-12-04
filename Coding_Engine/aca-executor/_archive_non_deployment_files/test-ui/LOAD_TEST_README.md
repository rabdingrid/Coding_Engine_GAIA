# Load Testing Script: Multiple Users with Real DSA Questions

## 📋 Overview

This script simulates multiple concurrent users submitting real DSA questions to test:
- **Queue handling** with 1 replica (min)
- **Auto-scaling** behavior (scales to max 3 replicas)
- **Performance metrics** per user (CPU, memory, execution time)
- **Container distribution** (which replica handled which request)
- **Overall system capacity**

## 🚀 Quick Start

### Prerequisites

1. **Test UI server running** on `http://localhost:3001`
   ```bash
   cd test-ui
   npm start
   ```

2. **Python 3** with `requests` module
   ```bash
   pip3 install requests
   ```

3. **Azure CLI** logged in (for auto-detecting executor URL)

### Basic Usage

```bash
# Run with default settings (30 users, Python)
python3 load-test-multi-user.py

# Or use the wrapper script
./run-load-test.sh
```

### Advanced Usage

```bash
# Test with 50 users
python3 load-test-multi-user.py -n 50

# Test with Java
python3 load-test-multi-user.py -n 30 -l java

# Test with all languages (rotates through)
python3 load-test-multi-user.py -n 40 -l all

# Specify executor URL manually
python3 load-test-multi-user.py -n 30 --executor-url https://your-executor-url.com

# Use different test UI URL
python3 load-test-multi-user.py -n 30 --test-ui-url http://localhost:3000
```

## 📊 What It Tests

### 1. **Concurrent Request Handling**
- Simulates multiple users submitting code simultaneously
- Tests queue system with Gunicorn (4 workers × 2 threads = 8 concurrent per replica)

### 2. **Auto-Scaling**
- Monitors replica count before and after test
- Verifies replicas scale from 1 (min) to 3 (max) under load

### 3. **Performance Metrics**
For each user, tracks:
- **Container ID**: Which replica handled the request
- **CPU Usage**: Percentage CPU used during execution
- **Memory Usage**: Memory consumed in MB
- **Execution Time**: Time taken in milliseconds
- **Test Results**: Pass/fail status for each test case

### 4. **Real DSA Questions**
- Fetches questions from database via Test UI API
- Uses actual test cases from questions
- Supports multiple languages (Python, Java, JavaScript, C++)

## 📈 Output

The script provides:

### 1. **Real-time Progress**
```
⚡ Executing 30 concurrent requests...
   [5/30] load_test_user_5: ✅ success (1234ms, CPU: 45.2%)
   [10/30] load_test_user_10: ✅ success (987ms, CPU: 38.1%)
   ...
```

### 2. **Summary Statistics**
```
📊 LOAD TEST RESULTS SUMMARY
==========================================
🎯 Overall Statistics:
   Total Users: 30
   Successful Requests: 30 (100.0%)
   Failed Requests: 0 (0.0%)
   All Tests Passed: 30 (100.0%)
   Total Duration: 45.23s
   Average Duration per User: 1.51s

⚡ Performance Metrics:
   Average Execution Time: 1234.56ms
   Average CPU Usage: 42.3%
   Average Memory Usage: 38.5MB
   Min Execution Time: 456.78ms
   Max Execution Time: 2345.67ms

📦 Container Distribution:
   Unique Containers Used: 3
   container-1: 12 requests | Avg CPU: 45.2% | Avg Mem: 40.1MB
   container-2: 10 requests | Avg CPU: 38.5% | Avg Mem: 35.2MB
   container-3: 8 requests | Avg CPU: 41.3% | Avg Mem: 39.8MB
```

### 3. **Detailed User Results**
```
👥 DETAILED USER RESULTS
==========================================
User ID              Question                  Lang     Status    Time(ms)   CPU%     Mem(MB)   Container                      Tests    
----------------------------------------------------------------------------------------------------
load_test_user_1    Two Sum                    python   ✅ success 1234      45.2     38.5      container-1...                 2/2      
load_test_user_2    Climbing Stairs            java     ✅ success 2345      67.8     45.2      container-2...                 3/3      
...
```

### 4. **Replica Scaling Info**
```
📈 REPLICA SCALING
==========================================
   Initial Replicas: 1
   Final Replicas: 3
   ✅ Replicas scaled from 1 to 3
```

### 5. **JSON Output File**
Results are saved to `load_test_results_YYYYMMDD_HHMMSS.json` with full details.

## 🎯 Expected Behavior

### With 1 Replica (Min)
- **Capacity**: 8 concurrent requests (4 workers × 2 threads)
- **Behavior**: Requests beyond 8 will be queued
- **Performance**: Should handle 30 users, but may take longer

### With Auto-Scaling (1 → 3 Replicas)
- **Initial**: 1 replica (8 concurrent capacity)
- **Under Load**: Scales to 2-3 replicas (16-24 concurrent capacity)
- **Performance**: Should handle 30 users efficiently

### Metrics to Watch
- **Execution Time**: Should be consistent (500ms - 2s per execution)
- **CPU Usage**: Should be reasonable (30-70% per execution)
- **Memory Usage**: Should be stable (30-50MB per execution)
- **Container Distribution**: Should be balanced across replicas

## 🔧 Configuration

### Number of Users
- **Small Test**: 10-20 users (tests single replica)
- **Medium Test**: 30-50 users (tests auto-scaling)
- **Large Test**: 50-100 users (tests max capacity)

### Languages
- **python**: Most common, fastest execution
- **java**: Slower startup, higher memory
- **javascript**: Fast execution
- **cpp**: Fast execution, compilation overhead

## 📝 Example Scenarios

### Scenario 1: Test Single Replica Capacity
```bash
# Set min_replicas = 1, max_replicas = 1
python3 load-test-multi-user.py -n 20 -l python
# Expected: All requests handled by 1 replica, may see queuing
```

### Scenario 2: Test Auto-Scaling
```bash
# Set min_replicas = 1, max_replicas = 3
python3 load-test-multi-user.py -n 30 -l python
# Expected: Replicas scale from 1 to 2-3, balanced distribution
```

### Scenario 3: Test High Load
```bash
# Set min_replicas = 1, max_replicas = 3
python3 load-test-multi-user.py -n 50 -l python
# Expected: All 3 replicas used, may see some queuing
```

## 🐛 Troubleshooting

### Issue: "Could not fetch executor URL"
**Solution**: Provide executor URL manually
```bash
python3 load-test-multi-user.py --executor-url https://your-executor-url.com
```

### Issue: "Could not fetch questions"
**Solution**: Make sure Test UI server is running
```bash
cd test-ui
npm start
# Then run load test in another terminal
```

### Issue: "Request timeout"
**Solution**: Increase timeout or reduce number of users
```bash
# Reduce users
python3 load-test-multi-user.py -n 20
```

### Issue: "No code solution available"
**Solution**: The script has default solutions, but you can add more in the `SOLUTIONS` dictionary in the script.

## 📊 Interpreting Results

### Good Results ✅
- All requests successful (100% success rate)
- All tests passed
- Execution times consistent (500ms - 2s)
- CPU usage reasonable (30-70%)
- Memory usage stable (30-50MB)
- Replicas scaled appropriately

### Warning Signs ⚠️
- Some requests failed
- High execution times (>5s)
- Very high CPU usage (>90%)
- Memory spikes (>100MB)
- Replicas didn't scale when needed

### Critical Issues ❌
- Many requests failed (>10%)
- Timeouts
- Replicas not scaling
- Container crashes

## 🔍 Monitoring During Test

You can monitor replicas in real-time:
```bash
# Watch replica count
watch -n 2 'az containerapp show --name ai-ta-ra-code-executor2 --resource-group ai-ta-2 --query "properties.template.scale.minReplicas" -o tsv'

# Or check Azure Portal
# Container Apps → ai-ta-ra-code-executor2 → Scale
```

## 📚 Related Files

- `load-test-multi-user.py`: Main load testing script
- `run-load-test.sh`: Wrapper script for easy execution
- `test-50-users-load.sh`: Bash-based load test (simpler)
- `test-10-users-1-replica.sh`: Single replica test

## 🎯 Next Steps

After running the load test:
1. Review the summary statistics
2. Check container distribution (should be balanced)
3. Verify replica scaling worked
4. Review any errors or timeouts
5. Adjust replica limits if needed
6. Run again with different parameters

---

**Happy Load Testing!** 🚀

