// Script to add a sample question to the database
// Run with: node add-sample-question.js

const { Pool } = require('pg');

const pool = new Pool({
  connectionString: 'postgresql://postgres:LpGWrOQpFdgLxybzTYWdGiAuJbitpizZ@yamanote.proxy.rlwy.net:55115/railway',
  ssl: { rejectUnauthorized: false }
});

async function addSampleQuestion() {
  try {
    console.log('Adding sample question...');

    // Add question
    const questionResult = await pool.query(
      `INSERT INTO questions (title, description, difficulty) 
       VALUES ($1, $2, $3) RETURNING *`,
      [
        'Two Sum',
        'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.\n\nYou can return the answer in any order.',
        'Easy'
      ]
    );

    const questionId = questionResult.rows[0].id;
    console.log(`✅ Question created with ID: ${questionId}`);

    // Add test cases
    const testCases = [
      { input: '5\n10', expected_output: '15' },
      { input: '100\n200', expected_output: '300' },
      { input: '-5\n5', expected_output: '0' }
    ];

    for (let i = 0; i < testCases.length; i++) {
      const tc = testCases[i];
      await pool.query(
        `INSERT INTO test_cases (question_id, input, expected_output, test_order) 
         VALUES ($1, $2, $3, $4)`,
        [questionId, tc.input, tc.expected_output, i + 1]
      );
      console.log(`✅ Test case ${i + 1} added`);
    }

    console.log('\n🎉 Sample question added successfully!');
    console.log(`Question ID: ${questionId}`);
    console.log('Refresh your browser to see it.');

    await pool.end();
  } catch (error) {
    console.error('Error:', error);
    await pool.end();
    process.exit(1);
  }
}

addSampleQuestion();


