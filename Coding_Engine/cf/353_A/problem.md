# Domino

## Rating: 1200
## Tags: implementation, math

## Description
Valera has got n domino pieces in a row. Each piece consists of two halves — the upper one and the lower one. Each of the halves contains a number from 1 to 6. Valera loves even integers very much, so he wants the sum of the numbers on the upper halves and the sum of the numbers on the lower halves to be even.

To do that, Valera can rotate the dominoes by 180 degrees. After the rotation the upper and the lower halves swap places. This action takes one second. Help Valera find out the minimum time he must spend rotating dominoes to make his wish come true.

## Input Format
The first line contains integer n (1 ≤ n ≤ 100), denoting the number of dominoes Valera has. Next n lines contain two space-separated integers xi, yi (1 ≤ xi, yi ≤ 6). Number xi is initially written on the upper half of the i-th domino, yi is initially written on the lower half.

## Output Format
Print a single number — the minimum required number of seconds. If Valera can't do the task in any time, print  - 1.

## Examples

### Example 1
**Input:**
```
2
4 2
6 4
```
**Output:**
```
0
```

### Example 2
**Input:**
```
1
2 3
```
**Output:**
```
-1
```

### Example 3
**Input:**
```
3
1 4
2 3
4 4
```
**Output:**
```
1
```
