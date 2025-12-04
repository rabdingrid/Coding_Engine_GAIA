# Select Three Sticks

## Rating: 800
## Tags: brute force, greedy, sortings

## Description
You are given $$$n$$$ sticks with positive integral length $$$a_1, a_2, \ldots, a_n$$$.

You can perform the following operation any number of times (possibly zero):

- choose one stick, then either increase or decrease its length by $$$1$$$. After each operation, all sticks should have positive lengths.

What is the minimum number of operations that you have to perform such that it is possible to select three of the $$$n$$$ sticks and use them without breaking to form an equilateral triangle?

An equilateral triangle is a triangle where all of its three sides have the same length.

## Input Format
The first line of the input contains a single integer $$$t$$$ ($$$1 \le t \le 100$$$) — the number of test cases. The description of the test cases follows.

The first line of each test case contains a single integer $$$n$$$ ($$$3 \le n \le 300$$$) — the number of sticks.

The second line of each test case contains $$$n$$$ integers $$$a_1, a_2, \ldots, a_n$$$ ($$$1 \le a_i \le 10^9$$$) — the lengths of the sticks.

It is guaranteed that the sum of $$$n$$$ over all test cases does not exceed $$$300$$$.

## Output Format
For each test case, print one integer on a single line — the minimum number of operations to be made.

## Examples

### Example 1
**Input:**
```
4
3
1 2 3
4
7 3 7 3
5
3 4 2 1 1
8
3 1 4 1 5 9 2 6
```
**Output:**
```
2
4
1
1
```
