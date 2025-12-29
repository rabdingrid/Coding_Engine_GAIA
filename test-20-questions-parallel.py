#!/usr/bin/env python3
"""
Test 20 DSA Questions in Parallel
Each question has 10 test cases
Tests queue system and load distribution with 1 replica
"""

import json
import time
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

API_URL = "https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io"

# 20 DSA Questions with 10 test cases each
DSA_QUESTIONS = [
    {
        "id": "q1",
        "title": "Two Sum",
        "language": "python",
        "code": """def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

target = int(input())
nums = list(map(int, input().split()))
result = two_sum(nums, target)
print(' '.join(map(str, result)))""",
        "test_cases": [
            {"id": "t1", "input": "9\n2 7 11 15", "expected_output": "0 1"},
            {"id": "t2", "input": "6\n3 2 4", "expected_output": "1 2"},
            {"id": "t3", "input": "6\n3 3", "expected_output": "0 1"},
            {"id": "t4", "input": "10\n1 2 3 4 5", "expected_output": "0 4"},
            {"id": "t5", "input": "15\n5 10 3 7 2 8", "expected_output": "1 3"},
            {"id": "t6", "input": "8\n1 3 5 7", "expected_output": "0 3"},
            {"id": "t7", "input": "5\n1 2 3", "expected_output": "0 2"},
            {"id": "t8", "input": "20\n2 4 6 8 10 12 14", "expected_output": "2 5"},
            {"id": "t9", "input": "0\n-1 0 1 2 3", "expected_output": "0 1"},
            {"id": "t10", "input": "100\n10 20 30 70", "expected_output": "2 3"}
        ]
    },
    {
        "id": "q2",
        "title": "Reverse Linked List",
        "language": "python",
        "code": """class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head):
    prev = None
    current = head
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    return prev

def list_to_array(head):
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result

n = int(input())
values = list(map(int, input().split()))
head = None
for val in reversed(values):
    head = ListNode(val, head)

reversed_head = reverse_list(head)
result = list_to_array(reversed_head)
print(' '.join(map(str, result)))""",
        "test_cases": [
            {"id": "t1", "input": "5\n1 2 3 4 5", "expected_output": "5 4 3 2 1"},
            {"id": "t2", "input": "2\n1 2", "expected_output": "2 1"},
            {"id": "t3", "input": "1\n1", "expected_output": "1"},
            {"id": "t4", "input": "4\n10 20 30 40", "expected_output": "40 30 20 10"},
            {"id": "t5", "input": "3\n5 10 15", "expected_output": "15 10 5"},
            {"id": "t6", "input": "6\n1 2 3 4 5 6", "expected_output": "6 5 4 3 2 1"},
            {"id": "t7", "input": "7\n7 6 5 4 3 2 1", "expected_output": "1 2 3 4 5 6 7"},
            {"id": "t8", "input": "3\n100 200 300", "expected_output": "300 200 100"},
            {"id": "t9", "input": "2\n0 1", "expected_output": "1 0"},
            {"id": "t10", "input": "5\n-1 -2 -3 -4 -5", "expected_output": "-5 -4 -3 -2 -1"}
        ]
    },
    {
        "id": "q3",
        "title": "Binary Search",
        "language": "python",
        "code": """def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

n = int(input())
target = int(input())
arr = list(map(int, input().split()))
result = binary_search(arr, target)
print(result)""",
        "test_cases": [
            {"id": "t1", "input": "6\n5\n1 2 3 4 5 6", "expected_output": "4"},
            {"id": "t2", "input": "5\n3\n1 2 3 4 5", "expected_output": "2"},
            {"id": "t3", "input": "4\n1\n1 2 3 4", "expected_output": "0"},
            {"id": "t4", "input": "5\n10\n1 3 5 7 9", "expected_output": "-1"},
            {"id": "t5", "input": "7\n7\n1 2 3 4 5 6 7", "expected_output": "6"},
            {"id": "t6", "input": "3\n2\n1 2 3", "expected_output": "1"},
            {"id": "t7", "input": "8\n15\n5 10 15 20 25 30 35 40", "expected_output": "2"},
            {"id": "t8", "input": "4\n0\n1 2 3 4", "expected_output": "-1"},
            {"id": "t9", "input": "6\n6\n1 2 3 4 5 6", "expected_output": "5"},
            {"id": "t10", "input": "5\n1\n1 2 3 4 5", "expected_output": "0"}
        ]
    },
    {
        "id": "q4",
        "title": "Maximum Subarray Sum",
        "language": "python",
        "code": """def max_subarray_sum(nums):
    max_sum = current_sum = nums[0]
    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    return max_sum

n = int(input())
nums = list(map(int, input().split()))
result = max_subarray_sum(nums)
print(result)""",
        "test_cases": [
            {"id": "t1", "input": "5\n-2 1 -3 4 -1 2 1 -5 4", "expected_output": "6"},
            {"id": "t2", "input": "1\n1", "expected_output": "1"},
            {"id": "t3", "input": "5\n5 4 -1 7 8", "expected_output": "23"},
            {"id": "t4", "input": "3\n-1 -2 -3", "expected_output": "-1"},
            {"id": "t5", "input": "4\n1 2 3 4", "expected_output": "10"},
            {"id": "t6", "input": "6\n-2 -1 -3 -4 -5", "expected_output": "-1"},
            {"id": "t7", "input": "5\n1 -2 3 -4 5", "expected_output": "5"},
            {"id": "t8", "input": "7\n2 -1 3 -2 4 -1 5", "expected_output": "10"},
            {"id": "t9", "input": "3\n10 -5 8", "expected_output": "13"},
            {"id": "t10", "input": "4\n-1 2 -3 4", "expected_output": "4"}
        ]
    },
    {
        "id": "q5",
        "title": "Valid Parentheses",
        "language": "python",
        "code": """def is_valid(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    for char in s:
        if char in mapping:
            if not stack or stack.pop() != mapping[char]:
                return False
        else:
            stack.append(char)
    return not stack

s = input().strip()
result = is_valid(s)
print("true" if result else "false")""",
        "test_cases": [
            {"id": "t1", "input": "()", "expected_output": "true"},
            {"id": "t2", "input": "()[]{}", "expected_output": "true"},
            {"id": "t3", "input": "(]", "expected_output": "false"},
            {"id": "t4", "input": "([)]", "expected_output": "false"},
            {"id": "t5", "input": "{[]}", "expected_output": "true"},
            {"id": "t6", "input": "((()))", "expected_output": "true"},
            {"id": "t7", "input": "([{}])", "expected_output": "true"},
            {"id": "t8", "input": "([)]", "expected_output": "false"},
            {"id": "t9", "input": "()()()", "expected_output": "true"},
            {"id": "t10", "input": "(((", "expected_output": "false"}
        ]
    },
    {
        "id": "q6",
        "title": "Merge Two Sorted Arrays",
        "language": "python",
        "code": """def merge_sorted_arrays(arr1, arr2):
    result = []
    i, j = 0, 0
    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1
    result.extend(arr1[i:])
    result.extend(arr2[j:])
    return result

n1 = int(input())
arr1 = list(map(int, input().split()))
n2 = int(input())
arr2 = list(map(int, input().split()))
result = merge_sorted_arrays(arr1, arr2)
print(' '.join(map(str, result)))""",
        "test_cases": [
            {"id": "t1", "input": "3\n1 2 3\n3\n2 5 6", "expected_output": "1 2 2 3 5 6"},
            {"id": "t2", "input": "1\n1\n1\n2", "expected_output": "1 2"},
            {"id": "t3", "input": "0\n\n1\n1", "expected_output": "1"},
            {"id": "t4", "input": "2\n1 3\n2\n2 4", "expected_output": "1 2 3 4"},
            {"id": "t5", "input": "3\n1 5 9\n3\n2 6 10", "expected_output": "1 2 5 6 9 10"},
            {"id": "t6", "input": "2\n10 20\n2\n15 25", "expected_output": "10 15 20 25"},
            {"id": "t7", "input": "4\n1 2 3 4\n2\n5 6", "expected_output": "1 2 3 4 5 6"},
            {"id": "t8", "input": "2\n5 10\n3\n1 2 3", "expected_output": "1 2 3 5 10"},
            {"id": "t9", "input": "3\n1 1 1\n2\n2 2", "expected_output": "1 1 1 2 2"},
            {"id": "t10", "input": "1\n0\n1\n1", "expected_output": "0 1"}
        ]
    },
    {
        "id": "q7",
        "title": "Find Peak Element",
        "language": "python",
        "code": """def find_peak(nums):
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[mid + 1]:
            right = mid
        else:
            left = mid + 1
    return left

nums = list(map(int, input().split()))
result = find_peak(nums)
print(result)""",
        "test_cases": [
            {"id": "t1", "input": "1 2 3 1", "expected_output": "2"},
            {"id": "t2", "input": "1 2 1 3 5 6 4", "expected_output": "5"},
            {"id": "t3", "input": "1 2 3", "expected_output": "2"},
            {"id": "t4", "input": "3 2 1", "expected_output": "0"},
            {"id": "t5", "input": "1 3 2 4 1", "expected_output": "1"},
            {"id": "t6", "input": "1 2 3 4 5 1", "expected_output": "4"},
            {"id": "t7", "input": "5 4 3 2", "expected_output": "0"},
            {"id": "t8", "input": "1 5 3 2 1", "expected_output": "1"},
            {"id": "t9", "input": "10 5 1", "expected_output": "0"},
            {"id": "t10", "input": "1 2 1 0", "expected_output": "1"}
        ]
    },
    {
        "id": "q8",
        "title": "Remove Duplicates from Sorted Array",
        "language": "python",
        "code": """def remove_duplicates(nums):
    if not nums:
        return 0
    write_index = 1
    for i in range(1, len(nums)):
        if nums[i] != nums[i-1]:
            nums[write_index] = nums[i]
            write_index += 1
    return write_index

n = int(input())
nums = list(map(int, input().split()))
k = remove_duplicates(nums)
print(k)
print(' '.join(map(str, nums[:k])))""",
        "test_cases": [
            {"id": "t1", "input": "3\n1 1 2", "expected_output": "2\n1 2"},
            {"id": "t2", "input": "5\n0 0 1 1 1 2 2 3 3 4", "expected_output": "5\n0 1 2 3 4"},
            {"id": "t3", "input": "1\n1", "expected_output": "1\n1"},
            {"id": "t4", "input": "3\n1 2 3", "expected_output": "3\n1 2 3"},
            {"id": "t5", "input": "4\n1 1 1 1", "expected_output": "1\n1"},
            {"id": "t6", "input": "5\n1 2 2 3 3", "expected_output": "3\n1 2 3"},
            {"id": "t7", "input": "6\n0 0 0 1 1 1", "expected_output": "2\n0 1"},
            {"id": "t8", "input": "4\n5 5 10 10", "expected_output": "2\n5 10"},
            {"id": "t9", "input": "3\n-1 -1 0", "expected_output": "2\n-1 0"},
            {"id": "t10", "input": "5\n1 1 2 2 3", "expected_output": "3\n1 2 3"}
        ]
    },
    {
        "id": "q9",
        "title": "Rotate Array",
        "language": "python",
        "code": """def rotate_array(nums, k):
    n = len(nums)
    k = k % n
    nums[:] = nums[-k:] + nums[:-k]

n = int(input())
k = int(input())
nums = list(map(int, input().split()))
rotate_array(nums, k)
print(' '.join(map(str, nums)))""",
        "test_cases": [
            {"id": "t1", "input": "7\n3\n1 2 3 4 5 6 7", "expected_output": "5 6 7 1 2 3 4"},
            {"id": "t2", "input": "4\n2\n-1 -100 3 99", "expected_output": "3 99 -1 -100"},
            {"id": "t3", "input": "3\n1\n1 2 3", "expected_output": "3 1 2"},
            {"id": "t4", "input": "5\n2\n1 2 3 4 5", "expected_output": "4 5 1 2 3"},
            {"id": "t5", "input": "4\n4\n1 2 3 4", "expected_output": "1 2 3 4"},
            {"id": "t6", "input": "6\n3\n1 2 3 4 5 6", "expected_output": "4 5 6 1 2 3"},
            {"id": "t7", "input": "3\n0\n1 2 3", "expected_output": "1 2 3"},
            {"id": "t8", "input": "5\n1\n10 20 30 40 50", "expected_output": "50 10 20 30 40"},
            {"id": "t9", "input": "4\n2\n-1 0 1 2", "expected_output": "1 2 -1 0"},
            {"id": "t10", "input": "6\n6\n1 2 3 4 5 6", "expected_output": "1 2 3 4 5 6"}
        ]
    },
    {
        "id": "q10",
        "title": "Contains Duplicate",
        "language": "python",
        "code": """def contains_duplicate(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False

n = int(input())
nums = list(map(int, input().split()))
result = contains_duplicate(nums)
print("true" if result else "false")""",
        "test_cases": [
            {"id": "t1", "input": "4\n1 2 3 1", "expected_output": "true"},
            {"id": "t2", "input": "4\n1 2 3 4", "expected_output": "false"},
            {"id": "t3", "input": "5\n1 1 1 3 3 4 3 2 4 2", "expected_output": "true"},
            {"id": "t4", "input": "1\n1", "expected_output": "false"},
            {"id": "t5", "input": "3\n1 2 2", "expected_output": "true"},
            {"id": "t6", "input": "5\n1 2 3 4 5", "expected_output": "false"},
            {"id": "t7", "input": "4\n10 20 10 30", "expected_output": "true"},
            {"id": "t8", "input": "3\n-1 0 1", "expected_output": "false"},
            {"id": "t9", "input": "6\n1 2 3 1 4 5", "expected_output": "true"},
            {"id": "t10", "input": "2\n1 1", "expected_output": "true"}
        ]
    },
    {
        "id": "q11",
        "title": "Product of Array Except Self",
        "language": "python",
        "code": """def product_except_self(nums):
    n = len(nums)
    result = [1] * n
    left_product = 1
    for i in range(n):
        result[i] = left_product
        left_product *= nums[i]
    right_product = 1
    for i in range(n-1, -1, -1):
        result[i] *= right_product
        right_product *= nums[i]
    return result

n = int(input())
nums = list(map(int, input().split()))
result = product_except_self(nums)
print(' '.join(map(str, result)))""",
        "test_cases": [
            {"id": "t1", "input": "4\n1 2 3 4", "expected_output": "24 12 8 6"},
            {"id": "t2", "input": "4\n-1 1 0 -3 3", "expected_output": "0 0 9 0 0"},
            {"id": "t3", "input": "2\n2 3", "expected_output": "3 2"},
            {"id": "t4", "input": "3\n1 0 1", "expected_output": "0 1 0"},
            {"id": "t5", "input": "4\n2 4 6 8", "expected_output": "192 96 64 48"},
            {"id": "t6", "input": "3\n-1 -2 -3", "expected_output": "6 3 2"},
            {"id": "t7", "input": "5\n1 2 3 4 5", "expected_output": "120 60 40 30 24"},
            {"id": "t8", "input": "2\n0 5", "expected_output": "5 0"},
            {"id": "t9", "input": "4\n10 20 30 40", "expected_output": "24000 12000 8000 6000"},
            {"id": "t10", "input": "3\n1 1 1", "expected_output": "1 1 1"}
        ]
    },
    {
        "id": "q12",
        "title": "Longest Substring Without Repeating Characters",
        "language": "python",
        "code": """def length_of_longest_substring(s):
    char_map = {}
    start = 0
    max_length = 0
    for end in range(len(s)):
        if s[end] in char_map and char_map[s[end]] >= start:
            start = char_map[s[end]] + 1
        char_map[s[end]] = end
        max_length = max(max_length, end - start + 1)
    return max_length

s = input().strip()
result = length_of_longest_substring(s)
print(result)""",
        "test_cases": [
            {"id": "t1", "input": "abcabcbb", "expected_output": "3"},
            {"id": "t2", "input": "bbbbb", "expected_output": "1"},
            {"id": "t3", "input": "pwwkew", "expected_output": "3"},
            {"id": "t4", "input": "", "expected_output": "0"},
            {"id": "t5", "input": "dvdf", "expected_output": "3"},
            {"id": "t6", "input": "abc", "expected_output": "3"},
            {"id": "t7", "input": "aab", "expected_output": "2"},
            {"id": "t8", "input": "abcdef", "expected_output": "6"},
            {"id": "t9", "input": "abba", "expected_output": "2"},
            {"id": "t10", "input": "tmmzuxt", "expected_output": "5"}
        ]
    },
    {
        "id": "q13",
        "title": "Group Anagrams",
        "language": "python",
        "code": """from collections import defaultdict

def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = ''.join(sorted(s))
        groups[key].append(s)
    result = []
    for key in sorted(groups.keys()):
        result.append(sorted(groups[key]))
    return result

n = int(input())
if n == 0:
    print("")
elif n == 1:
    s = input().strip()
    print(s if s else "")
else:
    strs = input().strip().split()
    result = group_anagrams(strs)
    output_lines = []
    for group in result:
        output_lines.append(' '.join(sorted(group)))
    print('\\n'.join(output_lines))""",
        "test_cases": [
            {"id": "t1", "input": "6\neat tea tan ate nat bat", "expected_output": "bat\neat tea ate\ntan nat"},
            {"id": "t2", "input": "1\n", "expected_output": ""},
            {"id": "t3", "input": "1\na", "expected_output": "a"},
            {"id": "t4", "input": "3\nabc def ghi", "expected_output": "abc\ndef\nghi"},
            {"id": "t5", "input": "4\nlisten silent enlist inlets", "expected_output": "enlist inlets listen silent"},
            {"id": "t6", "input": "3\ncat act tac", "expected_output": "act cat tac"},
            {"id": "t7", "input": "2\nhello world", "expected_output": "hello\nworld"},
            {"id": "t8", "input": "4\nab ba cd dc", "expected_output": "ab ba\ncd dc"},
            {"id": "t9", "input": "3\n123 321 213", "expected_output": "123 213 321"},
            {"id": "t10", "input": "5\naa bb cc dd ee", "expected_output": "aa\nbb\ncc\ndd\nee"}
        ]
    },
    {
        "id": "q14",
        "title": "Top K Frequent Elements",
        "language": "python",
        "code": """from collections import Counter

def top_k_frequent(nums, k):
    counter = Counter(nums)
    return [num for num, _ in counter.most_common(k)]

n = int(input())
k = int(input())
nums = list(map(int, input().split()))
result = top_k_frequent(nums, k)
print(' '.join(map(str, result)))""",
        "test_cases": [
            {"id": "t1", "input": "6\n2\n1 1 1 2 2 3", "expected_output": "1 2"},
            {"id": "t2", "input": "1\n1\n1", "expected_output": "1"},
            {"id": "t3", "input": "5\n2\n1 2 2 3 3", "expected_output": "2 3"},
            {"id": "t4", "input": "6\n3\n1 1 2 2 3 3", "expected_output": "1 2 3"},
            {"id": "t5", "input": "7\n1\n1 1 1 1 1 1 1", "expected_output": "1"},
            {"id": "t6", "input": "5\n2\n5 5 5 10 10", "expected_output": "5 10"},
            {"id": "t7", "input": "8\n3\n1 1 2 2 3 3 4 4", "expected_output": "1 2 3"},
            {"id": "t8", "input": "4\n1\n1 2 3 4", "expected_output": "1"},
            {"id": "t9", "input": "6\n2\n10 10 20 20 30 30", "expected_output": "10 20"},
            {"id": "t10", "input": "5\n3\n1 1 1 2 2", "expected_output": "1 2"}
        ]
    },
    {
        "id": "q15",
        "title": "Climbing Stairs",
        "language": "python",
        "code": """def climb_stairs(n):
    if n <= 2:
        return n
    first, second = 1, 2
    for i in range(3, n + 1):
        third = first + second
        first, second = second, third
    return second

n = int(input())
result = climb_stairs(n)
print(result)""",
        "test_cases": [
            {"id": "t1", "input": "2", "expected_output": "2"},
            {"id": "t2", "input": "3", "expected_output": "3"},
            {"id": "t3", "input": "4", "expected_output": "5"},
            {"id": "t4", "input": "5", "expected_output": "8"},
            {"id": "t5", "input": "6", "expected_output": "13"},
            {"id": "t6", "input": "7", "expected_output": "21"},
            {"id": "t7", "input": "8", "expected_output": "34"},
            {"id": "t8", "input": "9", "expected_output": "55"},
            {"id": "t9", "input": "10", "expected_output": "89"},
            {"id": "t10", "input": "1", "expected_output": "1"}
        ]
    },
    {
        "id": "q16",
        "title": "Coin Change",
        "language": "python",
        "code": """def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1

n = int(input())
amount = int(input())
coins = list(map(int, input().split()))
result = coin_change(coins, amount)
print(result)""",
        "test_cases": [
            {"id": "t1", "input": "3\n11\n1 2 5", "expected_output": "3"},
            {"id": "t2", "input": "1\n3\n2", "expected_output": "-1"},
            {"id": "t3", "input": "1\n0\n1", "expected_output": "0"},
            {"id": "t4", "input": "2\n3\n1 2", "expected_output": "2"},
            {"id": "t5", "input": "4\n10\n1 3 4 5", "expected_output": "2"},
            {"id": "t6", "input": "3\n6\n1 2 5", "expected_output": "2"},
            {"id": "t7", "input": "2\n5\n1 5", "expected_output": "1"},
            {"id": "t8", "input": "3\n7\n2 3 5", "expected_output": "2"},
            {"id": "t9", "input": "4\n15\n1 5 10 25", "expected_output": "2"},
            {"id": "t10", "input": "2\n4\n1 3", "expected_output": "2"}
        ]
    },
    {
        "id": "q17",
        "title": "House Robber",
        "language": "python",
        "code": """def rob(nums):
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    dp = [0] * len(nums)
    dp[0] = nums[0]
    dp[1] = max(nums[0], nums[1])
    for i in range(2, len(nums)):
        dp[i] = max(dp[i-1], dp[i-2] + nums[i])
    return dp[-1]

n = int(input())
nums = list(map(int, input().split()))
result = rob(nums)
print(result)""",
        "test_cases": [
            {"id": "t1", "input": "4\n1 2 3 1", "expected_output": "4"},
            {"id": "t2", "input": "5\n2 7 9 3 1", "expected_output": "12"},
            {"id": "t3", "input": "2\n2 1", "expected_output": "2"},
            {"id": "t4", "input": "1\n1", "expected_output": "1"},
            {"id": "t5", "input": "5\n5 1 1 5 1", "expected_output": "10"},
            {"id": "t6", "input": "4\n10 1 1 10", "expected_output": "20"},
            {"id": "t7", "input": "3\n1 2 3", "expected_output": "4"},
            {"id": "t8", "input": "6\n1 2 3 4 5 6", "expected_output": "12"},
            {"id": "t9", "input": "4\n100 1 1 100", "expected_output": "200"},
            {"id": "t10", "input": "3\n5 10 5", "expected_output": "10"}
        ]
    },
    {
        "id": "q18",
        "title": "Word Break",
        "language": "python",
        "code": """def word_break(s, word_dict):
    word_set = set(word_dict)
    dp = [False] * (len(s) + 1)
    dp[0] = True
    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    return dp[len(s)]

s = input().strip()
n = int(input())
word_dict = [input().strip() for _ in range(n)]
result = word_break(s, word_dict)
print("true" if result else "false")""",
        "test_cases": [
            {"id": "t1", "input": "leetcode\n2\nleet code", "expected_output": "true"},
            {"id": "t2", "input": "applepenapple\n2\napple pen", "expected_output": "true"},
            {"id": "t3", "input": "catsandog\n4\ncats dog sand and cat", "expected_output": "false"},
            {"id": "t4", "input": "a\n1\na", "expected_output": "true"},
            {"id": "t5", "input": "ab\n2\na b", "expected_output": "true"},
            {"id": "t6", "input": "abc\n3\na b c", "expected_output": "true"},
            {"id": "t7", "input": "abcd\n2\nab cd", "expected_output": "true"},
            {"id": "t8", "input": "abcde\n3\nab cd e", "expected_output": "true"},
            {"id": "t9", "input": "aaaa\n2\na aa", "expected_output": "true"},
            {"id": "t10", "input": "xyz\n1\nabc", "expected_output": "false"}
        ]
    },
    {
        "id": "q19",
        "title": "Longest Increasing Subsequence",
        "language": "python",
        "code": """def length_of_lis(nums):
    if not nums:
        return 0
    dp = [1] * len(nums)
    for i in range(1, len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)

n = int(input())
nums = list(map(int, input().split()))
result = length_of_lis(nums)
print(result)""",
        "test_cases": [
            {"id": "t1", "input": "8\n10 9 2 5 3 7 101 18", "expected_output": "4"},
            {"id": "t2", "input": "6\n0 1 0 3 2 3", "expected_output": "4"},
            {"id": "t3", "input": "4\n7 7 7 7", "expected_output": "1"},
            {"id": "t4", "input": "5\n1 2 3 4 5", "expected_output": "5"},
            {"id": "t5", "input": "5\n5 4 3 2 1", "expected_output": "1"},
            {"id": "t6", "input": "6\n1 3 2 4 5 6", "expected_output": "5"},
            {"id": "t7", "input": "7\n10 20 10 30 20 50 40", "expected_output": "4"},
            {"id": "t8", "input": "4\n1 5 2 6", "expected_output": "3"},
            {"id": "t9", "input": "5\n2 1 3 4 5", "expected_output": "4"},
            {"id": "t10", "input": "3\n1 2 3", "expected_output": "3"}
        ]
    },
    {
        "id": "q20",
        "title": "Partition Equal Subset Sum",
        "language": "python",
        "code": """def can_partition(nums):
    total = sum(nums)
    if total % 2 != 0:
        return False
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for num in nums:
        for j in range(target, num - 1, -1):
            dp[j] = dp[j] or dp[j - num]
    return dp[target]

n = int(input())
nums = list(map(int, input().split()))
result = can_partition(nums)
print("true" if result else "false")""",
        "test_cases": [
            {"id": "t1", "input": "4\n1 5 11 5", "expected_output": "true"},
            {"id": "t2", "input": "3\n1 2 3 5", "expected_output": "false"},
            {"id": "t3", "input": "2\n1 1", "expected_output": "true"},
            {"id": "t4", "input": "3\n1 2 3", "expected_output": "true"},
            {"id": "t5", "input": "4\n1 2 3 4", "expected_output": "true"},
            {"id": "t6", "input": "3\n1 3 5", "expected_output": "false"},
            {"id": "t7", "input": "4\n2 2 2 2", "expected_output": "true"},
            {"id": "t8", "input": "5\n1 1 1 1 2", "expected_output": "true"},
            {"id": "t9", "input": "3\n10 20 30", "expected_output": "true"},
            {"id": "t10", "input": "4\n1 1 1 1", "expected_output": "true"}
        ]
    }
]

