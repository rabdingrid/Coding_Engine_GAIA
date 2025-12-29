# 🚀 Enhanced Coding Engine UI

A modern, enhanced frontend for the FastAPI-based coding execution engine with database integration.

## ✨ Features

- ✅ **Load Questions from Database**: Automatically loads all questions from `coding_question_bank` table
- ✅ **FastAPI Integration**: Uses `/run`, `/runall`, and `/submit` endpoints
- ✅ **Multi-Language Support**: Python, Java, C++, JavaScript, C#
- ✅ **Separate Result Tabs**: View outputs from Run, Run All, and Submit separately
- ✅ **Real-time Execution**: See test results as they execute
- ✅ **Detailed Metrics**: CPU usage, memory usage, execution time

## 🚀 Quick Start

### Option 1: Using the Startup Script (Recommended)

```bash
cd Coding_Engine/frontend
chmod +x start-ui.sh
./start-ui.sh
```

This will start both the Questions API server (port 3002) and the Frontend server (port 3001).

### Option 2: Manual Start

#### Step 1: Install Dependencies

```bash
# Install asyncpg for database connectivity
python3 -m pip install --user asyncpg

# Or use a virtual environment
python3 -m venv venv
source venv/bin/activate
pip install asyncpg
```

#### Step 2: Start Questions API Server

```bash
cd Coding_Engine/frontend
python3 questions-api.py
```

This starts the Questions API on port 3002.

#### Step 3: Start Frontend Server

In a new terminal:

```bash
cd Coding_Engine/frontend
python3 server.py
```

This starts the frontend on port 3001.

#### Step 4: Open in Browser

Navigate to: **http://localhost:3001**

## 📋 Configuration

### Database Connection

The Questions API connects to Azure PostgreSQL. Update the connection string in `questions-api.py`:

```python
DB_URL = os.getenv('DATABASE_URL', 'postgresql://postgresadmin:5oXcNX59QmEl7zmV3DbjemkiJ@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require')
```

Or set the `DATABASE_URL` environment variable:

```bash
export DATABASE_URL="postgresql://user:password@host:port/database?sslmode=require"
```

### API Endpoints

The frontend connects to the FastAPI executor. Update the API URL in the UI dropdown or in `app.js`:

```javascript
let apiUrl = 'https://ai-ta-ra-code-executor2--0000028.happypond-428960e8.eastus2.azurecontainerapps.io';
```

## 🎯 Usage

1. **Select a Problem**: Click on a problem from the sidebar (loaded from database)
2. **Choose Language**: Select Python, Java, C++, JavaScript, or C#
3. **Write Code**: Use the boilerplate code or write your own solution
4. **Run**: Click "Run" to test with sample test cases (uses `/run` endpoint)
5. **Run All**: Click "Run All" to test with all test cases (uses `/runall` endpoint)
6. **Submit**: Click "Submit" to submit your solution and save to database (uses `/submit` endpoint)

## 📊 Result Tabs

The UI has three separate tabs for results:

- **Run Tab**: Shows results from the `/run` endpoint (sample test cases)
- **Run All Tab**: Shows results from the `/runall` endpoint (all test cases)
- **Submit Tab**: Shows results from the `/submit` endpoint (saved to database)

## 🔧 API Endpoints

### Questions API (Port 3002)

- `GET /api/questions` - Get all questions from database
- `GET /api/questions/<id>` - Get specific question by ID

### FastAPI Executor

- `POST /run` - Execute code with sample test cases
- `POST /runall` - Execute code with all test cases
- `POST /submit` - Submit code and save results to database

## 🐛 Troubleshooting

### Questions not loading?

1. Make sure `questions-api.py` is running on port 3002
2. Check database connection string in `questions-api.py`
3. Verify database is accessible and `coding_question_bank` table exists
4. Check browser console for errors

### API errors?

1. Verify the FastAPI executor URL is correct
2. Check if the executor is running and accessible
3. Check browser console for CORS or network errors
4. Try the production URL: `https://ai-ta-ra-code-executor2--0000028.happypond-428960e8.eastus2.azurecontainerapps.io`

### Port conflicts?

- Questions API uses port 3002 (change `QUESTIONS_API_PORT` env var)
- Frontend uses port 3001 (change `PORT` in `server.py`)

## 📁 File Structure

```
frontend/
├── index.html          # Main HTML file
├── app.js              # Application logic (FastAPI integration)
├── styles.css          # Styling
├── server.py           # Frontend HTTP server
├── questions-api.py    # Backend API to fetch questions from database
├── start-ui.sh         # Startup script
└── README-ENHANCED.md  # This file
```

## 🎨 Features in Detail

### Database Integration

- Automatically fetches all questions from `coding_question_bank` table
- Displays question title, description, difficulty, tags
- Shows sample test cases and all test cases
- Loads boilerplate code for each language

### FastAPI Endpoint Integration

- **`/run`**: Executes code with sample test cases only
- **`/runall`**: Executes code with all test cases (excluding samples)
- **`/submit`**: Executes code with all test cases and saves results to database

### Result Display

- Separate tabs for each endpoint's results
- Detailed test case results with input/output comparison
- Execution metrics (time, CPU, memory)
- Color-coded pass/fail indicators
- Error messages for failed test cases

## 🔐 Security Notes

- The Questions API uses read-only database queries
- The FastAPI executor handles code execution security
- CORS is enabled for local development
- Production deployment should restrict CORS appropriately

## 📝 Notes

- The UI automatically loads questions on startup
- Questions are sorted by creation date (newest first)
- Test cases are displayed in preview (first 3 for all test cases)
- Boilerplate code is loaded based on selected language
- Results are preserved when switching between tabs




