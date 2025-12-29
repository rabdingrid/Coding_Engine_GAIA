#!/usr/bin/env python3
"""
Generate 50 DSA Questions with 20+ Test Cases Each
Creates proper file system structure with IDs, test cases, and boilerplates
"""

import os
import json
import uuid
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# 50 DSA Questions with categories
QUESTIONS = [
    # ARRAYS & STRINGS (10 questions)
    {
        "id": "Q001",
        "title": "Two Sum",
        "category": "Array",
        "difficulty": "Easy",
        "tags": ["Array", "Hash Table"],
        "description": """Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Example 2:
Input: nums = [3,2,4], target = 6
Output: [1,2]

Example 3:
Input: nums = [3,3], target = 6
Output: [0,1]""",
        "test_cases": [
            {"input": "4\n2 7 11 15\n9", "output": "0 1"},
            {"input": "3\n3 2 4\n6", "output": "1 2"},
            {"input": "2\n3 3\n6", "output": "0 1"},
            {"input": "5\n1 2 3 4 5\n9", "output": "3 4"},
            {"input": "10\n1 5 8 12 15 20 25 30 35 40\n45", "output": "4 5"},
            {"input": "2\n-1 -2\n-3", "output": "0 1"},
            {"input": "4\n0 4 3 0\n0", "output": "0 3"},
            {"input": "100\n" + " ".join(str(i) for i in range(100)) + "\n197", "output": "98 99"},
            {"input": "3\n-10 -5 5\n0", "output": "1 2"},
            {"input": "6\n1 1 1 1 1 1\n2", "output": "0 1"},
            {"input": "20\n" + " ".join(str(i*2) for i in range(20)) + "\n38", "output": "9 10"},
            {"input": "50\n" + " ".join(str(i) for i in range(50)) + "\n97", "output": "48 49"},
            {"input": "1000\n" + " ".join(str(i) for i in range(1000)) + "\n1997", "output": "998 999"},
            {"input": "5\n-1 0 1 2 3\n1", "output": "0 2"},
            {"input": "8\n1 2 3 4 5 6 7 8\n15", "output": "6 7"},
            {"input": "15\n" + " ".join(str(i*10) for i in range(15)) + "\n280", "output": "13 14"},
            {"input": "30\n" + " ".join(str(i) for i in range(30)) + "\n57", "output": "28 29"},
            {"input": "4\n1000 2000 3000 4000\n5000", "output": "1 2"},
            {"input": "7\n-5 -3 -1 0 1 3 5\n2", "output": "2 4"},
            {"input": "200\n" + " ".join(str(i) for i in range(200)) + "\n397", "output": "198 199"},
            {"input": "3\n1000000 2000000 3000000\n5000000", "output": "1 2"},
        ],
        "boilerplates": {
            "python": """def twoSum(nums, target):
    # Your code here
    pass

# Read input
n = int(input())
nums = list(map(int, input().split()))
target = int(input())

# Call function
result = twoSum(nums, target)
print(result[0], result[1])""",
            "java": """import java.util.*;

public class Solution {
    public int[] twoSum(int[] nums, int target) {
        // Your code here
        return new int[]{0, 0};
    }
    
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) {
            nums[i] = sc.nextInt();
        }
        int target = sc.nextInt();
        
        Solution sol = new Solution();
        int[] result = sol.twoSum(nums, target);
        System.out.println(result[0] + " " + result[1]);
    }
}""",
            "cpp": """#include <iostream>
#include <vector>
#include <unordered_map>
using namespace std;

vector<int> twoSum(vector<int>& nums, int target) {
    // Your code here
    return {};
}

int main() {
    int n;
    cin >> n;
    vector<int> nums(n);
    for (int i = 0; i < n; i++) {
        cin >> nums[i];
    }
    int target;
    cin >> target;
    
    vector<int> result = twoSum(nums, target);
    cout << result[0] << " " << result[1] << endl;
    return 0;
}""",
            "javascript": """function twoSum(nums, target) {
    // Your code here
    return [0, 0];
}

// Read input
const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

let input = [];
rl.on('line', (line) => {
    input.push(line);
    if (input.length === 3) {
        const n = parseInt(input[0]);
        const nums = input[1].split(' ').map(Number);
        const target = parseInt(input[2]);
        const result = twoSum(nums, target);
        console.log(result[0], result[1]);
        rl.close();
    }
});""",
            "csharp": """using System;
using System.Linq;

public class Solution {
    public int[] TwoSum(int[] nums, int target) {
        // Your code here
        return new int[] {0, 0};
    }
    
    public static void Main() {
        int n = int.Parse(Console.ReadLine());
        int[] nums = Console.ReadLine().Split(' ').Select(int.Parse).ToArray();
        int target = int.Parse(Console.ReadLine());
        
        Solution sol = new Solution();
        int[] result = sol.TwoSum(nums, target);
        Console.WriteLine(result[0] + " " + result[1]);
    }
}"""
        }
    },
    # Add more questions here - I'll create a comprehensive list
]

def create_question_structure(question_data):
    """Create file structure for a single question"""
    q_id = question_data["id"]
    q_dir = BASE_DIR / q_id
    
    # Create directories
    (q_dir / "test_cases").mkdir(parents=True, exist_ok=True)
    (q_dir / "boilerplates").mkdir(parents=True, exist_ok=True)
    
    # Create metadata.json
    metadata = {
        "id": q_id,
        "uuid": str(uuid.uuid5(uuid.NAMESPACE_DNS, f"dsa-question-{q_id}")),
        "title": question_data["title"],
        "category": question_data["category"],
        "difficulty": question_data["difficulty"],
        "tags": question_data["tags"],
        "test_case_count": len(question_data["test_cases"])
    }
    
    with open(q_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    # Create problem.md
    with open(q_dir / "problem.md", "w") as f:
        f.write(f"# {question_data['title']}\n\n")
        f.write(f"**Category**: {question_data['category']}\n")
        f.write(f"**Difficulty**: {question_data['difficulty']}\n")
        f.write(f"**Tags**: {', '.join(question_data['tags'])}\n\n")
        f.write(question_data["description"])
    
    # Create test cases
    for idx, tc in enumerate(question_data["test_cases"], 1):
        tc_num = f"{idx:02d}"
        with open(q_dir / "test_cases" / f"{tc_num}.in", "w") as f:
            f.write(tc["input"])
        with open(q_dir / "test_cases" / f"{tc_num}.out", "w") as f:
            f.write(tc["output"])
    
    # Create boilerplates
    for lang, code in question_data["boilerplates"].items():
        ext = {"python": "py", "java": "java", "cpp": "cpp", "javascript": "js", "csharp": "cs"}[lang]
        with open(q_dir / "boilerplates" / f"{lang}.{ext}", "w") as f:
            f.write(code)
    
    print(f"✅ Created {q_id}: {question_data['title']}")

if __name__ == "__main__":
    print("🚀 Generating 50 DSA Questions...")
    print(f"📁 Base directory: {BASE_DIR}")
    
    # For now, create structure for first question as example
    # Full 50 questions will be added in next step
    if QUESTIONS:
        create_question_structure(QUESTIONS[0])
        print(f"\n✅ Generated {len(QUESTIONS)} question(s)")
        print("📝 Note: Full 50 questions will be added in next iteration")
    else:
        print("⚠️  No questions defined yet")

