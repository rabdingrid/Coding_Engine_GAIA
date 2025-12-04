# Coding Question Bank - Complete List

This file contains all questions from the `coding_question_bank` table.

**Generated:** 2025-12-04 15:10:09
**Total Questions:** 52

---


## Question #1

**UUID:** `067ce721-4bef-59fd-a3f2-43613e6b13e8`  
**Difficulty:** Medium  
**Tags:** String, Sliding Window  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Longest Substring Without Repeating Characters

**Category**: String
**Difficulty**: Medium
**Tags**: String, Sliding Window

## Problem Description

This is a medium level problem in the String category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Longest Substring Without Repeating Characters\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Longest Substring Without Repeating Characters\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Longest Substring Without Repeating Characters\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Longest Substring Without Repeating Characters\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Longest Substring Without Repeating Characters\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #2

**UUID:** `139eea7e-36ba-552a-9c52-dd4bfae96c02`  
**Difficulty:** Medium  
**Tags:** Binary Search  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Find First and Last Position

**Category**: Search
**Difficulty**: Medium
**Tags**: Binary Search

## Problem Description

This is a medium level problem in the Search category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Find First and Last Position\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Find First and Last Position\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Find First and Last Position\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Find First and Last Position\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Find First and Last Position\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #3

**UUID:** `1967bd33-8079-5b92-92de-eda54e6fbdfe`  
**Difficulty:** Medium  
**Tags:** Backtracking, Recursion  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Combination Sum

**Category**: Backtracking
**Difficulty**: Medium
**Tags**: Backtracking, Recursion

## Problem Description

This is a medium level problem in the Backtracking category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Combination Sum\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Combination Sum\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Combination Sum\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Combination Sum\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Combination Sum\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #4

**UUID:** `1b87758c-556a-5e22-bf40-4162c9c9e47b`  
**Difficulty:** Easy  
**Tags:** Tree, DFS  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Same Tree

**Category**: Tree
**Difficulty**: Easy
**Tags**: Tree, DFS

## Problem Description

This is a easy level problem in the Tree category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Same Tree\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Same Tree\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Same Tree\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Same Tree\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Same Tree\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #5

**UUID:** `1dd8aa8e-cba3-5f35-bbca-b2d23e3eef38`  
**Difficulty:** Medium  
**Tags:** Tree, DFS  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Validate Binary Search Tree

**Category**: Tree
**Difficulty**: Medium
**Tags**: Tree, DFS

## Problem Description

This is a medium level problem in the Tree category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Validate Binary Search Tree\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Validate Binary Search Tree\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Validate Binary Search Tree\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Validate Binary Search Tree\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Validate Binary Search Tree\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #6

**UUID:** `1f91a5e3-c13f-5955-8187-f5251af5a365`  
**Difficulty:** Medium  
**Tags:** Graph, Topological Sort  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Course Schedule

**Category**: Graph
**Difficulty**: Medium
**Tags**: Graph, Topological Sort

## Problem Description

This is a medium level problem in the Graph category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Course Schedule\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Course Schedule\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Course Schedule\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Course Schedule\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Course Schedule\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #7

**UUID:** `20ce4b04-4677-5350-b49c-979c562aee37`  
**Difficulty:** Medium  
**Tags:** Tree, DFS  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Construct Binary Tree from Preorder and Inorder

**Category**: Tree
**Difficulty**: Medium
**Tags**: Tree, DFS

## Problem Description

This is a medium level problem in the Tree category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Construct Binary Tree from Preorder and Inorder\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Construct Binary Tree from Preorder and Inorder\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Construct Binary Tree from Preorder and Inorder\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Construct Binary Tree from Preorder and Inorder\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Construct Binary Tree from Preorder and Inorder\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #8

**UUID:** `29ea5edc-191d-5145-a5b6-58387065205e`  
**Difficulty:** Medium  
**Tags:** DP  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# House Robber

**Category**: DP
**Difficulty**: Medium
**Tags**: DP

## Problem Description

This is a medium level problem in the DP category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for House Robber\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for House Robber\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for House Robber\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for House Robber\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for House Robber\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #9

**UUID:** `36858490-cff1-545f-aaec-6ca581a85c30`  
**Difficulty:** Medium  
**Tags:** String, Hash Table  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Group Anagrams

**Category**: String
**Difficulty**: Medium
**Tags**: String, Hash Table

## Problem Description

This is a medium level problem in the String category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Group Anagrams\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Group Anagrams\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Group Anagrams\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Group Anagrams\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Group Anagrams\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #10

**UUID:** `3a28702e-3afe-58cb-863a-53220f402f0e`  
**Difficulty:** Easy  
**Tags:** Array, Hash Table  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Two Sum

**Category**: Array
**Difficulty**: Easy
**Tags**: Array, Hash Table

## Problem Description

