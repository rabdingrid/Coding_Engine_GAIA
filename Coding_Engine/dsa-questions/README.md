# DSA Questions Repository

## 📁 File System Structure

```
dsa-questions/
├── README.md                    # This file
├── questions.json               # Master index of all questions
├── import-to-db.js             # Script to import questions to database
├── Q001/                        # Question 1
│   ├── metadata.json           # Question metadata (ID, title, difficulty, tags)
│   ├── problem.md              # Problem description
│   ├── test_cases/             # Test cases directory
│   │   ├── 01.in               # Test case 1 input
│   │   ├── 01.out              # Test case 1 expected output
│   │   ├── 02.in
│   │   ├── 02.out
│   │   └── ... (20+ test cases)
│   └── boilerplates/           # Language-specific boilerplates
│       ├── python.py
│       ├── java.java
│       ├── cpp.cpp
│       ├── javascript.js
│       └── csharp.cs
├── Q002/
│   └── ...
└── Q050/
    └── ...
```

## 📋 Question ID Format

- **Format**: `Q001`, `Q002`, ..., `Q050`
- **Database UUID**: Generated from question ID (consistent)
- **Easy Fetching**: Questions can be fetched by ID or UUID

## 🎯 Question Categories

1. **Arrays & Strings** (10 questions)
2. **Linked Lists** (5 questions)
3. **Trees & Binary Trees** (8 questions)
4. **Graphs** (7 questions)
5. **Dynamic Programming** (8 questions)
6. **Recursion & Backtracking** (5 questions)
7. **Sorting & Searching** (4 questions)
8. **Stack & Queue** (3 questions)

## 📊 Test Cases Structure

Each question has **at least 20 test cases**:
- **5-8 basic test cases** (simple inputs)
- **5-8 edge cases** (empty, single element, max values, etc.)
- **5-8 long test cases** (large inputs for performance testing)
- **2-4 corner cases** (boundary conditions)

## 🔧 Usage

### Import to Database:
```bash
cd dsa-questions
node import-to-db.js
```

### Fetch Question:
```javascript
// By ID
GET /api/questions/Q001

// By UUID (from database)
GET /api/questions/{uuid}
```

## ✅ Features

- ✅ Proper file system organization
- ✅ Easy to add new questions
- ✅ Version control friendly
- ✅ Language-specific boilerplates
- ✅ Comprehensive test cases
- ✅ TLE/MLE detection ready

