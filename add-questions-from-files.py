#!/usr/bin/env python3
"""
Read questions from files and format them properly like Endpoint Inspection
"""

import json
import os
import asyncpg
import asyncio
import re
from pathlib import Path

DB_URL = os.getenv('DATABASE_URL', 'postgresql://postgresadmin:5oXcNX59QmEl7zmV3DbjemkiJ@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require')

def format_question_html(question_text):
    """Format question with proper HTML structure"""
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
        header_keywords = ["Example", "Function Description", "Constraints", "Input Format", "Sample Case", "Returns", "Explanation"]
        if any(line.startswith(kw) for kw in header_keywords):
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
        
        # Check if line looks like a list item
        if re.match(r'^[-•*]\s+', line) or re.match(r'^\d+[.)]\s+', line):
            if current_para:
                html += "<p>" + " ".join(current_para) + "</p>\n\n"
                current_para = []
            if not in_list:
                html += "<ul>\n"
                in_list = True
            list_item = re.sub(r'^[-•*]\s+', '', line)
            list_item = re.sub(r'^\d+[.)]\s+', '', list_item)
            list_items.append(list_item)
        elif line.startswith("    ") or (line.startswith("\t") and len(line) > 1):
            # Indented line
            if list_items:
                list_items[-1] += " " + line.strip()
            elif current_para:
                current_para.append(line.strip())
        else:
            # Regular paragraph text
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

async def update_all_questions():
    """Read questions from files and update database"""
    conn = await asyncpg.connect(DB_URL)
    
    try:
        # Question file mappings
        question_files = {
            "13725261-21c9-424b-bced-e0be21078aeb": "coding questions/Binary Manipulation /question",
            "cf43bce1-dfc7-4d42-904b-0d9461641076": "coding questions/Cartridge Recycling   /question",
            "2149e972-0cec-4da7-84bc-2526b4640f30": "coding questions/Modulo Challenge/question",
            "4d76d396-bf37-492d-86ba-2d611d2193c8": "coding questions/API Rate-Limiting   50 points  20 minute(s) Easy  Priority Queues  Data Structures  Interviewer Guidelines /question",
            "66f674e3-b85e-4175-8bcc-a25e9eeb8324": "coding questions/Maximal Permutation /question"
        }
        
        print("📝 Reading questions from files and formatting...")
        
        for uuid_val, q_path in question_files.items():
            q_file = Path(q_path)
            if not q_file.exists():
                print(f"   ⚠️  File not found: {q_path}")
                continue
            
            try:
                # Read file content
                question_text = q_file.read_text(encoding='utf-8')
                
                if not question_text or len(question_text.strip()) < 50:
                    print(f"   ⚠️  File empty or too short: {q_path}")
                    continue
                
                # Format with proper HTML
                question_html = format_question_html(question_text)
                
                # Check if first paragraph has content
                start = question_html.find('<p>') + 3
                end = question_html.find('</p>', start)
                first_para = question_html[start:end] if end > start else ''
                
                if len(first_para.strip()) > 20:
                    await conn.execute(
                        "UPDATE coding_question_bank SET question = $1 WHERE uuid = $2",
                        question_html, uuid_val
                    )
                    print(f"   ✅ Updated: {Path(q_path).parent.name} (first para: {len(first_para)} chars)")
                else:
                    print(f"   ⚠️  First para too short: {Path(q_path).parent.name}")
                    print(f"      Preview: {question_html[:150]}...")
            except Exception as e:
                print(f"   ❌ Error with {Path(q_path).parent.name}: {e}")
        
        print("\n✅ All questions updated!")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(update_all_questions())




