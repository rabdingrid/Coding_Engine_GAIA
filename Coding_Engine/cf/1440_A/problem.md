# Buy the String

## Rating: 800
## Tags: implementation, math

## Description
You are given four integers $$$n$$$, $$$c_0$$$, $$$c_1$$$ and $$$h$$$ and a binary string $$$s$$$ of length $$$n$$$.

A binary string is a string consisting of characters $$$0$$$ and $$$1$$$.

You can change any character of the string $$$s$$$ (the string should be still binary after the change). You should pay $$$h$$$ coins for each change.

After some changes (possibly zero) you want to buy the string. To buy the string you should buy all its characters. To buy the character $$$0$$$ you should pay $$$c_0$$$ coins, to buy the character $$$1$$$ you should pay $$$c_1$$$ coins.

Find the minimum number of coins needed to buy the string.

## Input Format
The first line contains a single integer $$$t$$$ ($$$1 \leq t \leq 10$$$) — the number of test cases. Next $$$2t$$$ lines contain descriptions of test cases.

The first line of the description of each test case contains four integers $$$n$$$, $$$c_{0}$$$, $$$c_{1}$$$, $$$h$$$ ($$$1 \leq n, c_{0}, c_{1}, h \leq 1000$$$).

The second line of the description of each test case contains the binary string $$$s$$$ of length $$$n$$$.

## Output Format
For each test case print a single integer — the minimum number of coins needed to buy the string.

## Examples

### Example 1
**Input:**
```
6
3 1 1 1
100
5 10 100 1
01010
5 10 1 1
11111
5 1 10 1
11111
12 2 1 10
101110110101
2 100 1 10
00
```
**Output:**
```
3
52
5
10
16
22
```