This is a easy level problem in the Array category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Two Sum\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Two Sum\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Two Sum\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Two Sum\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Two Sum\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "4\n2 7 11 15\n9",
    "stdin": "4\n2 7 11 15\n9",
    "output": "0 1",
    "stdout": "0 1",
    "expected_output": "0 1"
  },
  {
    "input": "3\n3 2 4\n6",
    "stdin": "3\n3 2 4\n6",
    "output": "1 2",
    "stdout": "1 2",
    "expected_output": "1 2"
  },
  {
    "input": "2\n3 3\n6",
    "stdin": "2\n3 3\n6",
    "output": "0 1",
    "stdout": "0 1",
    "expected_output": "0 1"
  }
]
```

### Test Cases

```json
[
  {
    "input": "4\n2 7 11 15\n9",
    "stdin": "4\n2 7 11 15\n9",
    "output": "0 1",
    "stdout": "0 1",
    "expected_output": "0 1"
  },
  {
    "input": "3\n3 2 4\n6",
    "stdin": "3\n3 2 4\n6",
    "output": "1 2",
    "stdout": "1 2",
    "expected_output": "1 2"
  },
  {
    "input": "2\n3 3\n6",
    "stdin": "2\n3 3\n6",
    "output": "0 1",
    "stdout": "0 1",
    "expected_output": "0 1"
  },
  {
    "input": "5\n1 2 3 4 5\n9",
    "stdin": "5\n1 2 3 4 5\n9",
    "output": "3 4",
    "stdout": "3 4",
    "expected_output": "3 4"
  },
  {
    "input": "6\n10 20 30 40 50 60\n70",
    "stdin": "6\n10 20 30 40 50 60\n70",
    "output": "2 3",
    "stdout": "2 3",
    "expected_output": "2 3"
  },
  {
    "input": "2\n-1 -2\n-3",
    "stdin": "2\n-1 -2\n-3",
    "output": "0 1",
    "stdout": "0 1",
    "expected_output": "0 1"
  },
  {
    "input": "4\n0 4 3 0\n0",
    "stdin": "4\n0 4 3 0\n0",
    "output": "0 3",
    "stdout": "0 3",
    "expected_output": "0 3"
  },
  {
    "input": "3\n-10 -5 5\n0",
    "stdin": "3\n-10 -5 5\n0",
    "output": "1 2",
    "stdout": "1 2",
    "expected_output": "1 2"
  },
  {
    "input": "1\n5\n5",
    "stdin": "1\n5\n5",
    "output": "0 0",
    "stdout": "0 0",
    "expected_output": "0 0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99\n197",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99\n197",
    "output": "98 99",
    "stdout": "98 99",
    "expected_output": "98 99"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199\n397",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199\n397",
    "output": "198 199",
    "stdout": "198 199",
    "expected_output": "198 199"
  },
  {
    "input": "500\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 377 378 379 380 381 382 383 384 385 386 387 388 389 390 391 392 393 394 395 396 397 398 399 400 401 402 403 404 405 406 407 408 409 410 411 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 430 431 432 433 434 435 436 437 438 439 440 441 442 443 444 445 446 447 448 449 450 451 452 453 454 455 456 457 458 459 460 461 462 463 464 465 466 467 468 469 470 471 472 473 474 475 476 477 478 479 480 481 482 483 484 485 486 487 488 489 490 491 492 493 494 495 496 497 498 499\n997",
    "stdin": "500\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 377 378 379 380 381 382 383 384 385 386 387 388 389 390 391 392 393 394 395 396 397 398 399 400 401 402 403 404 405 406 407 408 409 410 411 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 430 431 432 433 434 435 436 437 438 439 440 441 442 443 444 445 446 447 448 449 450 451 452 453 454 455 456 457 458 459 460 461 462 463 464 465 466 467 468 469 470 471 472 473 474 475 476 477 478 479 480 481 482 483 484 485 486 487 488 489 490 491 492 493 494 495 496 497 498 499\n997",
    "output": "498 499",
    "stdout": "498 499",
    "expected_output": "498 499"
  },
  {
    "input": "1000\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 377 378 379 380 381 382 383 384 385 386 387 388 389 390 391 392 393 394 395 396 397 398 399 400 401 402 403 404 405 406 407 408 409 410 411 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 430 431 432 433 434 435 436 437 438 439 440 441 442 443 444 445 446 447 448 449 450 451 452 453 454 455 456 457 458 459 460 461 462 463 464 465 466 467 468 469 470 471 472 473 474 475 476 477 478 479 480 481 482 483 484 485 486 487 488 489 490 491 492 493 494 495 496 497 498 499 500 501 502 503 504 505 506 507 508 509 510 511 512 513 514 515 516 517 518 519 520 521 522 523 524 525 526 527 528 529 530 531 532 533 534 535 536 537 538 539 540 541 542 543 544 545 546 547 548 549 550 551 552 553 554 555 556 557 558 559 560 561 562 563 564 565 566 567 568 569 570 571 572 573 574 575 576 577 578 579 580 581 582 583 584 585 586 587 588 589 590 591 592 593 594 595 596 597 598 599 600 601 602 603 604 605 606 607 608 609 610 611 612 613 614 615 616 617 618 619 620 621 622 623 624 625 626 627 628 629 630 631 632 633 634 635 636 637 638 639 640 641 642 643 644 645 646 647 648 649 650 651 652 653 654 655 656 657 658 659 660 661 662 663 664 665 666 667 668 669 670 671 672 673 674 675 676 677 678 679 680 681 682 683 684 685 686 687 688 689 690 691 692 693 694 695 696 697 698 699 700 701 702 703 704 705 706 707 708 709 710 711 712 713 714 715 716 717 718 719 720 721 722 723 724 725 726 727 728 729 730 731 732 733 734 735 736 737 738 739 740 741 742 743 744 745 746 747 748 749 750 751 752 753 754 755 756 757 758 759 760 761 762 763 764 765 766 767 768 769 770 771 772 773 774 775 776 777 778 779 780 781 782 783 784 785 786 787 788 789 790 791 792 793 794 795 796 797 798 799 800 801 802 803 804 805 806 807 808 809 810 811 812 813 814 815 816 817 818 819 820 821 822 823 824 825 826 827 828 829 830 831 832 833 834 835 836 837 838 839 840 841 842 843 844 845 846 847 848 849 850 851 852 853 854 855 856 857 858 859 860 861 862 863 864 865 866 867 868 869 870 871 872 873 874 875 876 877 878 879 880 881 882 883 884 885 886 887 888 889 890 891 892 893 894 895 896 897 898 899 900 901 902 903 904 905 906 907 908 909 910 911 912 913 914 915 916 917 918 919 920 921 922 923 924 925 926 927 928 929 930 931 932 933 934 935 936 937 938 939 940 941 942 943 944 945 946 947 948 949 950 951 952 953 954 955 956 957 958 959 960 961 962 963 964 965 966 967 968 969 970 971 972 973 974 975 976 977 978 979 980 981 982 983 984 985 986 987 988 989 990 991 992 993 994 995 996 997 998 999\n1997",
    "stdin": "1000\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 377 378 379 380 381 382 383 384 385 386 387 388 389 390 391 392 393 394 395 396 397 398 399 400 401 402 403 404 405 406 407 408 409 410 411 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 430 431 432 433 434 435 436 437 438 439 440 441 442 443 444 445 446 447 448 449 450 451 452 453 454 455 456 457 458 459 460 461 462 463 464 465 466 467 468 469 470 471 472 473 474 475 476 477 478 479 480 481 482 483 484 485 486 487 488 489 490 491 492 493 494 495 496 497 498 499 500 501 502 503 504 505 506 507 508 509 510 511 512 513 514 515 516 517 518 519 520 521 522 523 524 525 526 527 528 529 530 531 532 533 534 535 536 537 538 539 540 541 542 543 544 545 546 547 548 549 550 551 552 553 554 555 556 557 558 559 560 561 562 563 564 565 566 567 568 569 570 571 572 573 574 575 576 577 578 579 580 581 582 583 584 585 586 587 588 589 590 591 592 593 594 595 596 597 598 599 600 601 602 603 604 605 606 607 608 609 610 611 612 613 614 615 616 617 618 619 620 621 622 623 624 625 626 627 628 629 630 631 632 633 634 635 636 637 638 639 640 641 642 643 644 645 646 647 648 649 650 651 652 653 654 655 656 657 658 659 660 661 662 663 664 665 666 667 668 669 670 671 672 673 674 675 676 677 678 679 680 681 682 683 684 685 686 687 688 689 690 691 692 693 694 695 696 697 698 699 700 701 702 703 704 705 706 707 708 709 710 711 712 713 714 715 716 717 718 719 720 721 722 723 724 725 726 727 728 729 730 731 732 733 734 735 736 737 738 739 740 741 742 743 744 745 746 747 748 749 750 751 752 753 754 755 756 757 758 759 760 761 762 763 764 765 766 767 768 769 770 771 772 773 774 775 776 777 778 779 780 781 782 783 784 785 786 787 788 789 790 791 792 793 794 795 796 797 798 799 800 801 802 803 804 805 806 807 808 809 810 811 812 813 814 815 816 817 818 819 820 821 822 823 824 825 826 827 828 829 830 831 832 833 834 835 836 837 838 839 840 841 842 843 844 845 846 847 848 849 850 851 852 853 854 855 856 857 858 859 860 861 862 863 864 865 866 867 868 869 870 871 872 873 874 875 876 877 878 879 880 881 882 883 884 885 886 887 888 889 890 891 892 893 894 895 896 897 898 899 900 901 902 903 904 905 906 907 908 909 910 911 912 913 914 915 916 917 918 919 920 921 922 923 924 925 926 927 928 929 930 931 932 933 934 935 936 937 938 939 940 941 942 943 944 945 946 947 948 949 950 951 952 953 954 955 956 957 958 959 960 961 962 963 964 965 966 967 968 969 970 971 972 973 974 975 976 977 978 979 980 981 982 983 984 985 986 987 988 989 990 991 992 993 994 995 996 997 998 999\n1997",
    "output": "998 999",
    "stdout": "998 999",
    "expected_output": "998 999"
  },
  {
    "input": "4\n1000000 2000000 3000000 4000000\n5000000",
    "stdin": "4\n1000000 2000000 3000000 4000000\n5000000",
    "output": "1 2",
    "stdout": "1 2",
    "expected_output": "1 2"
  },
  {
    "input": "3\n-1000000 -2000000 3000000\n0",
    "stdin": "3\n-1000000 -2000000 3000000\n0",
    "output": "0 2",
    "stdout": "0 2",
    "expected_output": "0 2"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #11

**UUID:** `3e7a0f8d-4b83-4a95-9c2b-91fce948af22`  
**Difficulty:** Medium  
**Tags:** simulation, queue, turnstile, greedy  
**Sample Test Cases:** 0  
**Test Cases:** 0  

### Question Description


A single-lane turnstile is placed at a building entry point. People can approach it either to **enter** the building or to **exit** it. Only one person can pass at any second.

Each person is associated with:
- `time[i]`: the exact second they arrive at the turnstile
- `direction[i]`: their intended movement  
  - `0` → wants to enter  
  - `1` → wants to exit

Arrivals occur in non-decreasing order of time.

Turnstile Operating Policy:

Rule A — Continuation Preference  
If the turnstile was used in the previous second, it continues serving people in the **same direction**.

Rule B — Initial or Idle Preference  
If the turnstile was **not used** in the previous second, exiting (1) is given priority over entering (0).

Rule C — Valid Passage  
A person may pass only at or after their arrival time, and only if the rules above favor their direction at that moment.

You must return an array `result[]` where:  
`result[i]` is the time at which person `i` passes through the turnstile.

---

Example 1:

Input:
n = 4  
time = [0, 0, 1, 5]  
direction = [0, 1, 1, 0]

Output:
[2, 0, 1, 5]

---

Example 2:

Input:
n = 5  
time = [0,1,1,3,3]  
direction = [0,1,0,0,1]

Output:
[0,2,1,4,3]

---

Constraints:

1 ≤ n ≤ 100000  
0 ≤ time[i] ≤ 1e9  
time[i] ≤ time[i+1]  
direction[i] ∈ {0, 1}
    

---

## Question #12

**UUID:** `4214a262-c21b-535f-b3a1-7786f5f7c5ee`  
**Difficulty:** Easy  
**Tags:** Tree, DFS  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Path Sum

**Category**: Tree
**Difficulty**: Easy
**Tags**: Tree, DFS

## Problem Description

This is a easy level problem in the Tree category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Path Sum\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Path Sum\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Path Sum\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Path Sum\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Path Sum\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #13

**UUID:** `48aff220-c2c3-588a-abbf-4b24ee75370e`  
**Difficulty:** Easy  
**Tags:** LinkedList, Recursion  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Reverse Linked List

**Category**: LinkedList
**Difficulty**: Easy
**Tags**: LinkedList, Recursion

## Problem Description

This is a easy level problem in the LinkedList category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Reverse Linked List\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Reverse Linked List\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Reverse Linked List\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Reverse Linked List\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Reverse Linked List\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #14

**UUID:** `4bb77c02-7edd-53aa-9332-c8f0f641673b`  
**Difficulty:** Medium  
**Tags:** String, Sliding Window  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Find All Anagrams in a String

**Category**: String
**Difficulty**: Medium
**Tags**: String, Sliding Window

## Problem Description

This is a medium level problem in the String category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Find All Anagrams in a String\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Find All Anagrams in a String\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Find All Anagrams in a String\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Find All Anagrams in a String\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Find All Anagrams in a String\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #15

**UUID:** `4c2d6491-311c-568d-8470-7f243778267b`  
**Difficulty:** Hard  
**Tags:** Backtracking, Recursion  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# N-Queens

**Category**: Backtracking
**Difficulty**: Hard
**Tags**: Backtracking, Recursion

## Problem Description

This is a hard level problem in the Backtracking category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for N-Queens\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for N-Queens\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for N-Queens\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for N-Queens\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for N-Queens\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #16

**UUID:** `4e29b7b2-0f19-59c9-b932-8b48129a1a2a`  
**Difficulty:** Medium  
**Tags:** LinkedList, Math  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Add Two Numbers

**Category**: LinkedList
**Difficulty**: Medium
**Tags**: LinkedList, Math

## Problem Description

This is a medium level problem in the LinkedList category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Add Two Numbers\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Add Two Numbers\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Add Two Numbers\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Add Two Numbers\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Add Two Numbers\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #17

**UUID:** `555a50fe-00fb-5da7-96dd-34b7969ae184`  
**Difficulty:** Hard  
**Tags:** Stack, Monotonic Stack  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Largest Rectangle in Histogram

**Category**: Stack
**Difficulty**: Hard
**Tags**: Stack, Monotonic Stack

## Problem Description

This is a hard level problem in the Stack category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Largest Rectangle in Histogram\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Largest Rectangle in Histogram\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Largest Rectangle in Histogram\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Largest Rectangle in Histogram\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Largest Rectangle in Histogram\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #18

**UUID:** `55ace37c-f0d9-5551-8fee-e25943d9fdc5`  
**Difficulty:** Medium  
**Tags:** Array, Prefix Sum  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Product of Array Except Self

**Category**: Array
**Difficulty**: Medium
**Tags**: Array, Prefix Sum

## Problem Description

This is a medium level problem in the Array category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Product of Array Except Self\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Product of Array Except Self\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Product of Array Except Self\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Product of Array Except Self\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Product of Array Except Self\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #19

**UUID:** `5d21863d-6cae-5880-9a8f-7d95b240a1bc`  
**Difficulty:** Medium  
**Tags:** Backtracking, Recursion  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Permutations

**Category**: Backtracking
**Difficulty**: Medium
**Tags**: Backtracking, Recursion

## Problem Description

This is a medium level problem in the Backtracking category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Permutations\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Permutations\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Permutations\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Permutations\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Permutations\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #20

**UUID:** `64f5c789-6c10-555e-a5c6-d9e1ae5a1f17`  
**Difficulty:** Medium  
**Tags:** Array, DP  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Maximum Product Subarray

**Category**: Array
**Difficulty**: Medium
**Tags**: Array, DP

## Problem Description

This is a medium level problem in the Array category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Maximum Product Subarray\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Maximum Product Subarray\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Maximum Product Subarray\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Maximum Product Subarray\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Maximum Product Subarray\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #21

**UUID:** `6c4cc125-3c2b-558a-ab65-7947a5a47847`  
**Difficulty:** Medium  
**Tags:** Tree, DFS  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Lowest Common Ancestor

**Category**: Tree
**Difficulty**: Medium
**Tags**: Tree, DFS

## Problem Description

This is a medium level problem in the Tree category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Lowest Common Ancestor\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Lowest Common Ancestor\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Lowest Common Ancestor\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Lowest Common Ancestor\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Lowest Common Ancestor\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #22

**UUID:** `6d0c42f9-92b9-5787-be77-ce2991853beb`  
**Difficulty:** Medium  
**Tags:** Binary Search  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Search in Rotated Sorted Array

**Category**: Search
**Difficulty**: Medium
**Tags**: Binary Search

## Problem Description

This is a medium level problem in the Search category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Search in Rotated Sorted Array\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Search in Rotated Sorted Array\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Search in Rotated Sorted Array\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Search in Rotated Sorted Array\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Search in Rotated Sorted Array\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #23

**UUID:** `8d5bba7d-a313-5819-a082-04de3903b81b`  
**Difficulty:** Hard  
**Tags:** Graph, BFS  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Word Ladder

**Category**: Graph
**Difficulty**: Hard
**Tags**: Graph, BFS

## Problem Description

This is a hard level problem in the Graph category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Word Ladder\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Word Ladder\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Word Ladder\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Word Ladder\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Word Ladder\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #24

**UUID:** `8ec3ec81-b0ea-5b29-86be-9ba3529d37ed`  
**Difficulty:** Medium  
**Tags:** Graph, Union Find  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Redundant Connection

**Category**: Graph
**Difficulty**: Medium
**Tags**: Graph, Union Find

## Problem Description

This is a medium level problem in the Graph category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Redundant Connection\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Redundant Connection\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Redundant Connection\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Redundant Connection\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Redundant Connection\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #25

**UUID:** `8fa28b81-896d-5a55-b468-f20cb73287af`  
**Difficulty:** Easy  
**Tags:** Array, Hash Table  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Contains Duplicate

**Category**: Array
**Difficulty**: Easy
**Tags**: Array, Hash Table

## Problem Description

This is a easy level problem in the Array category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Contains Duplicate\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Contains Duplicate\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Contains Duplicate\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Contains Duplicate\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Contains Duplicate\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #26

**UUID:** `91a260c5-a545-5006-943d-423b1b52cf18`  
**Difficulty:** Medium  
**Tags:** Array, DP  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Maximum Subarray

**Category**: Array
**Difficulty**: Medium
**Tags**: Array, DP

## Problem Description

This is a medium level problem in the Array category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Maximum Subarray\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Maximum Subarray\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Maximum Subarray\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Maximum Subarray\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Maximum Subarray\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "9\n-2 1 -3 4 -1 2 1 -5 4",
    "stdin": "9\n-2 1 -3 4 -1 2 1 -5 4",
    "output": "6",
    "stdout": "6",
    "expected_output": "6"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "5\n5 4 -1 7 8",
    "stdin": "5\n5 4 -1 7 8",
    "output": "23",
    "stdout": "23",
    "expected_output": "23"
  }
]
```

### Test Cases

```json
[
  {
    "input": "9\n-2 1 -3 4 -1 2 1 -5 4",
    "stdin": "9\n-2 1 -3 4 -1 2 1 -5 4",
    "output": "6",
    "stdout": "6",
    "expected_output": "6"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "5\n5 4 -1 7 8",
    "stdin": "5\n5 4 -1 7 8",
    "output": "23",
    "stdout": "23",
    "expected_output": "23"
  },
  {
    "input": "3\n-1 -2 -3",
    "stdin": "3\n-1 -2 -3",
    "output": "-1",
    "stdout": "-1",
    "expected_output": "-1"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "1\n-5",
    "stdin": "1\n-5",
    "output": "-5",
    "stdout": "-5",
    "expected_output": "-5"
  },
  {
    "input": "2\n-1 0",
    "stdin": "2\n-1 0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "3\n0 0 0",
    "stdin": "3\n0 0 0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n-50 -49 -48 -47 -46 -45 -44 -43 -42 -41 -40 -39 -38 -37 -36 -35 -34 -33 -32 -31 -30 -29 -28 -27 -26 -25 -24 -23 -22 -21 -20 -19 -18 -17 -16 -15 -14 -13 -12 -11 -10 -9 -8 -7 -6 -5 -4 -3 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49",
    "stdin": "100\n-50 -49 -48 -47 -46 -45 -44 -43 -42 -41 -40 -39 -38 -37 -36 -35 -34 -33 -32 -31 -30 -29 -28 -27 -26 -25 -24 -23 -22 -21 -20 -19 -18 -17 -16 -15 -14 -13 -12 -11 -10 -9 -8 -7 -6 -5 -4 -3 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49",
    "output": "3725",
    "stdout": "3725",
    "expected_output": "3725"
  },
  {
    "input": "200\n-50 -49 -48 -47 -46 -45 -44 -43 -42 -41 -40 -39 -38 -37 -36 -35 -34 -33 -32 -31 -30 -29 -28 -27 -26 -25 -24 -23 -22 -21 -20 -19 -18 -17 -16 -15 -14 -13 -12 -11 -10 -9 -8 -7 -6 -5 -4 -3 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149",
    "stdin": "200\n-50 -49 -48 -47 -46 -45 -44 -43 -42 -41 -40 -39 -38 -37 -36 -35 -34 -33 -32 -31 -30 -29 -28 -27 -26 -25 -24 -23 -22 -21 -20 -19 -18 -17 -16 -15 -14 -13 -12 -11 -10 -9 -8 -7 -6 -5 -4 -3 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149",
    "output": "8725",
    "stdout": "8725",
    "expected_output": "8725"
  },
  {
    "input": "500\n-50 -49 -48 -47 -46 -45 -44 -43 -42 -41 -40 -39 -38 -37 -36 -35 -34 -33 -32 -31 -30 -29 -28 -27 -26 -25 -24 -23 -22 -21 -20 -19 -18 -17 -16 -15 -14 -13 -12 -11 -10 -9 -8 -7 -6 -5 -4 -3 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 377 378 379 380 381 382 383 384 385 386 387 388 389 390 391 392 393 394 395 396 397 398 399 400 401 402 403 404 405 406 407 408 409 410 411 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 430 431 432 433 434 435 436 437 438 439 440 441 442 443 444 445 446 447 448 449",
    "stdin": "500\n-50 -49 -48 -47 -46 -45 -44 -43 -42 -41 -40 -39 -38 -37 -36 -35 -34 -33 -32 -31 -30 -29 -28 -27 -26 -25 -24 -23 -22 -21 -20 -19 -18 -17 -16 -15 -14 -13 -12 -11 -10 -9 -8 -7 -6 -5 -4 -3 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 377 378 379 380 381 382 383 384 385 386 387 388 389 390 391 392 393 394 395 396 397 398 399 400 401 402 403 404 405 406 407 408 409 410 411 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 430 431 432 433 434 435 436 437 438 439 440 441 442 443 444 445 446 447 448 449",
    "output": "23725",
    "stdout": "23725",
    "expected_output": "23725"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #27

**UUID:** `9409b5fd-4178-584e-82b5-e6a87a23bd5c`  
**Difficulty:** Easy  
**Tags:** DP  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Climbing Stairs

**Category**: DP
**Difficulty**: Easy
**Tags**: DP

## Problem Description

This is a easy level problem in the DP category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Climbing Stairs\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Climbing Stairs\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Climbing Stairs\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Climbing Stairs\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Climbing Stairs\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #28

**UUID:** `94e6cd41-5a91-500c-af2e-3830c69684f2`  
**Difficulty:** Medium  
**Tags:** Tree, BFS  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Binary Tree Level Order Traversal

**Category**: Tree
**Difficulty**: Medium
**Tags**: Tree, BFS

## Problem Description

This is a medium level problem in the Tree category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Binary Tree Level Order Traversal\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Binary Tree Level Order Traversal\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Binary Tree Level Order Traversal\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Binary Tree Level Order Traversal\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Binary Tree Level Order Traversal\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #29

**UUID:** `a6de0595-5d05-50ed-8f3d-3d5fc29b4e2d`  
**Difficulty:** Hard  
**Tags:** DP, String  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Edit Distance

**Category**: DP
**Difficulty**: Hard
**Tags**: DP, String

## Problem Description

This is a hard level problem in the DP category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Edit Distance\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Edit Distance\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Edit Distance\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Edit Distance\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Edit Distance\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #30

**UUID:** `a7caa176-56ec-5153-b68e-7437d323d7cf`  
**Difficulty:** Medium  
**Tags:** Queue, Design  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Design Circular Queue

**Category**: Queue
**Difficulty**: Medium
**Tags**: Queue, Design

## Problem Description

This is a medium level problem in the Queue category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Design Circular Queue\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Design Circular Queue\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Design Circular Queue\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Design Circular Queue\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Design Circular Queue\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #31

**UUID:** `acc88182-5e1a-5d9f-b8f3-eb90b1ff90d3`  
**Difficulty:** Medium  
**Tags:** Heap, Quick Select  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Kth Largest Element

**Category**: Search
**Difficulty**: Medium
**Tags**: Heap, Quick Select

## Problem Description

This is a medium level problem in the Search category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Kth Largest Element\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Kth Largest Element\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Kth Largest Element\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Kth Largest Element\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Kth Largest Element\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #32

**UUID:** `b17d65f4-deda-578e-a612-ebe48d169746`  
**Difficulty:** Hard  
**Tags:** Backtracking, Recursion  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Sudoku Solver

**Category**: Backtracking
**Difficulty**: Hard
**Tags**: Backtracking, Recursion

## Problem Description

This is a hard level problem in the Backtracking category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Sudoku Solver\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Sudoku Solver\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Sudoku Solver\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Sudoku Solver\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Sudoku Solver\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #33

**UUID:** `b410a9c2-4190-5d1f-9401-ab6bd31f785b`  
**Difficulty:** Medium  
**Tags:** Graph, DFS  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Number of Islands

**Category**: Graph
**Difficulty**: Medium
**Tags**: Graph, DFS

## Problem Description

This is a medium level problem in the Graph category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Number of Islands\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Number of Islands\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Number of Islands\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Number of Islands\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Number of Islands\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #34

**UUID:** `b986f150-0ab7-5d1c-adfb-f29b305adde4`  
**Difficulty:** Medium  
**Tags:** Backtracking, Recursion  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Generate Parentheses

**Category**: Backtracking
**Difficulty**: Medium
**Tags**: Backtracking, Recursion

## Problem Description

This is a medium level problem in the Backtracking category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Generate Parentheses\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Generate Parentheses\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Generate Parentheses\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Generate Parentheses\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Generate Parentheses\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #35

**UUID:** `bf608792-1ccf-5c1a-b939-20aeb785279a`  
**Difficulty:** Easy  
**Tags:** Array, Greedy  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Best Time to Buy and Sell Stock

**Category**: Array
**Difficulty**: Easy
**Tags**: Array, Greedy

## Problem Description

This is a easy level problem in the Array category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Best Time to Buy and Sell Stock\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Best Time to Buy and Sell Stock\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Best Time to Buy and Sell Stock\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Best Time to Buy and Sell Stock\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Best Time to Buy and Sell Stock\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #36

**UUID:** `ca10584c-9186-5d5a-bfda-4fc8f0b28355`  
**Difficulty:** Medium  
**Tags:** Graph, BFS  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Cheapest Flights Within K Stops

**Category**: Graph
**Difficulty**: Medium
**Tags**: Graph, BFS

## Problem Description

This is a medium level problem in the Graph category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Cheapest Flights Within K Stops\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Cheapest Flights Within K Stops\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Cheapest Flights Within K Stops\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Cheapest Flights Within K Stops\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Cheapest Flights Within K Stops\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #37

**UUID:** `cdc38d05-83ab-5bb8-adf4-23a2a37cec23`  
**Difficulty:** Medium  
**Tags:** DP, String  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Longest Common Subsequence

**Category**: DP
**Difficulty**: Medium
**Tags**: DP, String

## Problem Description

This is a medium level problem in the DP category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Longest Common Subsequence\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Longest Common Subsequence\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Longest Common Subsequence\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Longest Common Subsequence\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Longest Common Subsequence\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #38

**UUID:** `d185e109-0475-50ab-b9c1-c1a2b93efc12`  
**Difficulty:** Easy  
**Tags:** String, Stack  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Valid Parentheses

**Category**: String
**Difficulty**: Easy
**Tags**: String, Stack

## Problem Description

This is a easy level problem in the String category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Valid Parentheses\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Valid Parentheses\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Valid Parentheses\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Valid Parentheses\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Valid Parentheses\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #39

**UUID:** `d69847e4-e253-4400-9e44-febff93aeb3a`  
**Difficulty:** medium  
**Tags:** array, greedy, simulation  
**Sample Test Cases:** 0  
**Test Cases:** 0  

### Question Description

<h3>Problem</h3>
<p>A warehouse manager needs to organize boxes stored in a single row. Each box has a different weight, and they are positioned sequentially from position 0 to n-1.</p>

<p>The manager has a forklift that can lift a group of three consecutive boxes simultaneously. The removal process works as follows:</p>
<ul>
    <li>In each operation, locate the box with the smallest weight value</li>
    <li>Use the forklift to remove that box together with its immediate neighbors on both sides (if available)</li>
    <li>Repeat this procedure until all boxes have been removed from the warehouse</li>
</ul>

<p>When multiple boxes share the same minimum weight, the manager chooses the one appearing earliest in the sequence. If a box is at the edge and doesn't have neighbors on both sides, only the available adjacent boxes are removed.</p>

<p><strong>Calculate the total sum of the minimum-weight boxes selected in each removal operation.</strong></p>

<h3>Example</h3>
<p>Consider a warehouse with 5 boxes having weights: [5, 4, 1, 3, 2].</p>
<ol>
    <li>Step 1: The smallest weight is 1 (at position 2). Remove boxes at positions 1, 2, and 3 (weights 4, 1, 3). Add 1 to the total. Remaining boxes: [5, 2].</li>
    <li>Step 2: The smallest weight is 2 (at position 1). Remove boxes at positions 0 and 1 (weights 5, 2). Add 2 to the total. No boxes remain.</li>
</ol>
<p>Final result: 1 + 2 = 3.</p>

<h3>Function Description</h3>
<p>Implement the function <code>findTotalWeight</code> which takes:</p>
<ul>
    <li><code>vector&lt;int&gt; boxes</code> (or equivalent): an array representing the weights of boxes in the warehouse</li>
</ul>
<p><strong>Returns:</strong> <code>int</code>: the cumulative sum of minimum-weight boxes from each removal step</p>

<h3>Constraints</h3>
<ul>
    <li>3 ≤ number of boxes ≤ 2000</li>
    <li>1 ≤ box weight ≤ 100,000</li>
</ul>

### Boilerplate Code

```
{"cpp": "#include <bits/stdc++.h>\n\nusing namespace std;\n\nstring ltrim(const string &);\nstring rtrim(const string &);\n\nint findTotalWeight(vector<int> cans) {\n    // TODO: Implement your solution here\n}\n\nint main()\n{\n    string cans_count_temp;\n    getline(cin, cans_count_temp);\n    int cans_count = stoi(ltrim(rtrim(cans_count_temp)));\n    vector<int> cans(cans_count);\n    for (int i = 0; i < cans_count; i++) {\n        string cans_item_temp;\n        getline(cin, cans_item_temp);\n        int cans_item = stoi(ltrim(rtrim(cans_item_temp)));\n        cans[i] = cans_item;\n    }\n    int result = findTotalWeight(cans);\n    cout << result << \"\\n\";\n    return 0;\n}\n\nstring ltrim(const string &str) {\n    string s(str);\n    s.erase(s.begin(), find_if(s.begin(), s.end(), not1(ptr_fun<int, int>(isspace))));\n    return s;\n}\n\nstring rtrim(const string &str) {\n    string s(str);\n    s.erase(find_if(s.rbegin(), s.rend(), not1(ptr_fun<int, int>(isspace))).base(), s.end());\n    return s;\n}", "python": "#!/bin/python3\nimport math\nimport os\nimport random\nimport re\nimport sys\n\ndef findTotalWeight(cans):\n    # TODO: Implement your solution here\n    pass\n\nif __name__ == '__main__':\n    cans_count = int(input().strip())\n    cans = []\n    for _ in range(cans_count):\n        cans_item = int(input().strip())\n        cans.append(cans_item)\n    result = findTotalWeight(cans)\n    print(result)", "java": "import java.io.*;\nimport java.math.*;\nimport java.security.*;\nimport java.text.*;\nimport java.util.*;\nimport java.util.concurrent.*;\nimport java.util.function.*;\nimport java.util.regex.*;\nimport java.util.stream.*;\nimport static java.util.stream.Collectors.joining;\nimport static java.util.stream.Collectors.toList;\n\npublic class Result {\n    public static int findTotalWeight(List<Integer> cans) {\n        // TODO: Implement your solution here\n        return 0;\n    }\n    \n    public static void main(String[] args) throws IOException {\n        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(System.in));\n        int cansCount = Integer.parseInt(bufferedReader.readLine().trim());\n        List<Integer> cans = new ArrayList<>();\n        for (int i = 0; i < cansCount; i++) {\n            int cansItem = Integer.parseInt(bufferedReader.readLine().trim());\n            cans.add(cansItem);\n        }\n        int result = findTotalWeight(cans);\n        System.out.println(result);\n        bufferedReader.close();\n    }\n}", "javascript": "function findTotalWeight(cans) {\n    // TODO: Implement your solution here\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({\n    input: process.stdin,\n    output: process.stdout\n});\n\nconst lines = [];\nrl.on('line', (line) => {\n    lines.push(parseInt(line.trim()));\n    if (lines.length === lines[0] + 1) {\n        const n = lines[0];\n        const cans = lines.slice(1);\n        const result = findTotalWeight(cans);\n        console.log(result);\n        rl.close();\n    }\n});"}
```

---

## Question #40

**UUID:** `d82b5bd1-0d71-51b6-97d8-9b13ad6a2d44`  
**Difficulty:** Medium  
**Tags:** Graph, DFS  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Clone Graph

**Category**: Graph
**Difficulty**: Medium
**Tags**: Graph, DFS

## Problem Description

This is a medium level problem in the Graph category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Clone Graph\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Clone Graph\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Clone Graph\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Clone Graph\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Clone Graph\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #41

**UUID:** `da618127-65b9-536e-a8aa-55e1c119a58c`  
**Difficulty:** Easy  
**Tags:** LinkedList  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Merge Two Sorted Lists

**Category**: LinkedList
**Difficulty**: Easy
**Tags**: LinkedList

## Problem Description

This is a easy level problem in the LinkedList category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Merge Two Sorted Lists\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Merge Two Sorted Lists\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Merge Two Sorted Lists\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Merge Two Sorted Lists\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Merge Two Sorted Lists\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #42

**UUID:** `daa3f2c6-ef17-5990-9710-f0a41202557f`  
**Difficulty:** Medium  
**Tags:** DP  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Coin Change

**Category**: DP
**Difficulty**: Medium
**Tags**: DP

## Problem Description

This is a medium level problem in the DP category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Coin Change\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Coin Change\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Coin Change\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Coin Change\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Coin Change\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #43

**UUID:** `df745d63-509a-526b-9075-37cbe4db07cc`  
**Difficulty:** Medium  
**Tags:** DP, Binary Search  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Longest Increasing Subsequence

**Category**: DP
**Difficulty**: Medium
**Tags**: DP, Binary Search

## Problem Description

This is a medium level problem in the DP category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Longest Increasing Subsequence\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Longest Increasing Subsequence\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Longest Increasing Subsequence\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Longest Increasing Subsequence\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Longest Increasing Subsequence\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #44

**UUID:** `e1248aef-d979-50c3-8982-197d95a2d9dd`  
**Difficulty:** Easy  
**Tags:** Binary Search  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Binary Search

**Category**: Search
**Difficulty**: Easy
**Tags**: Binary Search

## Problem Description

This is a easy level problem in the Search category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Binary Search\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Binary Search\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Binary Search\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Binary Search\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Binary Search\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #45

**UUID:** `e1a86b16-3055-5da8-94af-9e321765bc48`  
**Difficulty:** Medium  
**Tags:** DP, String  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Decode Ways

**Category**: DP
**Difficulty**: Medium
**Tags**: DP, String

## Problem Description

This is a medium level problem in the DP category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Decode Ways\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Decode Ways\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Decode Ways\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Decode Ways\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Decode Ways\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #46

**UUID:** `e856c67b-80c3-53a1-8808-171319c9db7b`  
**Difficulty:** Easy  
**Tags:** Tree, DFS  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Invert Binary Tree

**Category**: Tree
**Difficulty**: Easy
**Tags**: Tree, DFS

## Problem Description

This is a easy level problem in the Tree category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Invert Binary Tree\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Invert Binary Tree\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Invert Binary Tree\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Invert Binary Tree\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Invert Binary Tree\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #47

**UUID:** `e980271d-5bab-5c1d-acbb-412a2c2a765e`  
**Difficulty:** Easy  
**Tags:** LinkedList, Two Pointers  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Linked List Cycle

**Category**: LinkedList
**Difficulty**: Easy
**Tags**: LinkedList, Two Pointers

## Problem Description

This is a easy level problem in the LinkedList category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Linked List Cycle\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Linked List Cycle\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Linked List Cycle\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Linked List Cycle\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Linked List Cycle\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #48

**UUID:** `ea423368-fa6d-5b9d-bd2a-d01360af1086`  
**Difficulty:** Medium  
**Tags:** DP  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Unique Paths

**Category**: DP
**Difficulty**: Medium
**Tags**: DP

## Problem Description

This is a medium level problem in the DP category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Unique Paths\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Unique Paths\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Unique Paths\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Unique Paths\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Unique Paths\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #49

**UUID:** `ead7b506-1d71-525a-bf2a-365bca2ec7e4`  
**Difficulty:** Medium  
**Tags:** LinkedList, Two Pointers  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Remove Nth Node From End

**Category**: LinkedList
**Difficulty**: Medium
**Tags**: LinkedList, Two Pointers

## Problem Description

This is a medium level problem in the LinkedList category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Remove Nth Node From End\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Remove Nth Node From End\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Remove Nth Node From End\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Remove Nth Node From End\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Remove Nth Node From End\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #50

**UUID:** `ec6f733a-2824-5634-9bb2-43660b4d3aa4`  
**Difficulty:** Easy  
**Tags:** Tree, DFS  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Maximum Depth of Binary Tree

**Category**: Tree
**Difficulty**: Easy
**Tags**: Tree, DFS

## Problem Description

This is a easy level problem in the Tree category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Maximum Depth of Binary Tree\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Maximum Depth of Binary Tree\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Maximum Depth of Binary Tree\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Maximum Depth of Binary Tree\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Maximum Depth of Binary Tree\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #51

**UUID:** `f1579b4e-ec6f-5140-a15b-0026d5bd9f92`  
**Difficulty:** Medium  
**Tags:** Stack, Monotonic Stack  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Daily Temperatures

**Category**: Stack
**Difficulty**: Medium
**Tags**: Stack, Monotonic Stack

## Problem Description

This is a medium level problem in the Stack category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Daily Temperatures\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Daily Temperatures\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Daily Temperatures\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Daily Temperatures\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Daily Temperatures\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---

## Question #52

**UUID:** `fa5a65b1-b5f3-5f20-a8d9-22abccce4bf5`  
**Difficulty:** Medium  
**Tags:** Graph, Dijkstra  
**Sample Test Cases:** 3  
**Test Cases:** 20  

### Question Description

# Network Delay Time

**Category**: Graph
**Difficulty**: Medium
**Tags**: Graph, Dijkstra

## Problem Description

This is a medium level problem in the Graph category.

Given the problem constraints, implement an efficient solution.

## Examples

### Example 1
**Input**: 
```
Sample input
```
**Output**: 
```
Sample output
```

## Constraints
- Think about edge cases
- Consider time and space complexity
- Optimize your solution


### Boilerplate Code

```
{"cpp":"#include <iostream>\n#include <vector>\nusing namespace std;\n\nint solve() {\n    // Your code here for Network Delay Time\n    return 0;\n}\n\nint main() {\n    int n;\n    cin >> n;\n    cout << solve() << endl;\n    return 0;\n}\n","csharp":"using System;\nusing System.Linq;\n\npublic class Solution {\n    public int Solve() {\n        // Your code here for Network Delay Time\n        return 0;\n    }\n    \n    public static void Main() {\n        int n = int.Parse(Console.ReadLine());\n        Solution sol = new Solution();\n        Console.WriteLine(sol.Solve());\n    }\n}\n","java":"import java.util.*;\n\npublic class Solution {\n    public int solve() {\n        // Your code here for Network Delay Time\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        int n = sc.nextInt();\n        Solution sol = new Solution();\n        System.out.println(sol.solve());\n    }\n}\n","javascript":"function solve() {\n    // Your code here for Network Delay Time\n    return 0;\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin, output: process.stdout});\nrl.on('line', (line) => {\n    const n = parseInt(line);\n    console.log(solve());\n    rl.close();\n});\n","python":"def solve():\n    # Your code here for Network Delay Time\n    pass\n\n# Read input and call solve\nn = int(input())\nprint(solve())\n"}
```

### Sample Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  }
]
```

### Test Cases

```json
[
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "2\n1 2",
    "stdin": "2\n1 2",
    "output": "2",
    "stdout": "2",
    "expected_output": "2"
  },
  {
    "input": "3\n1 2 3",
    "stdin": "3\n1 2 3",
    "output": "3",
    "stdout": "3",
    "expected_output": "3"
  },
  {
    "input": "4\n1 2 3 4",
    "stdin": "4\n1 2 3 4",
    "output": "4",
    "stdout": "4",
    "expected_output": "4"
  },
  {
    "input": "5\n1 2 3 4 5",
    "stdin": "5\n1 2 3 4 5",
    "output": "5",
    "stdout": "5",
    "expected_output": "5"
  },
  {
    "input": "1\n1",
    "stdin": "1\n1",
    "output": "1",
    "stdout": "1",
    "expected_output": "1"
  },
  {
    "input": "0",
    "stdin": "0",
    "output": "0",
    "stdout": "0",
    "expected_output": "0"
  },
  {
    "input": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "stdin": "100\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99",
    "output": "100",
    "stdout": "100",
    "expected_output": "100"
  },
  {
    "input": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "stdin": "200\n0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199",
    "output": "200",
    "stdout": "200",
    "expected_output": "200"
  },
  {
    "input": "10\n1 2 3 4 5 6 7 8 9 10",
    "stdin": "10\n1 2 3 4 5 6 7 8 9 10",
    "output": "10",
    "stdout": "10",
    "expected_output": "10"
  },
  {
    "input": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "stdin": "11\n1 2 3 4 5 6 7 8 9 10 11",
    "output": "11",
    "stdout": "11",
    "expected_output": "11"
  },
  {
    "input": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "stdin": "12\n1 2 3 4 5 6 7 8 9 10 11 12",
    "output": "12",
    "stdout": "12",
    "expected_output": "12"
  },
  {
    "input": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "stdin": "13\n1 2 3 4 5 6 7 8 9 10 11 12 13",
    "output": "13",
    "stdout": "13",
    "expected_output": "13"
  },
  {
    "input": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "stdin": "14\n1 2 3 4 5 6 7 8 9 10 11 12 13 14",
    "output": "14",
    "stdout": "14",
    "expected_output": "14"
  },
  {
    "input": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "stdin": "15\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
    "output": "15",
    "stdout": "15",
    "expected_output": "15"
  },
  {
    "input": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "stdin": "16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16",
    "output": "16",
    "stdout": "16",
    "expected_output": "16"
  },
  {
    "input": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "stdin": "17\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17",
    "output": "17",
    "stdout": "17",
    "expected_output": "17"
  },
  {
    "input": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "stdin": "18\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18",
    "output": "18",
    "stdout": "18",
    "expected_output": "18"
  },
  {
    "input": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "stdin": "19\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19",
    "output": "19",
    "stdout": "19",
    "expected_output": "19"
  },
  {
    "input": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "stdin": "20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
    "output": "20",
    "stdout": "20",
    "expected_output": "20"
  }
]
```

---
