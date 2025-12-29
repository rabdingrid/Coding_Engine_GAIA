#!/usr/bin/env python3
"""
Add "Count Between" question with correct boilerplates and solutions
"""

import json
import os
import asyncpg
import asyncio
import uuid
from pathlib import Path

DB_URL = os.getenv('DATABASE_URL', 'postgresql://postgresadmin:5oXcNX59QmEl7zmV3DbjemkiJ@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require')

QUESTION_UUID = "22c620aa-b462-4ca5-adee-74ef95598862"  # Existing UUID from previous run
TEST_CASES_DIR = Path("/Users/rabdin/Downloads/314967")

# Question details
QUESTION_TITLE = "Count Between"
QUESTION_DIFFICULTY = "Easy"
QUESTION_TAGS = ["Binary Search", "Data Structures", "Algorithms", "Arrays", "Problem Solving"]

# Problem description (HTML formatted)
PROBLEM_DESCRIPTION = """<h3>Problem</h3>

<p>Given:</p>
<ul>
    <li>An array of integers arr</li>
    <li>Two arrays low and high representing the lower and upper bounds of each range query</li>
    <li>For each range query, count how many elements in arr have values between low[i] and high[i] inclusive.</li>
</ul>

<h3>Example 1</h3>
<p>arr = [1, 3, 5, 6, 8]</p>
<p>low = [2]</p>
<p>high = [6]</p>
<p>Query 0: There are 3 elements in the inclusive range [2, 6]: [3, 5, 6] so store 3 in index 0 of the return array.</p>
<p>Return [3].</p>

<h3>Example 2</h3>
<p>arr = [4, 8, 7]</p>
<p>low = [2, 4]</p>
<p>high = [8, 4]</p>
<p>Query 0: There are 3 elements in the inclusive range [2, 8]: [4, 7, 8] so store 3 in index 0 of the return array.</p>
<p>Query 1: There is 1 element in the inclusive range [4, 4]: [4] so store 1 in index 1 of the return array.</p>
<p>Return [3, 1].</p>

<h3>Function Description</h3>
<p>Complete the function <code>countBetween</code> which takes:</p>
<ul>
    <li><code>int arr[n]</code>: array of integers</li>
    <li><code>int low[q]</code>: lower bounds for queries</li>
    <li><code>int high[q]</code>: upper bounds for queries</li>
</ul>
<p><strong>Returns:</strong> <code>int[q]</code>: count of elements in range for each query</p>

<h3>Constraints</h3>
<ul>
    <li>1 ≤ n ≤ 10<sup>5</sup></li>
    <li>1 ≤ arr[j] ≤ 10<sup>9</sup></li>
    <li>1 ≤ q ≤ 10<sup>5</sup></li>
    <li>1 ≤ low[i] ≤ high[i] ≤ 10<sup>9</sup></li>
</ul>"""

