#include <bits/stdc++.h>

using namespace std;

string ltrim(const string &);

string rtrim(const string &);

int findTotalWeight(vector<int> cans) {

    int total = 0;

    while (!cans.empty()) {

        // Find the minimum weight and its index

        int minWeight = cans[0];

        int minIndex = 0;

        for (int i = 1; i < cans.size(); i++) {

            if (cans[i] < minWeight) {

                minWeight = cans[i];

                minIndex = i;

            }

        }

        // Add the minimum weight to total

        total += minWeight;

        // Determine the range to remove

        // Remove the minimum can and its two adjacent cans (or fewer if at edge)

        int startIdx = max(0, minIndex - 1);

        int endIdx = min((int)cans.size() - 1, minIndex + 1);

        // Remove elements from end to start to maintain indices

        cans.erase(cans.begin() + startIdx, cans.begin() + endIdx + 1);

    }

    return total;

}

int main()

{

    string cans_count_temp;

    getline(cin, cans_count_temp);

    int cans_count = stoi(ltrim(rtrim(cans_count_temp)));

    vector<int> cans(cans_count);

    for (int i = 0; i < cans_count; i++) {

        string cans_item_temp;

        getline(cin, cans_item_temp);

        int cans_item = stoi(ltrim(rtrim(cans_item_temp)));

        cans[i] = cans_item;

    }

    int result = findTotalWeight(cans);

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

