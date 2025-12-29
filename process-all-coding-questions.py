#!/usr/bin/env python3
"""
Comprehensive script to process all coding questions:
1. Add solutions column (done)
2. Process each question from coding questions directory
3. Generate correct boilerplates for all languages
4. Add correct solutions (will need to solve each problem)
5. Update difficulty and tags
6. Remove old questions not in proper format
"""

import json
import os
import asyncpg
import asyncio
import uuid
from pathlib import Path
import re

DB_URL = os.getenv('DATABASE_URL', 'postgresql://postgresadmin:5oXcNX59QmEl7zmV3DbjemkiJ@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require')
CODING_QUESTIONS_DIR = Path("coding questions")

# Questions to keep (the 2 main ones)
QUESTIONS_TO_KEEP = [
    "d69847e4-e253-4400-9e44-febff93aeb3a",  # Warehouse Box Removal
    "eaec23b4-be2c-4b65-8745-15c265a56f75"   # Endpoint Inspection
]

async def main():
    """Main processing function"""
    print("🚀 Processing All Coding Questions")
    print("=" * 60)
    
    conn = await asyncpg.connect(DB_URL)
    
    try:
        # Step 1: Remove old questions not in proper format
        print("\n📋 Step 1: Cleaning old questions...")
        all_questions = await conn.fetch("SELECT uuid FROM coding_question_bank")
        removed_count = 0
        for row in all_questions:
            if row['uuid'] not in QUESTIONS_TO_KEEP:
                await conn.execute("DELETE FROM coding_question_bank WHERE uuid = $1", row['uuid'])
                removed_count += 1
        print(f"   ✅ Removed {removed_count} old questions")
        
        # Step 2: Process each question directory
        print("\n📋 Step 2: Processing questions from directory...")
        question_dirs = [d for d in CODING_QUESTIONS_DIR.iterdir() if d.is_dir()]
        
        for q_dir in question_dirs:
            print(f"\n   Processing: {q_dir.name}")
            try:
                await process_question(conn, q_dir)
            except Exception as e:
                print(f"   ❌ Error processing {q_dir.name}: {e}")
                import traceback
                traceback.print_exc()
        
        print("\n✅ All questions processed!")
        
    finally:
        await conn.close()

async def process_question(conn, q_dir):
    """Process a single question directory"""
    # Read question file
    question_file = q_dir / "question"
    if not question_file.exists():
        print(f"   ⚠️  No question file found, skipping")
        return
    
    question_text = question_file.read_text()
    
    # Read input path
    input_file = q_dir / "input"
    if not input_file.exists():
        print(f"   ⚠️  No input file found, skipping")
        return
    
    test_cases_dir = Path(input_file.read_text().strip())
    if not test_cases_dir.exists():
        print(f"   ⚠️  Test cases directory not found: {test_cases_dir}, skipping")
        return
    
    # Parse question metadata
    title = extract_title(question_text)
    difficulty = extract_difficulty(question_text)
    tags = extract_tags(question_text)
    function_info = extract_function_info(question_text)
    
    print(f"      Title: {title}")
    print(f"      Difficulty: {difficulty}")
    print(f"      Tags: {tags}")
    print(f"      Function: {function_info.get('name', 'N/A')}")
    
    # Read test cases
    sample_test_cases, test_cases = read_test_cases(test_cases_dir)
    print(f"      Test cases: {len(sample_test_cases)} sample, {len(test_cases)} regular")
    
    # Generate boilerplates
    boilerplates = generate_boilerplates(function_info)
    
    # Generate solutions (placeholder for now - will need to solve each problem)
    solutions = generate_solutions_placeholder(function_info)
    
    # Create question UUID
    question_uuid = str(uuid.uuid4())
    
    # Format question as HTML
    question_html = format_question_html(question_text)
    
    # Insert/update question
    await conn.execute("""
        INSERT INTO coding_question_bank (
            uuid, question, difficulty, tags,
            boiler_plate, sample_test_cases, test_cases, solutions
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        ON CONFLICT (uuid) DO UPDATE SET
            question = EXCLUDED.question,
            difficulty = EXCLUDED.difficulty,
            tags = EXCLUDED.tags,
            boiler_plate = EXCLUDED.boiler_plate,
            sample_test_cases = EXCLUDED.sample_test_cases,
            test_cases = EXCLUDED.test_cases,
            solutions = EXCLUDED.solutions
    """,
        question_uuid,
        question_html,
        difficulty.lower() if difficulty else "medium",
        json.dumps([tag.lower() for tag in tags]),
        json.dumps(boilerplates),
        json.dumps(sample_test_cases),
        json.dumps(test_cases),
        json.dumps(solutions)
    )
    
    print(f"      ✅ Added to database: {question_uuid}")

