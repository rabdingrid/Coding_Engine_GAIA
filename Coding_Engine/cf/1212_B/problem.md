# Two-gram

## Rating: 900
## Tags: *special, implementation

## Description
Two-gram is an ordered pair (i.e. string of length two) of capital Latin letters. For example, "AZ", "AA", "ZA" — three distinct two-grams.

You are given a string $$$s$$$ consisting of $$$n$$$ capital Latin letters. Your task is to find any two-gram contained in the given string as a substring (i.e. two consecutive characters of the string) maximal number of times. For example, for string $$$s$$$ = "BBAABBBA" the answer is two-gram "BB", which contained in $$$s$$$ three times. In other words, find any most frequent two-gram.

Note that occurrences of the two-gram can overlap with each other.

## Input Format
The first line of the input contains integer number $$$n$$$ ($$$2 \le n \le 100$$$) — the length of string $$$s$$$. The second line of the input contains the string $$$s$$$ consisting of $$$n$$$ capital Latin letters.

## Output Format
Print the only line containing exactly two capital Latin letters — any two-gram contained in the given string $$$s$$$ as a substring (i.e. two consecutive characters of the string) maximal number of times.

## Examples

### Example 1
**Input:**
```
7
ABACABA
```
**Output:**
```
AB
```

### Example 2
**Input:**
```
5
ZZZAA
```
**Output:**
```
ZZ
```