# Correct boilerplates (following Endpoint Inspection pattern)
BOILERPLATES = {
    "python": """def countBetween(arr, low, high):
    # Write your code here

n = int(input().strip())
arr = []
for _ in range(n):
    arr_item = int(input().strip())
    arr.append(arr_item)
q = int(input().strip())
low = []
for _ in range(q):
    low_item = int(input().strip())
    low.append(low_item)
q2 = int(input().strip())
high = []
for _ in range(q2):
    high_item = int(input().strip())
    high.append(high_item)
result = countBetween(arr, low, high)
print('\\n'.join(map(str, result)))""",

    "cpp": """#include <bits/stdc++.h>
using namespace std;

string ltrim(const string &);
string rtrim(const string &);

vector<int> countBetween(vector<int> arr, vector<int> low, vector<int> high) {
}

int main()
{
    string n_temp;
    getline(cin, n_temp);
    int n = stoi(ltrim(rtrim(n_temp)));
    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        string arr_item_temp;
        getline(cin, arr_item_temp);
        int arr_item = stoi(ltrim(rtrim(arr_item_temp)));
        arr[i] = arr_item;
    }
    string q_temp;
    getline(cin, q_temp);
    int q = stoi(ltrim(rtrim(q_temp)));
    vector<int> low(q);
    for (int i = 0; i < q; i++) {
        string low_item_temp;
        getline(cin, low_item_temp);
        int low_item = stoi(ltrim(rtrim(low_item_temp)));
        low[i] = low_item;
    }
    string q_temp2;
    getline(cin, q_temp2);
    int q2 = stoi(ltrim(rtrim(q_temp2)));
    vector<int> high(q2);
    for (int i = 0; i < q2; i++) {
        string high_item_temp;
        getline(cin, high_item_temp);
        int high_item = stoi(ltrim(rtrim(high_item_temp)));
        high[i] = high_item;
    }
    vector<int> result = countBetween(arr, low, high);
    for (size_t i = 0; i < result.size(); i++) {
        cout << result[i];
        if (i != result.size() - 1) {
            cout << "\\n";
        }
    }
    cout << "\\n";
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
}""",

    "java": """import java.io.*;
import java.util.*;

class Result {
    public static List<Integer> countBetween(List<Integer> arr, List<Integer> low, List<Integer> high) {
    // Write your code here
    }
}

class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(bufferedReader.readLine().trim());
        List<Integer> arr = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            int arrItem = Integer.parseInt(bufferedReader.readLine().trim());
            arr.add(arrItem);
        }
        int q = Integer.parseInt(bufferedReader.readLine().trim());
        List<Integer> low = new ArrayList<>();
        for (int i = 0; i < q; i++) {
            int lowItem = Integer.parseInt(bufferedReader.readLine().trim());
            low.add(lowItem);
        }
        int q2 = Integer.parseInt(bufferedReader.readLine().trim());
        List<Integer> high = new ArrayList<>();
        for (int i = 0; i < q2; i++) {
            int highItem = Integer.parseInt(bufferedReader.readLine().trim());
            high.add(highItem);
        }
        List<Integer> result = Result.countBetween(arr, low, high);
        System.out.println(
            result.stream()
                .map(Object::toString)
                .collect(java.util.stream.Collectors.joining("\\n"))
        );
        bufferedReader.close();
    }
}""",

    "javascript": """function countBetween(arr, low, high) {
    // Write your code here
}

const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false
});

const lines = [];
rl.on('line', (line) => {
    lines.push(line);
});

rl.on('close', () => {
    let idx = 0;
    const n = parseInt(lines[idx++].trim(), 10);
    let arr = [];
    for (let i = 0; i < n; i++) {
        arr.push(parseInt(lines[idx++].trim(), 10));
    }
    const q = parseInt(lines[idx++].trim(), 10);
    let low = [];
    for (let i = 0; i < q; i++) {
        low.push(parseInt(lines[idx++].trim(), 10));
    }
    const q2 = parseInt(lines[idx++].trim(), 10);
    let high = [];
    for (let i = 0; i < q2; i++) {
        high.push(parseInt(lines[idx++].trim(), 10));
    }
    const result = countBetween(arr, low, high);
    console.log(result.join('\\n'));
});""",

    "csharp": """using System;
using System.Collections.Generic;
using System.Linq;

class Result {
    public static List<int> countBetween(List<int> arr, List<int> low, List<int> high)
    {
    }
}

class Solution {
    public static void Main(string[] args)
    {
        int n = Convert.ToInt32(Console.ReadLine().Trim());
        List<int> arr = new List<int>();
        for (int i = 0; i < n; i++) {
            int arrItem = Convert.ToInt32(Console.ReadLine().Trim());
            arr.Add(arrItem);
        }
        int q = Convert.ToInt32(Console.ReadLine().Trim());
        List<int> low = new List<int>();
        for (int i = 0; i < q; i++) {
            int lowItem = Convert.ToInt32(Console.ReadLine().Trim());
            low.Add(lowItem);
        }
        int q2 = Convert.ToInt32(Console.ReadLine().Trim());
        List<int> high = new List<int>();
        for (int i = 0; i < q2; i++) {
            int highItem = Convert.ToInt32(Console.ReadLine().Trim());
            high.Add(highItem);
        }
        List<int> result = Result.countBetween(arr, low, high);
        Console.WriteLine(String.Join("\\n", result));
    }
}"""
}

