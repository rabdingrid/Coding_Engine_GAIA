#include <bits/stdc++.h>
using namespace std;

string ltrim(const string &);
string rtrim(const string &);

// Solution: Greedy approach using max heap
// Always use the server with highest capacity at each step
int calculateSchedulingTime(vector<int>& capacity, long long requests) {
    // Use max heap (priority queue) to always get server with highest capacity
    priority_queue<int> pq;
    
    // Add all server capacities to the heap
    for (int cap : capacity) {
        pq.push(cap);
    }
    
    long long remaining = requests;
    int time = 0;
    
    // Process requests until all are handled
    while (remaining > 0) {
        if (pq.empty()) {
            // Safety check (should not happen based on constraints)
            break;
        }
        
        // Get server with maximum capacity
        int max_capacity = pq.top();
        pq.pop();
        
        // Use this server to handle requests (up to its capacity)
        long long handled = min((long long)max_capacity, remaining);
        remaining -= handled;
        time++; // Each server use takes 1 second
        
        // After use, capacity becomes floor(capacity/2)
        int new_capacity = max_capacity / 2;
        
        // Add server back to heap if it still has capacity
        if (new_capacity > 0) {
            pq.push(new_capacity);
        }
    }
    
    return time;
}

int main() {
    string capacity_count_temp;
    getline(cin, capacity_count_temp);
    int capacity_count = stoi(ltrim(rtrim(capacity_count_temp)));
    
    vector<int> capacity(capacity_count);
    for (int i = 0; i < capacity_count; i++) {
        string capacity_item_temp;
        getline(cin, capacity_item_temp);
        int capacity_item = stoi(ltrim(rtrim(capacity_item_temp)));
        capacity[i] = capacity_item;
    }
    
    string requests_temp;
    getline(cin, requests_temp);
    long long requests = stoll(ltrim(rtrim(requests_temp)));
    
    int result = calculateSchedulingTime(capacity, requests);
    cout << result << "\n";
    
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
}


