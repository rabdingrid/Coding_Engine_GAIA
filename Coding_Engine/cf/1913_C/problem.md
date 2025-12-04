# Game with Multiset

## Rating: 1300
## Tags: binary search, bitmasks, brute force, greedy

## Description
In this problem, you are initially given an empty multiset. You have to process two types of queries:

1. ADD $$$x$$$ — add an element equal to $$$2^{x}$$$ to the multiset;
2. GET $$$w$$$ — say whether it is possible to take the sum of some subset of the current multiset and get a value equal to $$$w$$$.

## Input Format
The first line contains one integer $$$m$$$ ($$$1 \le m \le 10^5$$$) — the number of queries.

Then $$$m$$$ lines follow, each of which contains two integers $$$t_i$$$, $$$v_i$$$, denoting the $$$i$$$-th query. If $$$t_i = 1$$$, then the $$$i$$$-th query is ADD $$$v_i$$$ ($$$0 \le v_i \le 29$$$). If $$$t_i = 2$$$, then the $$$i$$$-th query is GET $$$v_i$$$ ($$$0 \le v_i \le 10^9$$$).

## Output Format
For each GET query, print YES if it is possible to choose a subset with sum equal to $$$w$$$, or NO if it is impossible.

## Examples

### Example 1
**Input:**
```
5
1 0
1 0
1 0
2 3
2 4
```
**Output:**
```
YES
NO
```

### Example 2
**Input:**
```
7
1 0
1 1
1 2
1 10
2 4
2 6
2 7
```
**Output:**
```
YES
YES
YES
```
