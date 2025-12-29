# Patchouli's Magical Talisman

## Rating: 800
## Tags: bitmasks, constructive algorithms, greedy, sortings

## Description
Patchouli is making a magical talisman. She initially has $$$n$$$ magical tokens. Their magical power can be represented with positive integers $$$a_1, a_2, \ldots, a_n$$$.

Patchouli may perform the following two operations on the tokens.

- Fusion: Patchouli chooses two tokens, removes them, and creates a new token with magical power equal to the sum of the two chosen tokens.
- Reduction: Patchouli chooses a token with an even value of magical power $$$x$$$, removes it and creates a new token with magical power equal to $$$\frac{x}{2}$$$.

Tokens are more effective when their magical powers are odd values. Please help Patchouli to find the minimum number of operations she needs to make magical powers of all tokens odd values.

## Input Format
Each test contains multiple test cases.

The first line contains a single integer $$$t$$$ ($$$1 \leq t \leq 10^3$$$) — the number of test cases. The description of the test cases follows.

For each test case, the first line contains one integer $$$n$$$ ($$$1 \leq n\leq 2\cdot 10^5$$$) — the initial number of tokens.

The second line contains $$$n$$$ intergers $$$a_1,a_2,\ldots,a_n$$$ ($$$1 \leq a_i \leq 10^9$$$) — the initial magical power of the $$$n$$$ tokens.

It is guaranteed that the sum of $$$n$$$ over all test cases does not exceed $$$2 \cdot 10^5$$$.

## Output Format
For each test case, print a single integer — the minimum number of operations Patchouli needs to make all tokens have an odd value of magical power.

It can be shown that under such restrictions the required sequence of operations exists.

## Examples

### Example 1
**Input:**
```
4
2
1 9
3
1 1 2
3
2 4 8
3
1049600 33792 1280
```
**Output:**
```
0
1
3
10
```
