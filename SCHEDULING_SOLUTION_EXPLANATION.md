# ✅ Scheduling Problem - Complete Solution

## 🎯 Problem Summary

**Goal:** Find minimum time to handle all requests by distributing them across servers.

**Key Rules:**
1. Each server has capacity[i] requests/second
2. After use, capacity becomes floor(capacity[i]/2)
3. Each server use takes 1 second
4. Need to handle all requests in minimum time

---

## 💡 Solution Strategy: Greedy Algorithm

**Approach:** Always use the server with the **highest capacity** at each step.

**Why Greedy Works:**
- Using a higher capacity server handles more requests per second
- This minimizes the total number of seconds needed
- Optimal because we want to maximize throughput at each step

---

## 🔧 Algorithm

```
1. Put all server capacities in a max heap (priority queue)
2. While there are remaining requests:
   a. Pop the server with maximum capacity
   b. Use it to handle min(capacity, remaining) requests
   c. Reduce remaining requests
   d. Calculate new capacity = floor(old_capacity / 2)
   e. If new_capacity > 0, push it back to heap
   f. Increment time by 1
3. Return total time
```

---

## 💻 Complete Code

```cpp
int calculateSchedulingTime(vector<int>& capacity, long long requests) {
    priority_queue<int> pq;  // Max heap
    
    // Add all capacities to heap
    for (int cap : capacity) {
        pq.push(cap);
    }
    
    long long remaining = requests;
    int time = 0;
    
    while (remaining > 0) {
        if (pq.empty()) break;
        
        int max_capacity = pq.top();
        pq.pop();
        
        long long handled = min((long long)max_capacity, remaining);
        remaining -= handled;
        time++;
        
        int new_capacity = max_capacity / 2;
        if (new_capacity > 0) {
            pq.push(new_capacity);
        }
    }
    
    return time;
}
```

---

## 📊 Example Walkthrough

**Input:** capacity = [2, 1, 5, 3, 1], requests = 17

**Step-by-step:**

| Step | Heap (max first) | Max Capacity | Handled | Remaining | Time |
|------|------------------|--------------|---------|-----------|------|
| Start | [5, 3, 2, 1, 1] | - | - | 17 | 0 |
| 1 | [5, 3, 2, 1, 1] | 5 | 5 | 12 | 1 |
| 2 | [3, 2, 2, 1, 1] | 3 | 3 | 9 | 2 |
| 3 | [2, 2, 1, 1, 1] | 2 | 2 | 7 | 3 |
| 4 | [2, 1, 1, 1, 1] | 2 | 2 | 5 | 4 |
| 5 | [1, 1, 1, 1, 1] | 1 | 1 | 4 | 5 |
| 6 | [1, 1, 1, 1] | 1 | 1 | 3 | 6 |
| 7 | [1, 1, 1] | 1 | 1 | 2 | 7 |
| 8 | [1, 1] | 1 | 1 | 1 | 8 |
| 9 | [1] | 1 | 1 | 0 | 9 |

**Result:** 9 seconds ✅

---

## ✅ Test Results

All test cases passed:

- ✅ Test Case 0: [2,1,5,3,1], requests=17 → **9** ✓
- ✅ Test Case 1: [3,1,4,2], requests=3 → **1** ✓
- ✅ Test Case 2: [7,10,9,10,6,3,9,9,10,10], requests=122 → **20** ✓

---

## 🔍 Key Points

1. **Max Heap:** Use `priority_queue<int>` (default is max heap)
2. **Greedy Choice:** Always pick maximum capacity
3. **Capacity Halving:** Use integer division (floor automatically)
4. **Edge Case:** Only push back if new_capacity > 0
5. **Data Types:** Use `long long` for requests (can be up to 10^12)

---

## ⚡ Time Complexity

- **Time:** O(T log n) where T = total time, n = number of servers
- **Space:** O(n) for the heap

**Note:** T is typically much smaller than requests due to greedy optimization.

---

## 📝 Complete Solution File

See `SCHEDULING_PROBLEM_COMPLETE_SOLUTION.cpp` for the full working code.

---

**Status:** ✅ **All test cases pass!**


