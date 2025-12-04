// Script to add DSA questions to the database
// Run with: node add-dsa-questions.js

const { Pool } = require('pg');

const pool = new Pool({
  connectionString: process.env.DATABASE_URL || 'postgresql://postgresadmin:5oXcNX59QmEl7zmV3DbjemkiJ@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require',
  ssl: { rejectUnauthorized: false }
});

// DSA Questions with test cases
const dsaQuestions = [
  // ARRAY
  {
    title: 'Maximum Subarray',
    category: 'Array',
    difficulty: 'Medium',
    description: `Given an integer array nums, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.

A subarray is a contiguous part of an array.

Example 1:
Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: [4,-1,2,1] has the largest sum = 6.

Example 2:
Input: nums = [1]
Output: 1

Example 3:
Input: nums = [5,4,-1,7,8]
Output: 23`,
    testCases: [
      { input: '[-2,1,-3,4,-1,2,1,-5,4]', expected_output: '6' },
      { input: '[1]', expected_output: '1' },
      { input: '[5,4,-1,7,8]', expected_output: '23' },
      { input: '[-1]', expected_output: '-1' },
      { input: '[-2,-1]', expected_output: '-1' }
    ]
  },
  {
    title: 'Best Time to Buy and Sell Stock',
    category: 'Array',
    difficulty: 'Easy',
    description: `You are given an array prices where prices[i] is the price of a given stock on the ith day.

You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.

Example 1:
Input: prices = [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.

Example 2:
Input: prices = [7,6,4,3,1]
Output: 0
Explanation: In this case, no transactions are done and the max profit = 0.`,
    testCases: [
      { input: '[7,1,5,3,6,4]', expected_output: '5' },
      { input: '[7,6,4,3,1]', expected_output: '0' },
      { input: '[1,2,3,4,5]', expected_output: '4' },
      { input: '[2,4,1]', expected_output: '2' }
    ]
  },
  
  // LINKED LIST
  {
    title: 'Reverse Linked List',
    category: 'LinkedList',
    difficulty: 'Easy',
    description: `Given the head of a singly linked list, reverse the list, and return the reversed list.

Example 1:
Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]

Example 2:
Input: head = [1,2]
Output: [2,1]

Example 3:
Input: head = []
Output: []

Note: For this problem, you'll receive the linked list as an array and should return the reversed array.`,
    testCases: [
      { input: '[1,2,3,4,5]', expected_output: '[5,4,3,2,1]' },
      { input: '[1,2]', expected_output: '[2,1]' },
      { input: '[]', expected_output: '[]' },
      { input: '[1]', expected_output: '[1]' }
    ]
  },
  {
    title: 'Merge Two Sorted Lists',
    category: 'LinkedList',
    difficulty: 'Easy',
    description: `You are given the heads of two sorted linked lists list1 and list2.

Merge the two lists in a one sorted list. The list should be made by splicing together the nodes of the first two lists.

Return the head of the merged linked list.

Example 1:
Input: list1 = [1,2,4], list2 = [1,3,4]
Output: [1,1,2,3,4,4]

Example 2:
Input: list1 = [], list2 = []
Output: []

Example 3:
Input: list1 = [], list2 = [0]
Output: [0]

Note: For this problem, you'll receive two arrays and should return the merged sorted array.`,
    testCases: [
      { input: '[1,2,4]\n[1,3,4]', expected_output: '[1,1,2,3,4,4]' },
      { input: '[]\n[]', expected_output: '[]' },
      { input: '[]\n[0]', expected_output: '[0]' },
      { input: '[1]\n[2]', expected_output: '[1,2]' }
    ]
  },
  
  // STACK
  {
    title: 'Valid Parentheses',
    category: 'Stack',
    difficulty: 'Easy',
    description: `Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

Example 1:
Input: s = "()"
Output: true

Example 2:
Input: s = "()[]{}"
Output: true

Example 3:
Input: s = "(]"
Output: false

Example 4:
Input: s = "([)]"
Output: false

Example 5:
Input: s = "{[]}"
Output: true`,
    testCases: [
      { input: '"()"', expected_output: 'true' },
      { input: '"()[]{}"', expected_output: 'true' },
      { input: '"(]"', expected_output: 'false' },
      { input: '"([)]"', expected_output: 'false' },
      { input: '"{[]}"', expected_output: 'true' },
      { input: '""', expected_output: 'true' }
    ]
  },
  {
    title: 'Daily Temperatures',
    category: 'Stack',
    difficulty: 'Medium',
    description: `Given an array of integers temperatures represents the daily temperatures, return an array answer such that answer[i] is the number of days you have to wait after the ith day to get a warmer temperature. If there is no future day for which this is possible, keep answer[i] == 0 instead.

Example 1:
Input: temperatures = [73,74,75,71,69,72,76,73]
Output: [1,1,4,2,1,1,0,0]

Example 2:
Input: temperatures = [30,40,50,60]
Output: [1,1,1,0]

Example 3:
Input: temperatures = [30,60,90]
Output: [1,1,0]`,
    testCases: [
      { input: '[73,74,75,71,69,72,76,73]', expected_output: '[1,1,4,2,1,1,0,0]' },
      { input: '[30,40,50,60]', expected_output: '[1,1,1,0]' },
      { input: '[30,60,90]', expected_output: '[1,1,0]' },
      { input: '[30]', expected_output: '[0]' }
    ]
  },
  
  // QUEUE
  {
    title: 'Design Circular Queue',
    category: 'Queue',
    difficulty: 'Medium',
    description: `Design your implementation of the circular queue. The circular queue is a linear data structure in which the operations are performed based on FIFO (First In First Out) principle and the last position is connected back to the first position to make a circle. It is also called "Ring Buffer".

Implement the MyCircularQueue class:
- MyCircularQueue(k) Initializes the object with the size of the queue to be k.
- int Front() Gets the front item from the queue. If the queue is empty, return -1.
- int Rear() Gets the last item from the queue. If the queue is empty, return -1.
- boolean enQueue(int value) Inserts an element into the circular queue. Return true if the operation is successful.
- boolean deQueue() Deletes an element from the circular queue. Return true if the operation is successful.
- boolean isEmpty() Checks whether the circular queue is empty.
- boolean isFull() Checks whether the circular queue is full.

For this problem, you'll implement a simple queue and return the front element after operations.

Example:
Input: ["MyCircularQueue","enQueue","enQueue","enQueue","enQueue","Rear","isFull","deQueue","enQueue","Rear"]
[[3],[1],[2],[3],[4],[],[],[],[4],[]]
Output: [null,true,true,true,false,3,true,true,true,4]`,
    testCases: [
      { input: '3\nenQueue 1\nenQueue 2\nenQueue 3\nFront', expected_output: '1' },
      { input: '3\nenQueue 1\nenQueue 2\ndeQueue\nFront', expected_output: '2' },
      { input: '2\nenQueue 1\nenQueue 2\nisFull', expected_output: 'true' }
    ]
  },
  
  // STRING
  {
    title: 'Longest Palindromic Substring',
    category: 'String',
    difficulty: 'Medium',
    description: `Given a string s, return the longest palindromic substring in s.

A string is called a palindrome if it reads the same backward as forward.

Example 1:
Input: s = "babad"
Output: "bab"
Explanation: "aba" is also a valid answer.

Example 2:
Input: s = "cbbd"
Output: "bb"

Example 3:
Input: s = "a"
Output: "a"`,
    testCases: [
      { input: '"babad"', expected_output: '"bab"' },
      { input: '"cbbd"', expected_output: '"bb"' },
      { input: '"a"', expected_output: '"a"' },
      { input: '"ac"', expected_output: '"a"' },
      { input: '"racecar"', expected_output: '"racecar"' }
    ]
  },
  {
    title: 'Longest Substring Without Repeating Characters',
    category: 'String',
    difficulty: 'Medium',
    description: `Given a string s, find the length of the longest substring without repeating characters.

Example 1:
Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.

Example 2:
Input: s = "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.

Example 3:
Input: s = "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3. Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.`,
    testCases: [
      { input: '"abcabcbb"', expected_output: '3' },
      { input: '"bbbbb"', expected_output: '1' },
      { input: '"pwwkew"', expected_output: '3' },
      { input: '""', expected_output: '0' },
      { input: '"dvdf"', expected_output: '3' }
    ]
  },
  
  // TREE
  {
    title: 'Maximum Depth of Binary Tree',
    category: 'Tree',
    difficulty: 'Easy',
    description: `Given the root of a binary tree, return its maximum depth.

A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

Example 1:
Input: root = [3,9,20,null,null,15,7]
Output: 3

Example 2:
Input: root = [1,null,2]
Output: 2

Note: For this problem, you'll receive the tree as an array representation and should return the maximum depth.`,
    testCases: [
      { input: '[3,9,20,null,null,15,7]', expected_output: '3' },
      { input: '[1,null,2]', expected_output: '2' },
      { input: '[]', expected_output: '0' },
      { input: '[1]', expected_output: '1' },
      { input: '[1,2,3,4,5]', expected_output: '3' }
    ]
  },
  {
    title: 'Same Tree',
    category: 'Tree',
    difficulty: 'Easy',
    description: `Given the roots of two binary trees p and q, write a function to check if they are the same or not.

Two binary trees are considered the same if they are structurally identical, and the nodes have the same value.

Example 1:
Input: p = [1,2,3], q = [1,2,3]
Output: true

Example 2:
Input: p = [1,2], q = [1,null,2]
Output: false

Example 3:
Input: p = [1,2,1], q = [1,1,2]
Output: false`,
    testCases: [
      { input: '[1,2,3]\n[1,2,3]', expected_output: 'true' },
      { input: '[1,2]\n[1,null,2]', expected_output: 'false' },
      { input: '[1,2,1]\n[1,1,2]', expected_output: 'false' },
      { input: '[]\n[]', expected_output: 'true' }
    ]
  },
  
  // GRAPH
  {
    title: 'Number of Islands',
    category: 'Graph',
    difficulty: 'Medium',
    description: `Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water), return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.

Example 1:
Input: grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
Output: 1

Example 2:
Input: grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
Output: 3

Note: For this problem, you'll receive the grid as a 2D array and should return the number of islands.`,
    testCases: [
      { input: '[["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]', expected_output: '1' },
      { input: '[["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]', expected_output: '3' },
      { input: '[["1"]]', expected_output: '1' },
      { input: '[["0"]]', expected_output: '0' }
    ]
  },
  {
    title: 'Clone Graph',
    category: 'Graph',
    difficulty: 'Medium',
    description: `Given a reference of a node in a connected undirected graph.

Return a deep copy (clone) of the graph.

Each node in the graph contains a value (int) and a list (List[Node]) of its neighbors.

For simplicity, you'll receive the graph as an adjacency list and should return the number of nodes.

Example 1:
Input: adjList = [[2,4],[1,3],[2,4],[1,3]]
Output: 4

Example 2:
Input: adjList = [[]]
Output: 1

Example 3:
Input: adjList = []
Output: 0`,
    testCases: [
      { input: '[[2,4],[1,3],[2,4],[1,3]]', expected_output: '4' },
      { input: '[[]]', expected_output: '1' },
      { input: '[]', expected_output: '0' }
    ]
  },
  
  // DYNAMIC PROGRAMMING
  {
    title: 'Climbing Stairs',
    category: 'DP',
    difficulty: 'Easy',
    description: `You are climbing a staircase. It takes n steps to reach the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

Example 1:
Input: n = 2
Output: 2
Explanation: There are two ways to climb to the top.
1. 1 step + 1 step
2. 2 steps

Example 2:
Input: n = 3
Output: 3
Explanation: There are three ways to climb to the top.
1. 1 step + 1 step + 1 step
2. 1 step + 2 steps
3. 2 steps + 1 step`,
    testCases: [
      { input: '2', expected_output: '2' },
      { input: '3', expected_output: '3' },
      { input: '4', expected_output: '5' },
      { input: '5', expected_output: '8' },
      { input: '1', expected_output: '1' }
    ]
  },
  {
    title: 'Coin Change',
    category: 'DP',
    difficulty: 'Medium',
    description: `You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money.

Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1.

You may assume that you have an infinite number of each kind of coin.

Example 1:
Input: coins = [1,2,5], amount = 11
Output: 3
Explanation: 11 = 5 + 5 + 1

Example 2:
Input: coins = [2], amount = 3
Output: -1

Example 3:
Input: coins = [1], amount = 0
Output: 0`,
    testCases: [
      { input: '[1,2,5]\n11', expected_output: '3' },
      { input: '[2]\n3', expected_output: '-1' },
      { input: '[1]\n0', expected_output: '0' },
      { input: '[1,2,5]\n6', expected_output: '2' }
    ]
  },
  {
    title: 'Longest Increasing Subsequence',
    category: 'DP',
    difficulty: 'Medium',
    description: `Given an integer array nums, return the length of the longest strictly increasing subsequence.

Example 1:
Input: nums = [10,9,2,5,3,7,101,18]
Output: 4
Explanation: The longest increasing subsequence is [2,3,7,18], therefore the length is 4.

Example 2:
Input: nums = [0,1,0,3,2,3]
Output: 4

Example 3:
Input: nums = [7,7,7,7,7,7,7]
Output: 1`,
    testCases: [
      { input: '[10,9,2,5,3,7,101,18]', expected_output: '4' },
      { input: '[0,1,0,3,2,3]', expected_output: '4' },
      { input: '[7,7,7,7,7,7,7]', expected_output: '1' },
      { input: '[1,3,6,7,9,4,10,5,6]', expected_output: '6' }
    ]
  }
];

