# Code Executor Test UI - Database Integrated

A full-featured test UI for the code executor with PostgreSQL database integration.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd test-ui
npm install
```

### 2. Start the Server

```bash
npm start
```

The server will start on `http://localhost:3000`

### 3. Open in Browser

Open `http://localhost:3000` in your browser.

---

## 📋 Features

### ✅ Database Integration
- **PostgreSQL Database**: Connected to Railway PostgreSQL
- **Questions Management**: Create, read, update, delete questions
- **Test Cases**: Add test cases to questions
- **Auto-initialization**: Tables are created automatically

### ✅ Question Management
- **Question List**: Left sidebar shows all questions
- **Question Details**: Click a question to view details and test cases
- **Add Question**: Create new questions with test cases
- **Test Cases**: Add multiple test cases per question

### ✅ Code Execution
- **Code Editor**: Syntax-highlighted editor (Python, JavaScript, Java, C++)
- **Run Code**: Execute code against test cases from database
- **Results Display**: View detailed test results with pass/fail status

---

## 🗄️ Database Schema

### Questions Table
```sql
CREATE TABLE questions (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  difficulty VARCHAR(20),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Test Cases Table
```sql
CREATE TABLE test_cases (
  id SERIAL PRIMARY KEY,
  question_id INTEGER REFERENCES questions(id) ON DELETE CASCADE,
  input TEXT,
  expected_output TEXT,
  input_file VARCHAR(255),
  output_file VARCHAR(255),
  test_order INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 📡 API Endpoints

### Questions
- `GET /api/questions` - Get all questions
- `GET /api/questions/:id` - Get question with test cases
- `POST /api/questions` - Create new question
- `PUT /api/questions/:id` - Update question
- `DELETE /api/questions/:id` - Delete question

### Test Cases
- `POST /api/questions/:id/testcases` - Add test case to question
- `PUT /api/testcases/:id` - Update test case
- `DELETE /api/testcases/:id` - Delete test case

---

## 🎯 Usage

### 1. Add a Question
1. Click "+ New" button in the left sidebar
2. Fill in title, description, difficulty
3. Add test cases (input and expected output)
4. Click "Save Question"

### 2. Select a Question
1. Click on any question in the left sidebar
2. Question details and test cases will load automatically
3. Test cases are displayed in the middle panel

### 3. Write and Test Code
1. Select a question
2. Write your code in the editor
3. Select language (Python, JavaScript, Java, C++)
4. Click "▶ Run Code"
5. View results in the results panel

---

## 🔧 Configuration

### Database Connection
The database connection string is in `server.js`:
```javascript
const pool = new Pool({
  connectionString: 'postgresql://postgres:LpGWrOQpFdgLxybzTYWdGiAuJbitpizZ@yamanote.proxy.rlwy.net:55115/railway',
  ssl: { rejectUnauthorized: false }
});
```

### Executor URL
The executor URL is in `index.html`:
```javascript
const EXECUTOR_URL = 'https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io';
```

---

## 📊 Example Workflow

1. **Add Question**: "Two Sum"
   - Description: "Given an array of integers..."
   - Difficulty: Medium
   - Test Case 1: Input: `5\n10`, Output: `15`
   - Test Case 2: Input: `100\n200`, Output: `300`

2. **Select Question**: Click "Two Sum" in sidebar

3. **Write Code**:
   ```python
   a = int(input())
   b = int(input())
   print(a + b)
   ```

4. **Run Code**: Click "▶ Run Code"

5. **View Results**: See pass/fail for each test case

---

## 🐛 Troubleshooting

### Database Connection Failed
- Check if database URL is correct
- Verify database is accessible
- Check server logs for errors

### Questions Not Loading
- Check browser console for errors
- Verify API server is running
- Check database connection

### Code Execution Failed
- Verify executor URL is correct
- Check executor is accessible
- Test executor connection button

---

## 📄 Files

- `server.js` - Express server with PostgreSQL integration
- `index.html` - Frontend UI
- `package.json` - Dependencies
- `README.md` - This file

---

## 🎉 Ready to Use!

1. Start server: `npm start`
2. Open browser: `http://localhost:3000`
3. Add questions and test code!

---

**Database**: PostgreSQL (Railway)  
**Executor**: Azure Container Apps  
**Status**: ✅ Ready for testing
