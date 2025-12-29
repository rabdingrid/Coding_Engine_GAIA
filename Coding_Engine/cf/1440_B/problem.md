# Sum of Medians

## Rating: 900
## Tags: greedy, math

## Description
A median of an array of integers of length $$$n$$$ is the number standing on the $$$\lceil {\frac{n}{2}} \rceil$$$ (rounding up) position in the non-decreasing ordering of its elements. Positions are numbered starting with $$$1$$$. For example, a median of the array $$$[2, 6, 4, 1, 3, 5]$$$ is equal to $$$3$$$. There exist some other definitions of the median, but in this problem, we will use the described one.

Given two integers $$$n$$$ and $$$k$$$ and non-decreasing array of $$$nk$$$ integers. Divide all numbers into $$$k$$$ arrays of size $$$n$$$, such that each number belongs to exactly one array.

You want the sum of medians of all $$$k$$$ arrays to be the maximum possible. Find this maximum possible sum.

## Input Format
The first line contains a single integer $$$t$$$ ($$$1 \leq t \leq 100$$$) — the number of test cases. The next $$$2t$$$ lines contain descriptions of test cases.

The first line of the description of each test case contains two integers $$$n$$$, $$$k$$$ ($$$1 \leq n, k \leq 1000$$$).

The second line of the description of each test case contains $$$nk$$$ integers $$$a_1, a_2, \ldots, a_{nk}$$$ ($$$0 \leq a_i \leq 10^9$$$) — given array. It is guaranteed that the array is non-decreasing: $$$a_1 \leq a_2 \leq \ldots \leq a_{nk}$$$.

It is guaranteed that the sum of $$$nk$$$ for all test cases does not exceed $$$2 \cdot 10^5$$$.

## Output Format
For each test case print a single integer — the maximum possible sum of medians of all $$$k$$$ arrays.

## Examples

### Example 1
**Input:**
```
6
2 4
0 24 34 58 62 64 69 78
2 2
27 61 81 91
4 3
2 4 16 18 21 27 36 53 82 91 92 95
3 4
3 11 12 22 33 35 38 67 69 71 94 99
2 1
11 41
3 3
1 1 1 1 1 1 1 1 1
```
**Output:**
```
165
108
145
234
11
3
```
