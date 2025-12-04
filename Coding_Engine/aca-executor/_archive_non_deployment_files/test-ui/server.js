const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');
const path = require('path');
const fetch = require('node-fetch');

const app = express();
const PORT = process.env.PORT || 3001; // Use 3001 to avoid conflict with Vite

// PostgreSQL connection
const pool = new Pool({
  connectionString: process.env.DATABASE_URL || 'postgresql://postgresadmin:5oXcNX59QmEl7zmV3DbjemkiJ@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require',
  ssl: {
    rejectUnauthorized: false  // Azure PostgreSQL requires SSL
  }
});

// Middleware
app.use(cors({
  origin: '*',
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
app.use(express.json());
app.use(express.static(__dirname));

// Log all requests
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
  next();
});

// Test database connection
pool.query('SELECT NOW()', (err, res) => {
  if (err) {
    console.error('Database connection error:', err);
  } else {
    console.log('✅ Database connected successfully');
  }
});

// Initialize database tables if they don't exist
async function initDatabase() {
  try {
    // Create questions table
    await pool.query(`
      CREATE TABLE IF NOT EXISTS questions (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        difficulty VARCHAR(20),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);

    // Create test_cases table
    await pool.query(`
      CREATE TABLE IF NOT EXISTS test_cases (
        id SERIAL PRIMARY KEY,
        question_id INTEGER REFERENCES questions(id) ON DELETE CASCADE,
        input TEXT,
        expected_output TEXT,
        input_file VARCHAR(255),
        output_file VARCHAR(255),
        test_order INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);

    console.log('✅ Database tables initialized');
  } catch (error) {
    console.error('Error initializing database:', error);
  }
}

initDatabase();

// API Routes

// Get all questions (from both tables)
app.get('/api/questions', async (req, res) => {
  try {
    // Fetch from coding_question_bank (main table)
    const codingQuestions = await pool.query(
      `SELECT 
        uuid as id,
        question as title,
        question as description,
        difficulty,
        tags,
        sample_test_cases,
        test_cases
      FROM coding_question_bank 
      ORDER BY uuid`
    );
    
    // Also fetch from questions table (if exists)
    let simpleQuestions = [];
    try {
      const simpleResult = await pool.query(
        'SELECT id, title, description, difficulty, created_at FROM questions ORDER BY id DESC'
      );
      simpleQuestions = simpleResult.rows;
    } catch (err) {
      // questions table might not exist, ignore
    }
    
    // Combine both (format coding_question_bank to match expected format)
    const formattedCoding = codingQuestions.rows.map(q => ({
      id: q.id,
      title: q.title || 'Untitled Question',
      description: q.description || '',
      difficulty: q.difficulty || 'Medium',
      tags: q.tags,
      test_cases: q.test_cases || q.sample_test_cases || []
    }));
    
    res.json({ 
      success: true, 
      questions: [...formattedCoding, ...simpleQuestions] 
    });
  } catch (error) {
    console.error('Error fetching questions:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Get question by ID with test cases
app.get('/api/questions/:id', async (req, res) => {
  try {
    const questionId = req.params.id; // Can be UUID or integer
    
    // Try coding_question_bank first (UUID)
    let questionResult = await pool.query(
      'SELECT * FROM coding_question_bank WHERE uuid = $1',
      [questionId]
    );
    
    let testCases = [];
    
    if (questionResult.rows.length > 0) {
      // Found in coding_question_bank
      const question = questionResult.rows[0];
      
      // Extract test cases from JSONB
      const allTestCases = question.test_cases || question.sample_test_cases || [];
      
      // Format test cases for frontend
      testCases = Array.isArray(allTestCases) ? allTestCases.map((tc, idx) => ({
        id: idx + 1,
        question_id: question.uuid,
        input: tc.input || tc.stdin || '',
        expected_output: tc.output || tc.stdout || tc.expected_output || '',
        test_order: idx + 1
      })) : [];
      
      res.json({
        success: true,
        question: {
          id: question.uuid,
          title: question.question || 'Untitled Question',
          description: question.question || '',
          difficulty: question.difficulty || 'Medium',
          tags: question.tags,
          boiler_plate: question.boiler_plate
        },
        test_cases: testCases
      });
      return;
    }
    
    // Try questions table (integer ID)
    const intId = parseInt(questionId);
    if (!isNaN(intId)) {
      questionResult = await pool.query(
        'SELECT * FROM questions WHERE id = $1',
        [intId]
      );
      
      if (questionResult.rows.length > 0) {
        // Get test cases from test_cases table
        const testCasesResult = await pool.query(
          'SELECT * FROM test_cases WHERE question_id = $1 ORDER BY test_order, id',
          [intId]
        );
        
        res.json({
          success: true,
          question: questionResult.rows[0],
          test_cases: testCasesResult.rows
        });
        return;
      }
    }
    
    // Not found in either table
    res.status(404).json({ success: false, error: 'Question not found' });
  } catch (error) {
    console.error('Error fetching question:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Create new question
app.post('/api/questions', async (req, res) => {
  try {
    const { title, description, difficulty } = req.body;

    if (!title) {
      return res.status(400).json({ success: false, error: 'Title is required' });
    }

    const result = await pool.query(
      'INSERT INTO questions (title, description, difficulty) VALUES ($1, $2, $3) RETURNING *',
      [title, description || '', difficulty || 'Medium']
    );

    res.json({ success: true, question: result.rows[0] });
  } catch (error) {
    console.error('Error creating question:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Update question
app.put('/api/questions/:id', async (req, res) => {
  try {
    const questionId = parseInt(req.params.id);
    const { title, description, difficulty } = req.body;

    const result = await pool.query(
      'UPDATE questions SET title = $1, description = $2, difficulty = $3, updated_at = CURRENT_TIMESTAMP WHERE id = $4 RETURNING *',
      [title, description, difficulty, questionId]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ success: false, error: 'Question not found' });
    }

    res.json({ success: true, question: result.rows[0] });
  } catch (error) {
    console.error('Error updating question:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Delete question
app.delete('/api/questions/:id', async (req, res) => {
  try {
    const questionId = parseInt(req.params.id);

    const result = await pool.query('DELETE FROM questions WHERE id = $1 RETURNING *', [questionId]);

    if (result.rows.length === 0) {
      return res.status(404).json({ success: false, error: 'Question not found' });
    }

    res.json({ success: true, message: 'Question deleted' });
  } catch (error) {
    console.error('Error deleting question:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Add test case to question
app.post('/api/questions/:id/testcases', async (req, res) => {
  try {
    const questionId = parseInt(req.params.id);
    const { input, expected_output, input_file, output_file } = req.body;

    // Get max test_order
    const maxOrderResult = await pool.query(
      'SELECT MAX(test_order) as max_order FROM test_cases WHERE question_id = $1',
      [questionId]
    );
    const nextOrder = (maxOrderResult.rows[0]?.max_order || 0) + 1;

    const result = await pool.query(
      'INSERT INTO test_cases (question_id, input, expected_output, input_file, output_file, test_order) VALUES ($1, $2, $3, $4, $5, $6) RETURNING *',
      [questionId, input || '', expected_output || '', input_file || null, output_file || null, nextOrder]
    );

    res.json({ success: true, test_case: result.rows[0] });
  } catch (error) {
    console.error('Error adding test case:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Update test case
app.put('/api/testcases/:id', async (req, res) => {
  try {
    const testCaseId = parseInt(req.params.id);
    const { input, expected_output, input_file, output_file } = req.body;

    const result = await pool.query(
      'UPDATE test_cases SET input = $1, expected_output = $2, input_file = $3, output_file = $4 WHERE id = $5 RETURNING *',
      [input, expected_output, input_file, output_file, testCaseId]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ success: false, error: 'Test case not found' });
    }

    res.json({ success: true, test_case: result.rows[0] });
  } catch (error) {
    console.error('Error updating test case:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Delete test case
app.delete('/api/testcases/:id', async (req, res) => {
  try {
    const testCaseId = parseInt(req.params.id);

    const result = await pool.query('DELETE FROM test_cases WHERE id = $1 RETURNING *', [testCaseId]);

    if (result.rows.length === 0) {
      return res.status(404).json({ success: false, error: 'Test case not found' });
    }

    res.json({ success: true, message: 'Test case deleted' });
  } catch (error) {
    console.error('Error deleting test case:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Proxy endpoint for executor (to avoid CORS)
app.get('/proxy/health', async (req, res) => {
  try {
    const executorUrl = 'https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io';
    const response = await fetch(`${executorUrl}/health`);
    const data = await response.json();
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// In-memory store for executions (for testing/monitoring)
// In production, this would be in a database
const executionsStore = [];

app.post('/proxy/execute', async (req, res) => {
  try {
    const executorUrl = 'https://ai-ta-ra-code-executor2.happypond-428960e8.eastus2.azurecontainerapps.io';
    const response = await fetch(`${executorUrl}/execute`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req.body)
    });
    const data = await response.json();
    
    // Store execution for monitoring (if successful) - ALWAYS store with full metadata
    if (response.ok && data.execution_id) {
      data.stored_at = new Date().toISOString();
      executionsStore.push(data);
      
      // Keep only last 1000 executions
      if (executionsStore.length > 1000) {
        executionsStore.shift();
      }
    }
    
    res.status(response.status).json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Store execution when received from executor
app.post('/api/monitoring/store', async (req, res) => {
  try {
    const execution = req.body;
    execution.stored_at = new Date().toISOString();
    executionsStore.push(execution);
    
    // Keep only last 1000 executions
    if (executionsStore.length > 1000) {
      executionsStore.shift();
    }
    
    res.json({ success: true, message: 'Execution stored' });
  } catch (error) {
    console.error('Error storing execution:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Monitoring endpoints
// Get all executions (for monitoring dashboard)
app.get('/api/monitoring/executions', async (req, res) => {
  console.log(`${new Date().toISOString()} - GET /api/monitoring/executions`);
  try {
    // Return executions from in-memory store
    // Format them for the dashboard
    const formattedExecutions = executionsStore.map(exec => ({
      execution_id: exec.execution_id || exec.metadata?.execution_id,
      user_id: exec.user_id,
      question_id: exec.question_id,
      submission_id: exec.submission_id || exec.metadata?.submission_id,
      language: exec.language,
      container_id: exec.metadata?.container_id || exec.metadata?.replica || 'unknown',
      replica_name: exec.metadata?.replica || 'unknown',
      status: exec.summary?.all_passed ? 'completed' : (exec.summary?.failed > 0 ? 'error' : 'completed'),
      tests_passed: exec.summary?.passed || 0,
      tests_total: exec.summary?.total_tests || 0,
      execution_time_ms: exec.metadata?.execution_time_ms || 0,
      cpu_usage_percent: exec.metadata?.cpu_usage_percent || 0,
      memory_usage_bytes: exec.metadata?.memory_usage_bytes || 0,
      memory_usage_mb: exec.metadata?.memory_usage_mb || (exec.metadata?.memory_usage_bytes ? exec.metadata.memory_usage_bytes / 1024 / 1024 : 0),
      timestamp: exec.timestamp || exec.stored_at
    }));
    
    // Sort by timestamp (newest first)
    formattedExecutions.sort((a, b) => {
      const timeA = new Date(a.timestamp || 0).getTime();
      const timeB = new Date(b.timestamp || 0).getTime();
      return timeB - timeA; // Newest first
    });
    
    res.json({ 
      success: true, 
      executions: formattedExecutions,
      count: formattedExecutions.length
    });
  } catch (error) {
    console.error('Error fetching executions:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Serve index.html
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Serve monitoring dashboard
app.get('/monitoring-dashboard.html', (req, res) => {
  res.sendFile(path.join(__dirname, 'monitoring-dashboard.html'));
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
  console.log(`📊 Database: PostgreSQL (Railway)`);
  console.log(`🌐 API Base URL: http://localhost:${PORT}/api`);
  console.log(`\n✅ Ready! Open http://localhost:${PORT} in your browser`);
});

