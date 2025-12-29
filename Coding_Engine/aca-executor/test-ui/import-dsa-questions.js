#!/usr/bin/env node
/**
 * Import DSA Questions from File System to Database
 * Reads questions from dsa-questions/ directory and imports to PostgreSQL
 */

const { Pool } = require('pg');
const fs = require('fs');
const path = require('path');

const pool = new Pool({
  connectionString: 'postgresql://postgres:LpGWrOQpFdgLxybzTYWdGiAuJbitpizZ@yamanote.proxy.rlwy.net:55115/railway',
  ssl: { rejectUnauthorized: false }
});

const BASE_DIR = path.join(__dirname, '../../dsa-questions');

async function importQuestions() {
  console.log('🚀 Starting DSA Questions Import...\n');
  
  try {
    // Get all question directories
    const questionDirs = fs.readdirSync(BASE_DIR)
      .filter(dir => dir.startsWith('Q') && fs.statSync(path.join(BASE_DIR, dir)).isDirectory())
      .sort();
    
    console.log(`📁 Found ${questionDirs.length} questions to import\n`);
    
    let imported = 0;
    let skipped = 0;
    
    for (const qDir of questionDirs) {
      const qPath = path.join(BASE_DIR, qDir);
      
      try {
        // Read metadata
        const metadataPath = path.join(qPath, 'metadata.json');
        if (!fs.existsSync(metadataPath)) {
          console.log(`⚠️  Skipping ${qDir}: metadata.json not found`);
          skipped++;
          continue;
        }
        
        const metadata = JSON.parse(fs.readFileSync(metadataPath, 'utf8'));
        
        // Read problem description
        const problemPath = path.join(qPath, 'problem.md');
        const problemDescription = fs.existsSync(problemPath) 
          ? fs.readFileSync(problemPath, 'utf8')
          : '';
        
        // Read test cases
        const testCasesDir = path.join(qPath, 'test_cases');
        const testCases = [];
        
        if (fs.existsSync(testCasesDir)) {
          const testFiles = fs.readdirSync(testCasesDir)
            .filter(f => f.endsWith('.in'))
            .sort();
          
          for (const inFile of testFiles) {
            const tcNum = inFile.replace('.in', '');
            const outFile = path.join(testCasesDir, `${tcNum}.out`);
            
            if (fs.existsSync(outFile)) {
              const input = fs.readFileSync(path.join(testCasesDir, inFile), 'utf8').trim();
              const output = fs.readFileSync(outFile, 'utf8').trim();
              
              testCases.push({
                input: input,
                output: output,
                stdin: input,
                stdout: output,
                expected_output: output
              });
            }
          }
        }
        
        // Read boilerplates
        const boilerplatesDir = path.join(qPath, 'boilerplates');
        const boilerplates = {};
        
        if (fs.existsSync(boilerplatesDir)) {
          const boilerplateFiles = fs.readdirSync(boilerplatesDir);
          
          for (const bpFile of boilerplateFiles) {
            const lang = bpFile.split('.')[0];
            const content = fs.readFileSync(path.join(boilerplatesDir, bpFile), 'utf8');
            boilerplates[lang] = content;
          }
        }
        
        // Ensure boilerplates is a valid JSON object (not null/undefined)
        const boilerplatesJson = Object.keys(boilerplates).length > 0 ? boilerplates : {};
        
        // Check if question already exists
        const checkResult = await pool.query(
          'SELECT uuid FROM coding_question_bank WHERE uuid = $1',
          [metadata.uuid]
        );
        
        if (checkResult.rows.length > 0) {
          // Update existing question
          await pool.query(
            `UPDATE coding_question_bank 
             SET question = $1, 
                 difficulty = $2, 
                 tags = $3, 
                 test_cases = $4, 
                 sample_test_cases = $5,
                 boiler_plate = $6
             WHERE uuid = $7`,
            [
              problemDescription || metadata.title,
              metadata.difficulty,
              JSON.stringify(metadata.tags || []),
              JSON.stringify(testCases),
              JSON.stringify(testCases.slice(0, 3)), // First 3 as sample
              JSON.stringify(boilerplatesJson),
              metadata.uuid
            ]
          );
          console.log(`✅ Updated ${qDir}: ${metadata.title} (${testCases.length} test cases)`);
        } else {
          // Insert new question
          await pool.query(
            `INSERT INTO coding_question_bank 
             (uuid, question, difficulty, tags, test_cases, sample_test_cases, boiler_plate)
             VALUES ($1, $2, $3, $4, $5, $6, $7)`,
            [
              metadata.uuid,
              problemDescription || metadata.title,
              metadata.difficulty,
              JSON.stringify(metadata.tags || []),
              JSON.stringify(testCases),
              JSON.stringify(testCases.slice(0, 3)), // First 3 as sample
              JSON.stringify(boilerplatesJson)
            ]
          );
          console.log(`✅ Imported ${qDir}: ${metadata.title} (${testCases.length} test cases)`);
        }
        
        imported++;
      } catch (error) {
        console.error(`❌ Error importing ${qDir}:`, error.message);
        skipped++;
      }
    }
    
    console.log(`\n📊 Summary:`);
    console.log(`   ✅ Imported: ${imported}`);
    console.log(`   ⚠️  Skipped: ${skipped}`);
    console.log(`   📝 Total: ${questionDirs.length}`);
    
  } catch (error) {
    console.error('❌ Import failed:', error);
    process.exit(1);
  } finally {
    await pool.end();
  }
}

// Run import
importQuestions().catch(console.error);