# Correct solutions for all languages
SOLUTIONS = {
    "python": """def countBetween(arr, low, high):
    # Sort array for binary search
    arr_sorted = sorted(arr)
    result = []
    
    for i in range(len(low)):
        # Count elements in range [low[i], high[i]] inclusive
        count = 0
        for num in arr_sorted:
            if low[i] <= num <= high[i]:
                count += 1
        result.append(count)
    
    return result

n = int(input().strip())
arr = []
for _ in range(n):
    arr_item = int(input().strip())
    arr.append(arr_item)
q = int(input().strip())
low = []
for _ in range(q):
    low_item = int(input().strip())
    low.append(low_item)
q2 = int(input().strip())
high = []
for _ in range(q2):
    high_item = int(input().strip())
    high.append(high_item)
result = countBetween(arr, low, high)
print('\\n'.join(map(str, result)))""",

    "cpp": """#include <bits/stdc++.h>
using namespace std;

string ltrim(const string &);
string rtrim(const string &);

vector<int> countBetween(vector<int> arr, vector<int> low, vector<int> high) {
    sort(arr.begin(), arr.end());
    vector<int> result;
    
    for (int i = 0; i < low.size(); i++) {
        int count = 0;
        for (int num : arr) {
            if (num >= low[i] && num <= high[i]) {
                count++;
            }
        }
        result.push_back(count);
    }
    
    return result;
}

int main()
{
    string n_temp;
    getline(cin, n_temp);
    int n = stoi(ltrim(rtrim(n_temp)));
    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        string arr_item_temp;
        getline(cin, arr_item_temp);
        int arr_item = stoi(ltrim(rtrim(arr_item_temp)));
        arr[i] = arr_item;
    }
    string q_temp;
    getline(cin, q_temp);
    int q = stoi(ltrim(rtrim(q_temp)));
    vector<int> low(q);
    for (int i = 0; i < q; i++) {
        string low_item_temp;
        getline(cin, low_item_temp);
        int low_item = stoi(ltrim(rtrim(low_item_temp)));
        low[i] = low_item;
    }
    string q_temp2;
    getline(cin, q_temp2);
    int q2 = stoi(ltrim(rtrim(q_temp2)));
    vector<int> high(q2);
    for (int i = 0; i < q2; i++) {
        string high_item_temp;
        getline(cin, high_item_temp);
        int high_item = stoi(ltrim(rtrim(high_item_temp)));
        high[i] = high_item;
    }
    vector<int> result = countBetween(arr, low, high);
    for (size_t i = 0; i < result.size(); i++) {
        cout << result[i];
        if (i != result.size() - 1) {
            cout << "\\n";
        }
    }
    cout << "\\n";
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
}""",

    "java": """import java.io.*;
import java.util.*;

class Result {
    public static List<Integer> countBetween(List<Integer> arr, List<Integer> low, List<Integer> high) {
        Collections.sort(arr);
        List<Integer> result = new ArrayList<>();
        
        for (int i = 0; i < low.size(); i++) {
            int count = 0;
            for (int num : arr) {
                if (num >= low.get(i) && num <= high.get(i)) {
                    count++;
                }
            }
            result.add(count);
        }
        
        return result;
    }
}

class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(bufferedReader.readLine().trim());
        List<Integer> arr = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            int arrItem = Integer.parseInt(bufferedReader.readLine().trim());
            arr.add(arrItem);
        }
        int q = Integer.parseInt(bufferedReader.readLine().trim());
        List<Integer> low = new ArrayList<>();
        for (int i = 0; i < q; i++) {
            int lowItem = Integer.parseInt(bufferedReader.readLine().trim());
            low.add(lowItem);
        }
        int q2 = Integer.parseInt(bufferedReader.readLine().trim());
        List<Integer> high = new ArrayList<>();
        for (int i = 0; i < q2; i++) {
            int highItem = Integer.parseInt(bufferedReader.readLine().trim());
            high.add(highItem);
        }
        List<Integer> result = Result.countBetween(arr, low, high);
        System.out.println(
            result.stream()
                .map(Object::toString)
                .collect(java.util.stream.Collectors.joining("\\n"))
        );
        bufferedReader.close();
    }
}""",

    "javascript": """function countBetween(arr, low, high) {
    arr.sort((a, b) => a - b);
    let result = [];
    
    for (let i = 0; i < low.length; i++) {
        let count = 0;
        for (let num of arr) {
            if (num >= low[i] && num <= high[i]) {
                count++;
            }
        }
        result.push(count);
    }
    
    return result;
}

const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false
});

const lines = [];
rl.on('line', (line) => {
    lines.push(line);
});

rl.on('close', () => {
    let idx = 0;
    const n = parseInt(lines[idx++].trim(), 10);
    let arr = [];
    for (let i = 0; i < n; i++) {
        arr.push(parseInt(lines[idx++].trim(), 10));
    }
    const q = parseInt(lines[idx++].trim(), 10);
    let low = [];
    for (let i = 0; i < q; i++) {
        low.push(parseInt(lines[idx++].trim(), 10));
    }
    const q2 = parseInt(lines[idx++].trim(), 10);
    let high = [];
    for (let i = 0; i < q2; i++) {
        high.push(parseInt(lines[idx++].trim(), 10));
    }
    const result = countBetween(arr, low, high);
    console.log(result.join('\\n'));
});""",

    "csharp": """using System;
using System.Collections.Generic;
using System.Linq;

class Result {
    public static List<int> countBetween(List<int> arr, List<int> low, List<int> high)
    {
        arr.Sort();
        List<int> result = new List<int>();
        
        for (int i = 0; i < low.Count; i++) {
            int count = 0;
            foreach (int num in arr) {
                if (num >= low[i] && num <= high[i]) {
                    count++;
                }
            }
            result.Add(count);
        }
        
        return result;
    }
}

class Solution {
    public static void Main(string[] args)
    {
        int n = Convert.ToInt32(Console.ReadLine().Trim());
        List<int> arr = new List<int>();
        for (int i = 0; i < n; i++) {
            int arrItem = Convert.ToInt32(Console.ReadLine().Trim());
            arr.Add(arrItem);
        }
        int q = Convert.ToInt32(Console.ReadLine().Trim());
        List<int> low = new List<int>();
        for (int i = 0; i < q; i++) {
            int lowItem = Convert.ToInt32(Console.ReadLine().Trim());
            low.Add(lowItem);
        }
        int q2 = Convert.ToInt32(Console.ReadLine().Trim());
        List<int> high = new List<int>();
        for (int i = 0; i < q2; i++) {
            int highItem = Convert.ToInt32(Console.ReadLine().Trim());
            high.Add(highItem);
        }
        List<int> result = Result.countBetween(arr, low, high);
        Console.WriteLine(String.Join("\\n", result));
    }
}"""
}

