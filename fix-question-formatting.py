#!/usr/bin/env python3
"""
Fix question formatting - properly format HTML for all questions
"""

import json
import os
import asyncpg
import asyncio
from pathlib import Path
import re

DB_URL = os.getenv('DATABASE_URL', 'postgresql://postgresadmin:5oXcNX59QmEl7zmV3DbjemkiJ@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require')

def format_question_html_properly(question_text):
    """Properly format question as HTML - handle different formats"""
    lines = [l.rstrip() for l in question_text.split('\n')]
    
    if not lines:
        return "<h3>Problem</h3><p>No description available.</p>"
    
    html = "<h3>Problem</h3>\n<p>"
    
    # Find where the actual problem description starts
    # Standard format: title (line 0), points (line 1), time (line 2), tags (line 3), then problem
    # Some questions start directly with problem description
    
    start_idx = 0
    # Check if it's standard format (has "points" or "minute" in early lines)
    for i in range(min(4, len(lines))):
        if 'point' in lines[i].lower() or 'minute' in lines[i].lower():
            start_idx = 4  # Skip title, points, time, tags
            break
    
    # Get problem content (skip metadata lines)
    content_lines = []
    for i in range(start_idx, len(lines)):
        line = lines[i]
        if line.strip():  # Only add non-empty lines
            content_lines.append(line)
        elif content_lines:  # Preserve empty lines between paragraphs
            content_lines.append("")
    
    current_para = []
    for line in content_lines:
        line = line.strip()
        line = line.strip()
        
        # Skip completely empty lines
        if not line:
            if current_para:
                html += " ".join(current_para) + "</p>\n<p>"
                current_para = []
            continue
        
        # Check for section headers
        header_keywords = ["Example", "Function Description", "Constraints", "Input Format", "Sample Case", "Returns", "Explanation"]
        is_header = any(line.startswith(kw) for kw in header_keywords)
        
        if is_header:
            if current_para:
                html += " ".join(current_para) + "</p>"
                current_para = []
            # Clean up header
            header = line
            if "Sample Case" in header:
                header = header.replace("Sample Case", "Example")
            if "Input Format For Custom Testing" in header:
                header = "Input Format"
            html += f"\n<h3>{header}</h3>\n<p>"
        else:
            current_para.append(line)
    
    if current_para:
        html += " ".join(current_para) + "</p>"
    
    return html

async def fix_all_questions():
    """Fix formatting for all questions"""
    conn = await asyncpg.connect(DB_URL)
    
    try:
        # Get all question UUIDs
        questions = await conn.fetch("SELECT uuid FROM coding_question_bank")
        
        print(f"📝 Fixing formatting for {len(questions)} questions...")
        
        for row in questions:
            uuid_val = row['uuid']
            
            # Get current question text from database
            current = await conn.fetchrow("SELECT question FROM coding_question_bank WHERE uuid = $1", uuid_val)
            if not current:
                continue
            
            # Re-read from file if possible, otherwise fix the stored one
            # For now, let's fix the stored format
            question_text = current['question']
            
            # Extract the actual problem text (remove HTML if present)
            # If it starts with <h3>Problem</h3>, extract the content
            if question_text.startswith("<h3>Problem</h3>"):
                # Already formatted, but might need fixing
                # Extract text between tags
                import re as regex
                text_only = regex.sub(r'<[^>]+>', ' ', question_text)
                text_only = ' '.join(text_only.split())
                
                # Try to find the original question file
                # For now, reformat the existing HTML properly
                # The issue is likely that it's missing proper structure
                pass
            
            # Better approach: read from question files if we can identify them
            # But since we don't have a mapping, let's fix the format function
            
            # Actually, let's just reformat all questions properly
            # We need to read from the question files again
            
        print("✅ Need to re-read question files to fix formatting")
        print("   This requires mapping UUIDs back to question files")
        
    finally:
        await conn.close()

# Let me create a better solution - re-process questions with proper formatting
async def reprocess_questions():
    """Re-process all questions with proper HTML formatting"""
    conn = await asyncpg.connect(DB_URL)
    
    try:
        # Question file mappings (we know the UUIDs from recent adds)
        question_mappings = {
            "13725261-21c9-424b-bced-e0be21078aeb": "coding questions/Binary Manipulation /question",
            "cf43bce1-dfc7-4d42-904b-0d9461641076": "coding questions/Cartridge Recycling   /question",
            "2149e972-0cec-4da7-84bc-2526b4640f30": "coding questions/Modulo Challenge/question",
            "4d76d396-bf37-492d-86ba-2d611d2193c8": "coding questions/API Rate-Limiting   50 points  20 minute(s) Easy  Priority Queues  Data Structures  Interviewer Guidelines /question",
            "66f674e3-b85e-4175-8bcc-a25e9eeb8324": "coding questions/Maximal Permutation /question"
        }
        
        print("📝 Re-formatting questions...")
        
        for uuid_val, q_file_path in question_mappings.items():
            q_file = Path(q_file_path)
            if not q_file.exists():
                print(f"   ⚠️  File not found: {q_file_path}")
                continue
            
            question_text = q_file.read_text()
            question_html = format_question_html_properly(question_text)
            
            # Update in database
            await conn.execute(
                "UPDATE coding_question_bank SET question = $1 WHERE uuid = $2",
                question_html, uuid_val
            )
            
            # Get title from first line or directory name
            first_line = question_text.split('\n')[0].strip()
            if len(first_line) > 50 or 'point' in first_line.lower():
                # Extract from path
                title = Path(q_file_path).parent.name.strip()
            else:
                title = first_line[:30]
            print(f"   ✅ Fixed: {title}...")
        
        print("\n✅ All questions reformatted!")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(reprocess_questions())

