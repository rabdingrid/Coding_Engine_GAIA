#!/usr/bin/env python3
"""
Extract question content from database HTML and reformat properly like Endpoint Inspection
"""

import json
import os
import asyncpg
import asyncio
import re

DB_URL = os.getenv('DATABASE_URL', 'postgresql://postgresadmin:5oXcNX59QmEl7zmV3DbjemkiJ@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require')

def extract_and_format_from_html(html):
    """
    Extract text from HTML and reformat with proper structure
    """
    if not html:
        return "<h3>Problem</h3>\n<p>No description available.</p>"
    
    # Extract all text content, preserving some structure
    text = html
    
    # Replace existing HTML tags with markers
    text = re.sub(r'<h3>(.*?)</h3>', r'[HEADER]\1[/HEADER]', text)
    text = re.sub(r'<p>(.*?)</p>', r'\1\n', text)
    text = re.sub(r'<ul>', '[LIST_START]', text)
    text = re.sub(r'</ul>', '[LIST_END]', text)
    text = re.sub(r'<li>(.*?)</li>', r'[ITEM]\1[/ITEM]', text)
    text = re.sub(r'<[^>]+>', ' ', text)  # Remove any remaining tags
    
    # Split into lines
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    # Rebuild HTML properly
    html_output = "<h3>Problem</h3>\n\n"
    
    current_para = []
    in_list = False
    
    for line in lines:
        # Handle headers
        if '[HEADER]' in line:
            if current_para:
                html_output += "<p>" + " ".join(current_para) + "</p>\n\n"
                current_para = []
            if in_list:
                html_output += "</ul>\n\n"
                in_list = False
            header = line.replace('[HEADER]', '').replace('[/HEADER]', '').strip()
            html_output += f"<h3>{header}</h3>\n\n"
            continue
        
        # Handle list items
        if '[ITEM]' in line:
            if current_para:
                html_output += "<p>" + " ".join(current_para) + "</p>\n\n"
                current_para = []
            if not in_list:
                html_output += "<ul>\n"
                in_list = True
            item = line.replace('[ITEM]', '').replace('[/ITEM]', '').strip()
            html_output += f"    <li>{item}</li>\n"
            continue
        
        if '[LIST_START]' in line:
            if current_para:
                html_output += "<p>" + " ".join(current_para) + "</p>\n\n"
                current_para = []
            if not in_list:
                html_output += "<ul>\n"
                in_list = True
            continue
        
        if '[LIST_END]' in line:
            if in_list:
                html_output += "</ul>\n\n"
                in_list = False
            continue
        
        # Regular text
        if line:
            # Check if it looks like a list item (starts with bullet-like pattern)
            if re.match(r'^[-•*]\s+', line) or re.match(r'^\d+[.)]\s+', line):
                if current_para:
                    html_output += "<p>" + " ".join(current_para) + "</p>\n\n"
                    current_para = []
                if not in_list:
                    html_output += "<ul>\n"
                    in_list = True
                item = re.sub(r'^[-•*]\s+', '', line)
                item = re.sub(r'^\d+[.)]\s+', '', item)
                html_output += f"    <li>{item}</li>\n"
            else:
                current_para.append(line)
    
    # Close any remaining content
    if in_list:
        html_output += "</ul>\n\n"
    if current_para:
        html_output += "<p>" + " ".join(current_para) + "</p>\n\n"
    
    return html_output.strip()

async def reformat_all():
    """Reformat all questions from database HTML"""
    conn = await asyncpg.connect(DB_URL)
    
    try:
        questions = await conn.fetch("SELECT uuid, question FROM coding_question_bank")
        
        print(f"📝 Reformatting {len(questions)} questions...")
        
        for q in questions:
            uuid_val = q['uuid']
            current_html = q['question']
            
            # Skip Endpoint Inspection (already properly formatted)
            if uuid_val == 'eaec23b4-be2c-4b65-8745-15c265a56f75':
                print(f"   ⏭️  Skipped: {uuid_val[:8]}... (Endpoint Inspection - already formatted)")
                continue
            
            new_html = extract_and_format_from_html(current_html)
            
            # Check if first paragraph has content
            start = new_html.find('<p>') + 3
            end = new_html.find('</p>', start)
            first_para = new_html[start:end] if end > start else ''
            
            if len(first_para.strip()) > 20:
                await conn.execute(
                    "UPDATE coding_question_bank SET question = $1 WHERE uuid = $2",
                    new_html, uuid_val
                )
                print(f"   ✅ Formatted: {uuid_val[:8]}... (first para: {len(first_para)} chars)")
            else:
                print(f"   ⚠️  Skipped: {uuid_val[:8]}... (first para too short: {len(first_para)} chars)")
                # Show preview
                print(f"      Preview: {new_html[:100]}...")
        
        print("\n✅ All questions reformatted!")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(reformat_all())




