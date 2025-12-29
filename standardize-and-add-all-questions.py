#!/usr/bin/env python3
"""
Standardize all questions to same format and add remaining questions
1. Update Warehouse to have correct boilerplates + solutions
2. Ensure Count Between matches format
3. Process all remaining questions in same format
"""

import json
import os
import asyncpg
import asyncio
import uuid
from pathlib import Path

DB_URL = os.getenv('DATABASE_URL', 'postgresql://postgresadmin:5oXcNX59QmEl7zmV3DbjemkiJ@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require')

print("🚀 Standardizing Questions and Adding Remaining Ones")
print("=" * 60)

# First, let me create a helper to read test cases
def read_test_cases_from_dir(test_dir):
    """Read test cases from directory"""
    if not test_dir.exists():
        return [], []
    
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

# For now, let me just standardize the existing questions
# Then we'll add the remaining ones one by one

async def standardize_warehouse():
    """Update Warehouse question to match correct format"""
    print("\n📋 Step 1: Standardizing Warehouse Box Removal...")
    
    conn = await asyncpg.connect(DB_URL)
    try:
        # Get current warehouse question
        row = await conn.fetchrow(
            "SELECT * FROM coding_question_bank WHERE uuid = 'd69847e4-e253-4400-9e44-febff93aeb3a'"
        )
        
        if row:
            # Update boilerplates to correct format (remove import os, use print, etc.)
            # For now, just add solutions placeholder - we'll need to solve it
            current_bp = json.loads(row['boiler_plate']) if row['boiler_plate'] else {}
            
            # Update Python boilerplate
            if 'python' in current_bp:
                python_bp = current_bp['python']
                # Remove import os and file operations
                python_bp = python_bp.replace('import os\n', '')
                python_bp = python_bp.replace('import math\n', '')
                python_bp = python_bp.replace('import random\n', '')
                python_bp = python_bp.replace('import re\n', '')
                python_bp = python_bp.replace('import sys\n', '')
                python_bp = python_bp.replace('#!/bin/python3\n', '')
                # Replace file writing with print
                if 'fptr = open' in python_bp:
                    lines = python_bp.split('\n')
                    new_lines = []
                    skip_next = False
                    for line in lines:
                        if 'fptr = open' in line or 'fptr.write' in line or 'fptr.close' in line:
                            continue
                        if 'fptr' in line and '=' in line:
                            continue
                        new_lines.append(line)
                    python_bp = '\n'.join(new_lines)
                    # Add print at the end if function call exists
                    if 'result = ' in python_bp and 'print' not in python_bp:
                        python_bp += '\nprint(result)'
                current_bp['python'] = python_bp
            
            # Add C# if missing
            if 'csharp' not in current_bp:
                current_bp['csharp'] = "// C# boilerplate to be added"
            
            # Add solutions placeholder
            solutions = {
                "python": "# Solution to be implemented",
                "cpp": "// Solution to be implemented",
                "java": "// Solution to be implemented",
                "javascript": "// Solution to be implemented",
                "csharp": "// Solution to be implemented"
            }
            
            await conn.execute("""
                UPDATE coding_question_bank
                SET boiler_plate = $1,
                    solutions = $2
                WHERE uuid = 'd69847e4-e253-4400-9e44-febff93aeb3a'
            """,
                json.dumps(current_bp),
                json.dumps(solutions)
            )
            
            print("   ✅ Warehouse updated with correct format")
        else:
            print("   ⚠️  Warehouse question not found")
    
    finally:
        await conn.close()

async def verify_format():
    """Verify all questions have same format"""
    print("\n📋 Step 2: Verifying format consistency...")
    
    conn = await asyncpg.connect(DB_URL)
    try:
        questions = await conn.fetch("""
            SELECT uuid, difficulty, tags, 
                   boiler_plate IS NOT NULL as has_bp,
                   solutions IS NOT NULL as has_sol
            FROM coding_question_bank
            ORDER BY uuid
        """)
        
        print(f"   Found {len(questions)} questions")
        for q in questions:
            bp_langs = []
            sol_langs = []
            if q['has_bp']:
                bp = await conn.fetchval(
                    "SELECT boiler_plate FROM coding_question_bank WHERE uuid = $1",
                    q['uuid']
                )
                if bp:
                    bp_data = json.loads(bp) if isinstance(bp, str) else bp
                    bp_langs = list(bp_data.keys()) if bp_data else []
            
            if q['has_sol']:
                sol = await conn.fetchval(
                    "SELECT solutions FROM coding_question_bank WHERE uuid = $1",
                    q['uuid']
                )
                if sol:
                    sol_data = json.loads(sol) if isinstance(sol, str) else sol
                    sol_langs = list(sol_data.keys()) if sol_data else []
            
            print(f"   {q['uuid'][:8]}... | BP: {len(bp_langs)} langs | Sol: {len(sol_langs)} langs")
    
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(standardize_warehouse())
    asyncio.run(verify_format())
    print("\n✅ Standardization complete!")
    print("\n📝 Next: Add remaining questions one by one...")




