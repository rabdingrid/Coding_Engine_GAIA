#!/usr/bin/env python3
"""
Fix question formatting properly - ensure first lines are included
"""

import json
import os
import asyncpg
import asyncio
from pathlib import Path

DB_URL = os.getenv('DATABASE_URL', 'postgresql://postgresadmin:5oXcNX59QmEl7zmV3DbjemkiJ@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require')

def format_question_html_properly(question_text):
    """Properly format question as HTML"""
    if not question_text or not question_text.strip():
        return "<h3>Problem</h3><p>No description available.</p>"
    
    lines = question_text.split('\n')
    
    html = "<h3>Problem</h3>\n<p>"
    
    # Determine start index - skip metadata lines
    # Standard format: title (line 0), points (line 1), time (line 2), tags (line 3), problem (line 4+)
    # Some questions start directly with problem description
    
    start_idx = 0
    # Check if line 1 or 2 has "points" or "minute" (indicating standard format)
    if len(lines) > 1:
        line1 = lines[1].strip().lower() if lines[1] else ""
        if 'point' in line1 or 'minute' in line1:
            start_idx = 4  # Skip: title, points, time, tags
    if len(lines) > 2 and start_idx == 0:
        line2 = lines[2].strip().lower() if lines[2] else ""
        if 'point' in line2 or 'minute' in line2:
            start_idx = 4  # Skip: title, points, time, tags
    
    # Process content lines
    current_para = []
    has_content = False
    
    for i in range(start_idx, len(lines)):
        line = lines[i].strip()
        
        # Empty line - end current paragraph
        if not line:
            if current_para:
                html += " ".join(current_para) + "</p>\n<p>"
                current_para = []
                has_content = True
            continue
        
        # Check for section headers
        if any(line.startswith(kw) for kw in ["Example", "Function Description", "Constraints", "Input Format", "Sample Case", "Returns", "Explanation"]):
            if current_para:
                html += " ".join(current_para) + "</p>"
                current_para = []
            # Clean header
            header = line.replace("Sample Case", "Example").replace("Input Format For Custom Testing", "Input Format")
            html += f"\n<h3>{header}</h3>\n<p>"
            has_content = True
        else:
            # Regular content line
            current_para.append(line)
            has_content = True
    
    # Close last paragraph
    if current_para:
        html += " ".join(current_para) + "</p>"
    elif not has_content:
        # If no content was added, try to use first non-empty line
        for line in lines:
            if line.strip() and not any(x in line.lower() for x in ['point', 'minute']):
                html += line.strip() + "</p>"
                break
        else:
            html += "Problem description not available.</p>"
    
    return html

async def fix_all():
    """Fix all questions"""
    conn = await asyncpg.connect(DB_URL)
    
    try:
        mappings = {
            "13725261-21c9-424b-bced-e0be21078aeb": "coding questions/Binary Manipulation /question",
            "cf43bce1-dfc7-4d42-904b-0d9461641076": "coding questions/Cartridge Recycling   /question",
            "2149e972-0cec-4da7-84bc-2526b4640f30": "coding questions/Modulo Challenge/question",
            "4d76d396-bf37-492d-86ba-2d611d2193c8": "coding questions/API Rate-Limiting   50 points  20 minute(s) Easy  Priority Queues  Data Structures  Interviewer Guidelines /question",
            "66f674e3-b85e-4175-8bcc-a25e9eeb8324": "coding questions/Maximal Permutation /question"
        }
        
        print("📝 Fixing question formatting...")
        
        for uuid_val, q_path in mappings.items():
            q_file = Path(q_path)
            if q_file.exists():
                question_text = q_file.read_text(encoding='utf-8')
                question_html = format_question_html_properly(question_text)
                
                await conn.execute(
                    "UPDATE coding_question_bank SET question = $1 WHERE uuid = $2",
                    question_html, uuid_val
                )
                
                # Verify first paragraph has content
                if "<p>Given" in question_html or "<p>You" in question_html or "<p>An" in question_html:
                    print(f"   ✅ Fixed: {Path(q_path).parent.name}")
                else:
                    print(f"   ⚠️  Check: {Path(q_path).parent.name} (first para might be empty)")
        
        print("\n✅ All questions updated!")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(fix_all())

