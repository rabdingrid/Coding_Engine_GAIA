# Compress Word Problem - Test Results (Question ID: 622797)

## ✅ **ALL 15 TEST CASES PASSED!**

### Test Summary
- **Status**: ✅ All Passed!
- **Pass Rate**: 100% (15/15)
- **Total Execution Time**: 298ms
- **Container ID**: ai-ta-ra-code-executor2--0000025-5b685f898d-9pbc5
- **CPU Usage**: 32.5%
- **Memory Usage**: 10.6 MB

---

## Problem Description

A student compresses big words by removing groups of consecutive equal characters. An operation consists of choosing a group of k consecutive equal characters and removing them. The student performs this operation as long as possible.

**Example:**
- word = "abbcccb", k = 3
- Remove three consecutive 'c' characters: "abbcccb" → "abbb"
- Remove three consecutive 'b' characters: "abbb" → "a"
- Final word: "a"

---

## Test Cases

### Basic Test Cases (1-3)
1. ✅ **word="aba" k=2** → "aba" (no consecutive equal chars to remove)
2. ✅ **word="baac" k=2** → "bc" (remove "aa")
3. ✅ **word="abbcccb" k=3** → "a" (remove "ccc", then "bbb")

### Medium Test Cases (4-9)
4. ✅ **word="ptmxpmonvnytatktgvibctrhfcc..." k=10** → Compressed
5. ✅ **word="bababbabbabbabaabbbbbaabbab..." k=10** → Compressed
6. ✅ **word="fffffffffffffffffffffffffff..." k=17** → Compressed
7. ✅ **word="zzzzzzzzzzzyyyyyyyyyyyyzzzz..." k=12** → Compressed
8. ✅ **word="wwwwwwwwwwwwwwwwwwwwwwwwwww..." k=16** → Compressed
9. ✅ **word="abbaaabbbabbbaaaaababbababb..." k=3** → Compressed

### Large Test Cases (10-12)
10. ✅ **word="hhhhhhhhhhhhhhhhhhhhhhhhhhh..." k=139** → Compressed
11. ✅ **word="jjjjjjjjjjjjjjjjjjjjjjjjjjj..." k=105** → Compressed
12. ✅ **word="rrrrrrrrrrrrrrrrrrrrrrrrrrr..." k=125** → Compressed

### Very Large Test Cases (13-15)
13. ✅ **word="baabbbaabaabbbbabaababbbbab..." k=3** → Compressed (large string)
14. ✅ **word="wxixgbftjdyeevnnhzzxfieysgg..." k=8179** → Compressed (very large string, ~100KB)
15. ✅ **word="iswowtyslmxnlgprahhwuclnuky..." k=23** → Compressed (very large string, ~8KB)

---

## Algorithm

**Stack-based approach:**
```python
def compressWord(word, k):
    stack = []  # Stack of [char, count]
    
    for char in word:
        if stack and stack[-1][0] == char:
            stack[-1][1] += 1
            if stack[-1][1] == k:
                stack.pop()  # Remove when count reaches k
        else:
            stack.append([char, 1])
    
    result = "".join(char * count for char, count in stack)
    return result
```

**Time Complexity**: O(n) where n is the length of the word
**Space Complexity**: O(n) in worst case (when no removals occur)

---

## Performance Metrics

- **Average execution time per test**: ~20ms
- **Total execution time**: 298ms (for 15 test cases)
- **Memory efficiency**: 10.6 MB (handles large inputs efficiently)
- **CPU usage**: 32.5% (efficient processing)

---

## System Validation

✅ **Code execution**: WORKING
✅ **Multi-test case handling**: WORKING (15 test cases)
✅ **Large input handling**: WORKING (up to ~100KB strings)
✅ **Edge case handling**: WORKING
✅ **Performance**: EXCELLENT (~20ms per test)
✅ **Memory efficiency**: EXCELLENT (10.6 MB)

---

## Files

1. **test-compress-word.sh** - Automated test script
2. **COMPRESS_WORD_TEST_RESULTS.md** - This documentation
3. **Test cases**: `/Users/rabdin/Documents/AGCodingEngine/Coding_Engine/aca-executor/622797/`
   - `input000.txt` to `input014.txt` (15 input files)
   - `output000.txt` to `output014.txt` (15 expected output files)

---

## Conclusion

**🎯 System Status: PRODUCTION READY!**

The Azure Container App executor successfully handled all 15 test cases, including:
- Basic edge cases
- Medium-sized strings
- Large strings (~8KB)
- Very large strings (~100KB)
- Various k values (from 2 to 8179)

The system demonstrates excellent performance and reliability for production use in coding contests.