def read_test_cases(test_dir):
    """Read all test cases from the directory"""
    test_cases = []
    sample_test_cases = []
    
    input_files = sorted([f for f in test_dir.glob("input*.txt")])
    
    for i, input_file in enumerate(input_files):
        test_num = input_file.stem.replace("input", "")
        output_file = test_dir / f"output{test_num}.txt"
        
        if not output_file.exists():
            continue
        
        input_data = input_file.read_text().strip()
        output_data = output_file.read_text().strip()
        
        test_case = {
            "id": f"test_case_{test_num}",
            "input": input_data,
            "expected_output": output_data
        }
        
        # First 3 are sample test cases
        if i < 3:
            sample_test_cases.append(test_case)
        else:
            test_cases.append(test_case)
    
    return sample_test_cases, test_cases

async def add_question():
    """Add the question to the database"""
    sample_test_cases, test_cases = read_test_cases(TEST_CASES_DIR)
    
    print(f"📊 Found {len(sample_test_cases)} sample test cases and {len(test_cases)} regular test cases")
    
    conn = await asyncpg.connect(DB_URL)
    
    try:
        await conn.execute("""
            UPDATE coding_question_bank
            SET question = $1,
                difficulty = $2,
                tags = $3,
                boiler_plate = $4,
                sample_test_cases = $5,
                test_cases = $6,
                solutions = $7
            WHERE uuid = $8
        """,
            PROBLEM_DESCRIPTION,
            QUESTION_DIFFICULTY.lower(),
            json.dumps([tag.lower() for tag in QUESTION_TAGS]),
            json.dumps(BOILERPLATES),
            json.dumps(sample_test_cases),
            json.dumps(test_cases),
            json.dumps(SOLUTIONS),
            QUESTION_UUID
        )
        
        print(f"✅ Question updated successfully!")
        print(f"   UUID: {QUESTION_UUID}")
        print(f"   Title: {QUESTION_TITLE}")
        print(f"   Difficulty: {QUESTION_DIFFICULTY}")
        print(f"   Tags: {QUESTION_TAGS}")
        print(f"   Sample Test Cases: {len(sample_test_cases)}")
        print(f"   Regular Test Cases: {len(test_cases)}")
        print(f"   Languages: {list(BOILERPLATES.keys())}")
        print(f"   Solutions: ✅ All 5 languages included")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(add_question())

