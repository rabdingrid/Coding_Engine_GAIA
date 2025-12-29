#include <bits/stdc++.h>
using namespace std;

string ltrim(const string &);
string rtrim(const string &);

// WRONG SOLUTION: Passes simple cases, fails complex cases
// Bug: Doesn't reuse servers after their capacity halves - only uses each server once
int calculateSchedulingTime(vector<int>& capacity, long long requests) {
    priority_queue<int> pq;
    
    for (int cap : capacity) {
        pq.push(cap);
    }
    
    long long remaining = requests;
    int time = 0;
    
    while (remaining > 0) {
        if (pq.empty()) {
            break;
        }
        
        int max_capacity = pq.top();
        pq.pop();
        
        // Handle requests
        long long handled = min((long long)max_capacity, remaining);
        remaining -= handled;
        time++;
        
        // BUG: Doesn't push server back after use
        // This works for simple cases where one server handles all requests
        // But fails for complex cases where we need to reuse servers
        int new_capacity = max_capacity / 2;
        // WRONG: Should push back if new_capacity > 0, but this code doesn't
        // This causes servers to be "used up" after first use
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