def extract_title(question_text):
    """Extract title from question text"""
    lines = question_text.split('\n')
    if lines:
        return lines[0].strip()
    return "Untitled Question"

def extract_difficulty(question_text):
    """Extract difficulty from question text"""
    text_lower = question_text.lower()
    if 'easy' in text_lower:
        return 'Easy'
    elif 'medium' in text_lower:
        return 'Medium'
    elif 'hard' in text_lower:
        return 'Hard'
    return 'Medium'

def extract_tags(question_text):
    """Extract tags from question text"""
    tags = []
    lines = question_text.split('\n')
    for line in lines[:5]:  # Check first few lines
        if any(keyword in line.lower() for keyword in ['array', 'graph', 'tree', 'string', 'dynamic', 'greedy', 'sorting']):
            # Extract potential tags
            words = line.split()
            for word in words:
                if word.isalpha() and len(word) > 3:
                    tags.append(word)
    # Default tags if none found
    if not tags:
        tags = ['algorithms', 'problem solving']
    return tags[:5]  # Limit to 5 tags

def extract_function_info(question_text):
    """Extract function name, parameters, return type from question"""
    # This is a simplified parser - will need refinement per question
    info = {
        'name': 'solve',
        'params': [],
        'return_type': 'List[int]'
    }
    
    # Try to find function name
    match = re.search(r'function\s+(\w+)', question_text, re.IGNORECASE)
    if match:
        info['name'] = match.group(1)
    
    # Try to find return type
    if 'int[]' in question_text or 'vector<int>' in question_text:
        info['return_type'] = 'List[int]'
    elif 'int' in question_text and '[]' not in question_text:
        info['return_type'] = 'int'
    elif 'long' in question_text.lower():
        info['return_type'] = 'long'
    
    return info

def read_test_cases(test_dir):
    """Read test cases from directory"""
    sample_test_cases = []
    test_cases = []
    
    input_files = sorted([f for f in test_dir.glob("input*.txt")])
    
    for i, input_file in enumerate(input_files):
        test_num = input_file.stem.replace("input", "")
        output_file = test_dir / f"output{test_num}.txt"
        
        if not output_file.exists():
            continue
        
        input_data = input_file.read_text().strip()
        output_data = output_file.read_text().strip()
        
        test_case = {
            "id": f"test_case_{test_num}",
            "input": input_data,
            "expected_output": output_data
        }
        
        # First 3 are sample
        if i < 3:
            sample_test_cases.append(test_case)
        else:
            test_cases.append(test_case)
    
    return sample_test_cases, test_cases

def generate_boilerplates(function_info):
    """Generate boilerplates for all languages"""
    # This is a simplified version - will need to be customized per question
    # For now, return placeholder structure
    return {
        "python": f"def {function_info['name']}():\n    # Write your code here\n",
        "cpp": f"vector<int> {function_info['name']}() {{\n    // Write your code here\n}}",
        "java": f"class Result {{\n    public static List<Integer> {function_info['name']}() {{\n    // Write your code here\n    }}\n}}",
        "javascript": f"function {function_info['name']}() {{\n    // Write your code here\n}}",
        "csharp": f"class Result {{\n    public static List<int> {function_info['name']}() {{\n    // Write your code here\n    }}\n}}"
    }

def generate_solutions_placeholder(function_info):
    """Generate placeholder solutions - will need to solve each problem"""
    return {
        "python": "# Solution to be implemented",
        "cpp": "// Solution to be implemented",
        "java": "// Solution to be implemented",
        "javascript": "// Solution to be implemented",
        "csharp": "// Solution to be implemented"
    }

def format_question_html(question_text):
    """Format question text as HTML"""
    # Simple formatting - convert to HTML
    lines = question_text.split('\n')
    html = "<h3>Problem</h3>\n<p>"
    html += "</p>\n<p>".join(lines[:10])
    html += "</p>"
    return html

if __name__ == "__main__":
    asyncio.run(main())




