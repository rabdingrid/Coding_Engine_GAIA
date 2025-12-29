#!/usr/bin/env python3
"""
Format all questions like Endpoint Inspection - with proper HTML structure
"""

import json
import os
import asyncpg
import asyncio
import re
from pathlib import Path

DB_URL = os.getenv('DATABASE_URL', 'postgresql://postgresadmin:5oXcNX59QmEl7zmV3DbjemkiJ@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require')

def format_question_properly(question_text):
    """
    Format question with proper HTML structure like Endpoint Inspection
    """
    if not question_text or not question_text.strip():
        return "<h3>Problem</h3>\n<p>No description available.</p>"
    
    lines = [l.rstrip() for l in question_text.split('\n')]
    
    # Skip metadata lines (title, points, time, tags)
    start_idx = 0
    for i in range(min(4, len(lines))):
        if 'point' in lines[i].lower() or 'minute' in lines[i].lower():
            start_idx = 4
            break
    
    html = "<h3>Problem</h3>\n\n"
    
    current_para = []
    in_list = False
    list_items = []
    
    for i in range(start_idx, len(lines)):
        line = lines[i].strip()
        
        # Empty line
        if not line:
            if list_items:
                html += "<ul>\n"
                for item in list_items:
                    html += f"    <li>{item}</li>\n"
                html += "</ul>\n\n"
                list_items = []
                in_list = False
            elif current_para:
                html += "<p>" + " ".join(current_para) + "</p>\n\n"
                current_para = []
            continue
        
        # Section headers
        if any(line.startswith(kw) for kw in ["Example", "Function Description", "Constraints", "Input Format", "Sample Case", "Returns", "Explanation"]):
            if list_items:
                html += "<ul>\n"
                for item in list_items:
                    html += f"    <li>{item}</li>\n"
                html += "</ul>\n\n"
                list_items = []
                in_list = False
            if current_para:
                html += "<p>" + " ".join(current_para) + "</p>\n\n"
                current_para = []
            
            header = line.replace("Sample Case", "Example").replace("Input Format For Custom Testing", "Input Format")
            html += f"<h3>{header}</h3>\n\n"
            continue
        
        # Check if line looks like a list item (starts with bullet, dash, or number)
        if re.match(r'^[-•*]\s+', line) or re.match(r'^\d+[.)]\s+', line):
            if current_para:
                html += "<p>" + " ".join(current_para) + "</p>\n\n"
                current_para = []
            # Remove bullet/number
            list_item = re.sub(r'^[-•*]\s+', '', line)
            list_item = re.sub(r'^\d+[.)]\s+', '', list_item)
            list_items.append(list_item)
            in_list = True
        elif line.startswith("    ") or line.startswith("\t"):  # Indented line (sub-list or continuation)
            if current_para:
                current_para.append(line.strip())
            elif list_items:
                # Continuation of list item
                if list_items:
                    list_items[-1] += " " + line.strip()
        else:
            if list_items:
                html += "<ul>\n"
                for item in list_items:
                    html += f"    <li>{item}</li>\n"
                html += "</ul>\n\n"
                list_items = []
                in_list = False
            current_para.append(line)
    
    # Close any remaining content
    if list_items:
        html += "<ul>\n"
        for item in list_items:
            html += f"    <li>{item}</li>\n"
        html += "</ul>\n\n"
    
    if current_para:
        html += "<p>" + " ".join(current_para) + "</p>\n\n"
    
    return html.strip()

async def format_all_questions():
    """Format all questions with proper HTML structure"""
    conn = await asyncpg.connect(DB_URL)
    
    try:
        # Get all questions
        questions = await conn.fetch("SELECT uuid, question FROM coding_question_bank")
        
        print(f"📝 Formatting {len(questions)} questions...")
        
        # Try to read from files first, fallback to extracting from current HTML
        question_files = {
            "13725261-21c9-424b-bced-e0be21078aeb": "coding questions/Binary Manipulation /question",
            "cf43bce1-dfc7-4d42-904b-0d9461641076": "coding questions/Cartridge Recycling   /question",
            "2149e972-0cec-4da7-84bc-2526b4640f30": "coding questions/Modulo Challenge/question",
            "4d76d396-bf37-492d-86ba-2d611d2193c8": "coding questions/API Rate-Limiting   50 points  20 minute(s) Easy  Priority Queues  Data Structures  Interviewer Guidelines /question",
            "66f674e3-b85e-4175-8bcc-a25e9eeb8324": "coding questions/Maximal Permutation /question"
        }
        
        for q in questions:
            uuid_val = q['uuid']
            current_html = q['question']
            
            # Try to read from file
            question_text = None
            if uuid_val in question_files:
                q_file = Path(question_files[uuid_val])
                if q_file.exists() and q_file.stat().st_size > 0:
                    try:
                        question_text = q_file.read_text(encoding='utf-8')
                    except:
                        pass
            
            # If file doesn't exist or is empty, extract from current HTML
            if not question_text:
                # Extract text from HTML
                text = re.sub(r'<[^>]+>', ' ', current_html)
                text = ' '.join(text.split())
                # This is a fallback - not ideal but better than nothing
                question_text = text
            
            if question_text and len(question_text.strip()) > 50:
                new_html = format_question_properly(question_text)
                
                # Check if first paragraph has content
                start = new_html.find('<p>') + 3
                end = new_html.find('</p>', start)
                first_para = new_html[start:end] if end > start else ''
                
                if len(first_para.strip()) > 20:
                    await conn.execute(
                        "UPDATE coding_question_bank SET question = $1 WHERE uuid = $2",
                        new_html, uuid_val
                    )
                    print(f"   ✅ Formatted: {uuid_val[:8]}...")
                else:
                    print(f"   ⚠️  Skipped: {uuid_val[:8]}... (first para too short)")
            else:
                print(f"   ⚠️  Skipped: {uuid_val[:8]}... (no source text found)")
        
        print("\n✅ All questions formatted!")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(format_all_questions())




