#!/usr/bin/env python3
"""
Fix question formatting in database - extract text and reformat properly
"""

import json
import os
import asyncpg
import asyncio
import re

DB_URL = os.getenv('DATABASE_URL', 'postgresql://postgresadmin:5oXcNX59QmEl7zmV3DbjemkiJ@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require')

def extract_text_from_html(html):
    """Extract all text content from HTML"""
    # Remove HTML tags but preserve structure
    text = re.sub(r'<h3>(.*?)</h3>', r'\n### \1\n', html)
    text = re.sub(r'<p>(.*?)</p>', r'\1\n', text)
    text = re.sub(r'<[^>]+>', ' ', text)
    # Clean up whitespace
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    return lines

def reformat_question_html(text_lines):
    """Reformat question as proper HTML"""
    html = "<h3>Problem</h3>\n<p>"
    
    current_para = []
    for line in text_lines:
        # Check for section headers
        if line.startswith('### '):
            if current_para:
                html += " ".join(current_para) + "</p>"
                current_para = []
            header = line.replace('### ', '').strip()
            html += f"\n<h3>{header}</h3>\n<p>"
        elif not line:
            if current_para:
                html += " ".join(current_para) + "</p>\n<p>"
                current_para = []
        else:
            current_para.append(line)
    
    if current_para:
        html += " ".join(current_para) + "</p>"
    
    return html

async def fix_all_questions():
    """Fix formatting for all questions in database"""
    conn = await asyncpg.connect(DB_URL)
    
    try:
        questions = await conn.fetch("SELECT uuid, question FROM coding_question_bank")
        
        print(f"📝 Fixing {len(questions)} questions...")
        
        for q in questions:
            uuid_val = q['uuid']
            current_html = q['question']
            
            # Extract text content
            text_lines = extract_text_from_html(current_html)
            
            # Check if first paragraph is too short
            if text_lines and len(text_lines[0]) < 30:
                # Try to find the actual problem description
                problem_start = 0
                for i, line in enumerate(text_lines):
                    if any(word in line.lower() for word in ['given', 'you have', 'an integer', 'determine', 'find']):
                        problem_start = i
                        break
                
                if problem_start > 0:
                    text_lines = text_lines[problem_start:]
            
            # Reformat
            new_html = reformat_question_html(text_lines)
            
            # Check if first paragraph has content
            start = new_html.find('<p>') + 3
            end = new_html.find('</p>', start)
            first_para = new_html[start:end] if end > start else ''
            
            if len(first_para.strip()) > 20:
                await conn.execute(
                    "UPDATE coding_question_bank SET question = $1 WHERE uuid = $2",
                    new_html, uuid_val
                )
                print(f"   ✅ Fixed: {uuid_val[:8]}... (first para: {len(first_para)} chars)")
            else:
                print(f"   ⚠️  Skipped: {uuid_val[:8]}... (first para still too short: {len(first_para)} chars)")
        
        print("\n✅ All questions processed!")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(fix_all_questions())




