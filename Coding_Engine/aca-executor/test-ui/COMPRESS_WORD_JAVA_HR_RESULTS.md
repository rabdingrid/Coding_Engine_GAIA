# Compress Word Problem - Java HackerRank Style Test Results (Question ID: 622797)

## ✅ **ALL 15 TEST CASES PASSED!**

### Test Summary
- **Status**: ✅ All Passed!
- **Pass Rate**: 100% (15/15)
- **Total Execution Time**: 11,497ms (~767ms per test, includes compilation)
- **Container ID**: ai-ta-ra-code-executor2--0000025-5b685f898d-9pbc5
- **CPU Usage**: 160.1%
- **Memory Usage**: 40.0 MB

---

## Java HackerRank-Style Implementation

### Code Structure
```java
import java.io.*;
import java.math.*;
import java.security.*;
import java.text.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.function.*;
import java.util.regex.*;
import java.util.stream.*;
import static java.util.stream.Collectors.joining;
import static java.util.stream.Collectors.toList;

class Result {
    public static String compressWord(String word, int k) {
        // Stack-based approach: track [char, count] pairs
        List<int[]> stack = new ArrayList<>();  // [char, count]
        
        for (char c : word.toCharArray()) {
            if (!stack.isEmpty() && stack.get(stack.size() - 1)[0] == c) {
                stack.get(stack.size() - 1)[1]++;
                if (stack.get(stack.size() - 1)[1] == k) {
                    stack.remove(stack.size() - 1);
                }
            } else {
                stack.add(new int[]{c, 1});
            }
        }
        
        StringBuilder result = new StringBuilder();
        for (int[] pair : stack) {
            char ch = (char) pair[0];
            int count = pair[1];
            for (int i = 0; i < count; i++) {
                result.append(ch);
            }
        }
        return result.toString();
    }
}

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(System.in));
        String word = bufferedReader.readLine();
        int k = Integer.parseInt(bufferedReader.readLine().trim());
        String result = Result.compressWord(word, k);
        System.out.println(result);
        bufferedReader.close();
    }
}
```

### Key Adaptations from HackerRank Boilerplate:
1. ✅ **Changed class name**: `Solution` → `Main` (to match filename `Main.java`)
2. ✅ **Removed `System.getenv("OUTPUT_PATH")`**: Uses `System.out.println()` instead
3. ✅ **Removed `BufferedWriter`**: Not needed for standard output
4. ✅ **Kept all imports**: HackerRank-style imports preserved
5. ✅ **Implemented `compressWord`**: Stack-based algorithm using `List<int[]>`

---

## Test Cases

### Basic Test Cases (1-3)
1. ✅ **word="aba" k=2** → "aba"
2. ✅ **word="baac" k=2** → "bc"
3. ✅ **word="abbcccb" k=3** → "a"

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

## Performance Comparison

| Metric | Python | C++ | Java (HR Style) |
|--------|--------|-----|-----------------|
| **Total Time** | 298ms | 17,507ms | 11,497ms |
| **Avg per Test** | ~20ms | ~1,167ms | ~767ms |
| **Memory** | 10.6 MB | 2.1 MB | 40.0 MB |
| **CPU Usage** | 32.5% | 0.0% | 160.1% |

**Note**: Java execution time includes compilation. Java is faster than C++ but slower than Python for this use case.

---

## Important Fix Applied

### **Issue**: 
```
error: class Solution is public, should be declared in a file named Solution.java
```

### **Solution**:
Changed `public class Solution` to `public class Main` to match the filename that the executor service uses (`Main.java`).

**Rule**: In Java, if a class is declared as `public`, it must be in a file with the same name.

---

## Algorithm

**Stack-based approach:**
- Use `List<int[]>` to track consecutive characters `[char, count]`
- When a character matches the top of stack, increment count
- When count reaches `k`, remove from stack
- Build result string from remaining stack elements

**Time Complexity**: O(n) where n is the length of the word
**Space Complexity**: O(n) in worst case

---

## System Validation

✅ **Code execution**: WORKING
✅ **Java compilation**: WORKING
✅ **HackerRank-style imports**: WORKING
✅ **Multi-test case handling**: WORKING (15 test cases)
✅ **Large input handling**: WORKING (up to ~100KB strings)
✅ **Edge case handling**: WORKING
✅ **Memory efficiency**: GOOD (40.0 MB)
✅ **Boilerplate compatibility**: WORKING (adapted for standard I/O)

---

## Files

1. **test-compress-word-java-hackerrank.sh** - Automated test script for Java HackerRank style
2. **COMPRESS_WORD_JAVA_HR_RESULTS.md** - This documentation
3. **Test cases**: `/Users/rabdin/Documents/AGCodingEngine/Coding_Engine/aca-executor/622797/`

---

## Conclusion

**🎯 System Status: PRODUCTION READY!**

The Azure Container App executor successfully handled all 15 test cases with the Java HackerRank-style boilerplate code, including:
- ✅ Basic edge cases
- ✅ Medium-sized strings
- ✅ Large strings (~8KB)
- ✅ Very large strings (~100KB)
- ✅ Various k values (from 2 to 8179)

The Java HackerRank-style implementation works correctly with the provided boilerplate structure, demonstrating that the system supports HackerRank-style Java code execution for coding contests.

**Key Takeaway**: When using HackerRank-style Java boilerplate, remember to change `public class Solution` to `public class Main` to match the executor's file naming convention.


