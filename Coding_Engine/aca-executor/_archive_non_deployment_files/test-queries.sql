-- Azure PostgreSQL Test Queries
-- Use these in Azure Data Studio to test your connection

-- 1. Check database version
SELECT version();

-- 2. List all tables
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;

-- 3. Count questions in coding_question_bank
SELECT COUNT(*) as total_questions FROM coding_question_bank;

-- 4. View sample questions
SELECT id, uuid, question, difficulty, tags 
FROM coding_question_bank 
LIMIT 10;

-- 5. View all table names with row counts
SELECT 
    schemaname,
    tablename,
    (SELECT COUNT(*) FROM information_schema.tables t2 
     WHERE t2.table_schema = t.schemaname 
     AND t2.table_name = t.tablename) as estimated_rows
FROM pg_tables t
WHERE schemaname = 'public'
ORDER BY tablename;

-- 6. Check table structure
SELECT 
    column_name,
    data_type,
    character_maximum_length,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'coding_question_bank'
ORDER BY ordinal_position;

-- 7. View test cases for a question
SELECT * FROM test_cases LIMIT 5;

-- 8. Count records in each table
SELECT 
    'coding_question_bank' as table_name, 
    COUNT(*) as record_count 
FROM coding_question_bank
UNION ALL
SELECT 'test_cases', COUNT(*) FROM test_cases
UNION ALL
SELECT 'users', COUNT(*) FROM users
UNION ALL
SELECT 'candidate', COUNT(*) FROM candidate
UNION ALL
SELECT 'jobs', COUNT(*) FROM jobs;