async function addDSAQuestions() {
  try {
    console.log('🚀 Starting to add DSA questions...\n');

    let addedCount = 0;
    let skippedCount = 0;

    for (const question of dsaQuestions) {
      try {
        // Check if question already exists
        const existing = await pool.query(
          'SELECT id FROM questions WHERE title = $1',
          [question.title]
        );

        if (existing.rows.length > 0) {
          console.log(`⏭️  Skipping "${question.title}" (already exists)`);
          skippedCount++;
          continue;
        }

        // Add question to questions table
        const questionResult = await pool.query(
          `INSERT INTO questions (title, description, difficulty) 
           VALUES ($1, $2, $3) RETURNING *`,
          [question.title, question.description, question.difficulty]
        );

        const questionId = questionResult.rows[0].id;
        console.log(`✅ Added: "${question.title}" (${question.category}) - ID: ${questionId}`);

        // Add test cases
        for (let i = 0; i < question.testCases.length; i++) {
          const tc = question.testCases[i];
          await pool.query(
            `INSERT INTO test_cases (question_id, input, expected_output, test_order) 
             VALUES ($1, $2, $3, $4)`,
            [questionId, tc.input, tc.expected_output, i + 1]
          );
        }
        console.log(`   └─ Added ${question.testCases.length} test cases`);

        addedCount++;
      } catch (error) {
        console.error(`❌ Error adding "${question.title}":`, error.message);
      }
    }

    console.log('\n' + '='.repeat(50));
    console.log(`✅ Successfully added: ${addedCount} questions`);
    console.log(`⏭️  Skipped (already exist): ${skippedCount} questions`);
    console.log(`📊 Total questions in database now: ${addedCount + skippedCount}`);
    console.log('='.repeat(50));
    console.log('\n🎉 Done! Refresh your browser to see the new questions.');

    await pool.end();
  } catch (error) {
    console.error('❌ Fatal error:', error);
    await pool.end();
    process.exit(1);
  }
}

addDSAQuestions();


