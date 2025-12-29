# How to Add a Question

## ✅ Method 1: Using the UI (Recommended)

1. **Click "+ New" button** in the left sidebar
2. **Fill in the form**:
   - **Title**: e.g., "Two Sum"
   - **Description**: Problem description
   - **Difficulty**: Easy, Medium, or Hard
3. **Add Test Cases**:
   - Click "+ Add Test Case" button
   - Enter **Input**: e.g., `5\n10`
   - Enter **Expected Output**: e.g., `15`
   - Add more test cases as needed
4. **Click "Save Question"**
5. **Refresh the page** - your question will appear in the sidebar!

---

## ✅ Method 2: Using the Script (Quick Test)

I've added a sample question for you! Run:

```bash
cd aca-executor/test-ui
node add-sample-question.js
```

This will add a sample "Two Sum" question with 3 test cases.

Then refresh your browser to see it!

---

## 📝 Example Question

**Title**: Two Sum  
**Description**: Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.  
**Difficulty**: Easy

**Test Cases**:
1. Input: `5\n10`, Expected Output: `15`
2. Input: `100\n200`, Expected Output: `300`
3. Input: `-5\n5`, Expected Output: `0`

---

## 🎯 After Adding a Question

1. **Click the question** in the left sidebar
2. **Question details** will load in the middle panel
3. **Test cases** will be displayed
4. **Write your code** in the editor
5. **Click "▶ Run Code"** to test

---

## 💡 Tips

- You can add multiple test cases per question
- Test cases are stored in the database
- Questions persist across browser refreshes
- You can delete questions by clicking on them and using the delete option (if added)

---

**Quick Add**: Run `node add-sample-question.js` to add a test question!


