# Implementation Plan: 50 DSA Questions with C# Support

## ✅ Completed

1. ✅ **File System Structure Created**
   - `dsa-questions/` directory structure
   - Question format: `Q001/`, `Q002/`, etc.
   - Each question has: `metadata.json`, `problem.md`, `test_cases/`, `boilerplates/`

2. ✅ **C# Language Support Added**
   - Added C# to executor-service-secure.py
   - Supports both `dotnet` and `mcs` (Mono) compilers
   - Added C# security patterns to blocked patterns
   - Updated supported languages list

3. ✅ **Import Script Created**
   - `IMPORT_TO_DB.js` - Imports questions from file system to database
   - Handles metadata, test cases, and boilerplates
   - Updates existing questions or creates new ones

## 🚧 In Progress

4. **Generate 50 DSA Questions**
   - Need to create comprehensive question generator
   - 50 questions across 8 categories
   - Each with 20+ test cases (basic, edge, long, corner cases)

5. **Enhanced TLE/MLE Detection**
   - Already added to C# function
   - Need to enhance for all languages (Python, Java, C++, JavaScript)

## 📋 Next Steps

### Step 1: Generate All 50 Questions

Create a comprehensive Python script that generates:
- **10 Array/String questions** (Q001-Q010)
- **5 Linked List questions** (Q011-Q015)
- **8 Tree/Binary Tree questions** (Q016-Q023)
- **7 Graph questions** (Q024-Q030)
- **8 Dynamic Programming questions** (Q031-Q038)
- **5 Recursion/Backtracking questions** (Q039-Q043)
- **4 Sorting/Searching questions** (Q044-Q047)
- **3 Stack/Queue questions** (Q048-Q050)

Each question needs:
- Proper metadata.json
- Comprehensive problem.md
- 20+ test cases (5-8 basic, 5-8 edge, 5-8 long, 2-4 corner)
- Boilerplates for all 5 languages (Python, Java, C++, JavaScript, C#)

### Step 2: Enhance TLE/MLE Detection

Update all execute functions to:
- Check execution time vs timeout
- Check memory usage vs MAX_MEMORY
- Return proper error messages: "Time Limit Exceeded (TLE)" or "Memory Limit Exceeded (MLE)"
- Detect infinite loops (CPU usage spikes)

### Step 3: Test Everything

1. Generate questions: `python3 generate-questions.py`
2. Import to database: `node IMPORT_TO_DB.js`
3. Test C# execution
4. Test TLE/MLE detection
5. Run load tests with new questions

## 🎯 Question Categories Breakdown

### Arrays & Strings (10 questions)
- Q001: Two Sum ✅ (example created)
- Q002: Maximum Subarray
- Q003: Longest Substring Without Repeating Characters
- Q004: Valid Parentheses
- Q005: Best Time to Buy and Sell Stock
- Q006: Contains Duplicate
- Q007: Product of Array Except Self
- Q008: Maximum Product Subarray
- Q009: Find All Anagrams in a String
- Q010: Group Anagrams

### Linked Lists (5 questions)
- Q011: Reverse Linked List
- Q012: Merge Two Sorted Lists
- Q013: Remove Nth Node From End
- Q014: Linked List Cycle
- Q015: Add Two Numbers

### Trees & Binary Trees (8 questions)
- Q016: Maximum Depth of Binary Tree
- Q017: Same Tree
- Q018: Invert Binary Tree
- Q019: Binary Tree Level Order Traversal
- Q020: Validate Binary Search Tree
- Q021: Path Sum
- Q022: Construct Binary Tree from Preorder and Inorder
- Q023: Lowest Common Ancestor

### Graphs (7 questions)
- Q024: Number of Islands
- Q025: Clone Graph
- Q026: Course Schedule
- Q027: Word Ladder
- Q028: Network Delay Time
- Q029: Cheapest Flights Within K Stops
- Q030: Redundant Connection

### Dynamic Programming (8 questions)
- Q031: Climbing Stairs
- Q032: Coin Change
- Q033: Longest Increasing Subsequence
- Q034: Longest Common Subsequence
- Q035: Edit Distance
- Q036: House Robber
- Q037: Decode Ways
- Q038: Unique Paths

### Recursion & Backtracking (5 questions)
- Q039: Generate Parentheses
- Q040: Combination Sum
- Q041: Permutations
- Q042: N-Queens
- Q043: Sudoku Solver

### Sorting & Searching (4 questions)
- Q044: Binary Search
- Q045: Search in Rotated Sorted Array
- Q046: Find First and Last Position
- Q047: Kth Largest Element

### Stack & Queue (3 questions)
- Q048: Daily Temperatures
- Q049: Design Circular Queue
- Q050: Largest Rectangle in Histogram

## 📝 Test Case Requirements

Each question needs **at least 20 test cases**:

1. **Basic Cases (5-8)**: Simple, straightforward inputs
2. **Edge Cases (5-8)**: Empty inputs, single element, max values, negative numbers
3. **Long Cases (5-8)**: Large inputs (arrays with 1000+ elements, strings with 10000+ chars)
4. **Corner Cases (2-4)**: Boundary conditions, special values

## 🔧 Usage

### Generate Questions:
```bash
cd dsa-questions
python3 generate-questions.py
```

### Import to Database:
```bash
node IMPORT_TO_DB.js
```

### Test C# Execution:
```bash
# Test with a simple C# program
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "code": "using System; class Program { static void Main() { Console.WriteLine(\"Hello C#\"); } }",
    "language": "csharp",
    "test_cases": [{"input": "", "expected_output": "Hello C#"}]
  }'
```

## ✅ Status

- [x] File system structure
- [x] C# language support
- [x] Import script
- [ ] 50 questions generator (in progress)
- [ ] Enhanced TLE/MLE for all languages
- [ ] Testing

