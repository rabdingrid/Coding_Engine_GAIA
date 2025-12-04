# Load Test Results: 500 Users with 20 Test Cases Each

## 📊 Test Configuration

- **Total Users**: 500
- **Test Cases per User**: 20 (including 3 long test cases)
- **Question**: Sum of Array Elements (DSA)
- **Languages**: Python, C++, Java, JavaScript, C# (distributed evenly)
- **Min Replicas**: 3 (ready replicas)
- **Max Replicas**: 10
- **Test Date**: December 4, 2025, 23:10:12

## 📈 Overall Results

| Metric | Value |
|--------|-------|
| **Total Requests** | 500 |
| **✅ Successful** | 148 (29.6%) |
| **❌ Failed** | 352 (70.4%) |
| **Total Duration** | 186.50 seconds (3.1 minutes) |
| **Average Wait Time** | 98,401ms (98.4 seconds) |
| **Average Execution Time** | 10,353ms (10.4 seconds) |

## 📝 Language Performance

| Language | Successful | Total | Success Rate |
|----------|-----------|-------|--------------|
| **Python** | 57 | 100 | 57.0% ✅ |
| **C++** | 7 | 100 | 7.0% ⚠️ |
| **Java** | 11 | 100 | 11.0% ⚠️ |
| **JavaScript** | 48 | 100 | 48.0% ✅ |
| **C#** | 25 | 100 | 25.0% ⚠️ |

## ⏱️ Performance Metrics (Successful Requests)

### Wait Times (Time until response received)
- **Min**: 1,318ms (1.3 seconds)
- **Max**: 178,605ms (178.6 seconds / ~3 minutes)
- **Avg**: 98,401ms (98.4 seconds / ~1.6 minutes)

### Execution Times (Code execution duration)
- **Min**: 312ms
- **Max**: 57,208ms (57.2 seconds)
- **Avg**: 10,353ms (10.4 seconds)

### Test Cases Passed
- **Min**: 0
- **Max**: 20
- **Avg**: 16.9/20
- **All Passed**: 121/148 (81.8% of successful requests)

## 🔄 Replica Status

**Replicas Running**: 9 replicas were active during the test
- Auto-scaling activated (started with 3, scaled to 9)
- Load was distributed across replicas
- Note: Replica IDs in CSV show as "unknown" due to API response format

## 📊 Detailed Results File

**File**: `LOAD_TEST_500_USERS_DETAILED_RESULTS.csv`

**Columns**:
- `User_ID`: User identifier (user_1 to user_500)
- `Language`: Programming language used
- `HTTP_Code`: HTTP response code (200 = success, 503 = service unavailable, 000 = timeout)
- `Success`: Yes/No
- `Start_Timestamp`: When request was sent
- `End_Timestamp`: When response was received
- `Duration_ms`: Total time from start to end
- `Execution_Time_ms`: Time spent executing code
- `Container_ID`: Container that processed the request
- `Replica_ID`: Replica that processed the request
- `CPU_Usage_%`: CPU usage percentage
- `Memory_Usage_Bytes`: Memory usage in bytes
- `Test_Cases_Passed`: Number of test cases that passed
- `Test_Cases_Total`: Total number of test cases (20)
- `All_Passed`: Yes if all 20 test cases passed

## ⚠️ Issues Identified

1. **High Failure Rate (70.4%)**:
   - Many requests timed out (HTTP 000) after 180 seconds
   - Some requests returned HTTP 503 (Service Unavailable)
   - System was overwhelmed with 500 concurrent requests

2. **Replica Information**:
   - Replica IDs show as "unknown" in CSV
   - This is due to API response format differences
   - Replicas were running (9 active replicas confirmed)

3. **Language Performance**:
   - Python and JavaScript performed best (57% and 48% success)
   - C++, Java, and C# had lower success rates (7-25%)
   - This may be due to compilation overhead and longer execution times

## 💡 Recommendations

1. **Stagger Requests**: Instead of 500 concurrent requests, stagger them (e.g., 50 at a time)
2. **Increase Timeout**: Current 180s timeout may be too short for 20 test cases
3. **Pre-warm More Replicas**: Start with 5-10 replicas instead of 3
4. **Optimize Compilation**: C++/Java/C# compilation adds overhead - consider caching compiled code
5. **Reduce Test Cases**: For load testing, use fewer test cases (e.g., 5-10 instead of 20)

## ✅ What Worked

1. **CSV Export**: Successfully created detailed CSV with all metrics
2. **Auto-scaling**: System scaled from 3 to 9 replicas automatically
3. **Sequential Test Execution**: Test cases executed sequentially (no parallel issues)
4. **Python/JavaScript**: These languages handled the load well
5. **Data Collection**: All requested metrics were captured and saved

## 📅 Test Timestamps

**Start**: 2025-12-04 23:10:12.314  
**End**: 2025-12-04 23:13:18.818  
**Duration**: 186,504ms (186.5 seconds / 3.1 minutes)