def submit_question(question):
    """Submit a question to the API"""
    start_time = time.time()
    try:
        data = json.dumps({
            "language": question["language"],
            "code": question["code"],
            "test_cases": question["test_cases"],
            "user_id": f"user_{question['id']}",
            "question_id": question["id"]
        }).encode('utf-8')
        
        req = urllib.request.Request(
            f"{API_URL}/runall",
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=300) as response:
            result = json.loads(response.read().decode('utf-8'))
            end_time = time.time()
            duration = end_time - start_time
            
            return {
                "question_id": question["id"],
                "title": question["title"],
                "status": "success",
                "duration": round(duration, 2),
                "total_tests": result["summary"]["total_tests"],
                "passed": result["summary"]["passed"],
                "failed": result["summary"]["failed"],
                "all_passed": result["summary"]["all_passed"],
                "execution_time_ms": result["metadata"]["execution_time_ms"],
                "replica": result["metadata"].get("replica", "unknown")
            }
    except urllib.error.HTTPError as e:
        end_time = time.time()
        duration = end_time - start_time
        error_body = e.read().decode('utf-8')[:100] if e.fp else str(e)
        return {
            "question_id": question["id"],
            "title": question["title"],
            "status": "error",
            "duration": round(duration, 2),
            "error": f"HTTP {e.code}: {error_body}"
        }
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        return {
            "question_id": question["id"],
            "title": question["title"],
            "status": "exception",
            "duration": round(duration, 2),
            "error": str(e)
        }

