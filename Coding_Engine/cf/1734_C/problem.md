# Removing Smallest Multiples

## Rating: 1200
## Tags: greedy, math

## Description
You are given a set $$$S$$$, which contains the first $$$n$$$ positive integers: $$$1, 2, \ldots, n$$$.

You can perform the following operation on $$$S$$$ any number of times (possibly zero):

- Choose a positive integer $$$k$$$ where $$$1 \le k \le n$$$, such that there exists a multiple of $$$k$$$ in $$$S$$$. Then, delete the smallest multiple of $$$k$$$ from $$$S$$$. This operation requires a cost of $$$k$$$.

You are given a set $$$T$$$, which is a subset of $$$S$$$. Find the minimum possible total cost of operations such that $$$S$$$ would be transformed into $$$T$$$. We can show that such a transformation is always possible.

## Input Format
The first line of the input contains a single integer $$$t$$$ ($$$1 \le t \le 10\,000$$$) — the number of test cases. The description of the test cases follows.

The first line contains a single positive integer $$$n$$$ ($$$1 \le n \le 10^6$$$).

The second line of each test case contains a binary string of length $$$n$$$, describing the set $$$T$$$. The $$$i$$$-th character of the string is '1' if and only if $$$i$$$ is an element of $$$T$$$, and '0' otherwise.

It is guaranteed that the sum of $$$n$$$ over all test cases does not exceed $$$10^6$$$.

## Output Format
For each test case, output one non-negative integer — the minimum possible total cost of operations such that $$$S$$$ would be transformed into $$$T$$$.

## Examples

### Example 1
**Input:**
```
6
6
111111
7
1101001
4
0000
4
0010
8
10010101
15
110011100101100
```
**Output:**
```
0
11
4
4
17
60
```