def main():
    print("=" * 80)
    print("🚀 Testing 20 DSA Questions in Parallel (10 test cases each)")
    print("=" * 80)
    print(f"API URL: {API_URL}")
    print(f"Total Questions: {len(DSA_QUESTIONS)}")
    print(f"Total Test Cases: {len(DSA_QUESTIONS) * 10}")
    print(f"Replicas: 1 (ready state)")
    print("=" * 80)
    print()
    
    # Test health first
    try:
        req = urllib.request.Request(f"{API_URL}/health", method='GET')
        with urllib.request.urlopen(req, timeout=30) as response:
            health = json.loads(response.read().decode('utf-8'))
            print(f"✅ Health Check: {health}")
    except Exception as e:
        print(f"⚠️  Health Check Failed: {e}")
        print("Continuing with test anyway...\n")
    
    print("\n📤 Sending 20 requests in parallel...\n")
    
    start_time = time.time()
    results = []
    
    # Submit all questions in parallel
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(submit_question, q): q for q in DSA_QUESTIONS}
        
        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()
            results.append(result)
            status_icon = "✅" if result["status"] == "success" else "❌"
            print(f"{status_icon} [{i}/20] {result['question_id']}: {result['title']} - "
                  f"{result['status']} ({result['duration']}s)")
    
    end_time = time.time()
    total_duration = end_time - start_time
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    
    successful = [r for r in results if r["status"] == "success"]
    failed = [r for r in results if r["status"] != "success"]
    
    print(f"Total Questions: {len(results)}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")
    print(f"Total Duration: {round(total_duration, 2)}s")
    print(f"Average per Question: {round(total_duration / len(results), 2)}s")
    
    if successful:
        total_tests = sum(r["total_tests"] for r in successful)
        total_passed = sum(r["passed"] for r in successful)
        avg_execution = sum(r["execution_time_ms"] for r in successful) / len(successful)
        
        print(f"\nTest Cases:")
        print(f"  Total: {total_tests}")
        print(f"  Passed: {total_passed}")
        print(f"  Failed: {total_tests - total_passed}")
        print(f"  Pass Rate: {round(total_passed / total_tests * 100, 1)}%")
        print(f"\nAverage Execution Time: {round(avg_execution, 0)}ms")
        
        # Replica distribution
        replicas = {}
        for r in successful:
            replica = r.get("replica", "unknown")
            replicas[replica] = replicas.get(replica, 0) + 1
        print(f"\nReplica Distribution:")
        for replica, count in replicas.items():
            print(f"  {replica}: {count} questions")
    
    if failed:
        print(f"\n❌ Failed Questions:")
        for r in failed:
            print(f"  {r['question_id']}: {r.get('error', 'Unknown error')}")
    
    # Save results to CSV
    import csv
    with open('test-20-questions-results.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['question_id', 'title', 'status', 'duration', 
                                               'total_tests', 'passed', 'failed', 'all_passed', 
                                               'execution_time_ms', 'replica', 'error'])
        writer.writeheader()
        for r in results:
            writer.writerow(r)
    
    print(f"\n💾 Results saved to: test-20-questions-results.csv")
    print("=" * 80)

if __name__ == "__main__":
    main()

