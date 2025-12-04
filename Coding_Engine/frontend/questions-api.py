#!/usr/bin/env python3
"""
Backend API to fetch questions from PostgreSQL database
Run with: python3 questions-api.py
"""

import os
import json
import asyncpg
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import sys

# Database connection - Railway PostgreSQL
DB_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:LpGWrOQpFdgLxybzTYWdGiAuJbitpizZ@yamanote.proxy.rlwy.net:55115/railway')

class QuestionsAPIHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/api/questions':
            self.handle_get_questions()
        elif path.startswith('/api/questions/'):
            question_id = path.split('/')[-1]
            self.handle_get_question(question_id)
        else:
            self.send_response(404)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())
    
    def send_cors_headers(self):
        """Send CORS headers"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Type', 'application/json')
    
    async def get_db_connection(self):
        """Get database connection"""
        return await asyncpg.connect(DB_URL)
    
    def handle_get_questions(self):
        """Get all questions"""
        import asyncio
        
        # Create new event loop for this request
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        except:
            loop = asyncio.get_event_loop()
        
        async def fetch_questions():
            try:
                conn = await asyncpg.connect(DB_URL)
                rows = await conn.fetch("""
                    SELECT uuid, question, sample_test_cases, test_cases, boiler_plate, difficulty, tags
                    FROM coding_question_bank
                    ORDER BY uuid
                """)
                
                questions = []
                for row in rows:
                    try:
                        # Parse JSONB fields - asyncpg returns JSONB as strings, need to parse
                        import json as json_lib
                        
                        # Parse question (can be string or dict)
                        question_data = row['question']
                        if isinstance(question_data, str):
                            try:
                                # Try to parse as JSON first
                                parsed = json_lib.loads(question_data)
                                # If it's a dict/object, use it
                                if isinstance(parsed, dict):
                                    question_data = parsed
                                else:
                                    # If parsed but not a dict, keep as string
                                    question_data = question_data
                            except:
                                # Not JSON, keep as string - we'll extract title from it
                                question_data = question_data
                        
                        # Parse sample_test_cases
                        sample_tests = row['sample_test_cases']
                        if isinstance(sample_tests, str):
                            try:
                                sample_tests = json_lib.loads(sample_tests) if sample_tests else []
                            except:
                                sample_tests = []
                        sample_tests = sample_tests if sample_tests else []
                        
                        # Parse test_cases
                        all_tests = row['test_cases']
                        if isinstance(all_tests, str):
                            try:
                                all_tests = json_lib.loads(all_tests) if all_tests else []
                            except:
                                all_tests = []
                        all_tests = all_tests if all_tests else []
                        
                        # Parse boiler_plate
                        boilerplate = row['boiler_plate']
                        if isinstance(boilerplate, str):
                            try:
                                boilerplate = json_lib.loads(boilerplate) if boilerplate else {}
                            except:
                                boilerplate = {}
                        boilerplate = boilerplate if boilerplate else {}
                        
                        # Parse tags
                        tags = row['tags']
                        if isinstance(tags, str):
                            try:
                                tags = json_lib.loads(tags) if tags else []
                            except:
                                tags = []
                        tags = tags if isinstance(tags, list) else []
                        
                        # Convert test cases to proper format
                        test_cases_list = []
                        if isinstance(all_tests, list):
                            for tc in all_tests:
                                if isinstance(tc, dict) and 'input' in tc:
                                    input_val = tc.get('input', '')
                                    # Skip file paths, only include actual test data
                                    if input_val and not input_val.startswith('/mnt/data') and not input_val.startswith('/'):
                                        test_cases_list.append({
                                            'id': tc.get('id', f"test_{len(test_cases_list) + 1}"),
                                            'input': input_val,
                                            'expected_output': tc.get('output', tc.get('expected_output', ''))
                                        })
                        elif isinstance(all_tests, dict):
                            for key, value in all_tests.items():
                                if isinstance(value, dict) and 'input' in value:
                                    input_val = value.get('input', '')
                                    # Skip file paths, only include actual test data
                                    if input_val and not input_val.startswith('/mnt/data') and not input_val.startswith('/'):
                                        test_cases_list.append({
                                            'id': key,
                                            'input': input_val,
                                            'expected_output': value.get('output', value.get('expected_output', ''))
                                        })
                        
                        # Convert sample test cases
                        sample_test_cases_list = []
                        if isinstance(sample_tests, list):
                            for tc in sample_tests:
                                if isinstance(tc, dict) and 'input' in tc:
                                    input_val = tc.get('input', '')
                                    # Skip file paths, only include actual test data
                                    if input_val and not input_val.startswith('/mnt/data') and not input_val.startswith('/'):
                                        sample_test_cases_list.append({
                                            'id': tc.get('id', f"sample_{len(sample_test_cases_list) + 1}"),
                                            'input': input_val,
                                            'expected_output': tc.get('output', tc.get('expected_output', ''))
                                        })
                        elif isinstance(sample_tests, dict):
                            for key, value in sample_tests.items():
                                if isinstance(value, dict) and 'input' in value:
                                    input_val = value.get('input', '')
                                    # Skip file paths, only include actual test data
                                    if input_val and not input_val.startswith('/mnt/data') and not input_val.startswith('/'):
                                        sample_test_cases_list.append({
                                            'id': key,
                                            'input': input_val,
                                            'expected_output': value.get('output', value.get('expected_output', ''))
                                        })
                        
                        # Extract title and description from question_data
                        title = 'Untitled'
                        description = ''
                        if isinstance(question_data, dict):
                            title = question_data.get('title', question_data.get('name', 'Untitled'))
                            description = question_data.get('description', question_data.get('question', ''))
                        elif isinstance(question_data, str):
                            # Parse markdown/text to extract title
                            lines = question_data.strip().split('\n')
                            
                            # Look for markdown headers (# Title or ## Title)
                            for line in lines[:15]:  # Check first 15 lines
                                line_stripped = line.strip()
                                if line_stripped.startswith('# '):
                                    title = line_stripped[2:].strip()
                                    # Remove markdown formatting like **bold**
                                    title = title.replace('**', '').replace('*', '').strip()
                                    if title:
                                        break
                                elif line_stripped.startswith('## ') and title == 'Untitled':
                                    title = line_stripped[3:].strip()
                                    title = title.replace('**', '').replace('*', '').strip()
                                    if title:
                                        break
                            
                            # If no header found, look for patterns like "**Title**" or bold text
                            if title == 'Untitled':
                                for line in lines[:10]:
                                    line_stripped = line.strip()
                                    # Look for **Title** pattern
                                    if '**' in line_stripped and line_stripped.count('**') >= 2:
                                        import re
                                        match = re.search(r'\*\*([^*]+)\*\*', line_stripped)
                                        if match:
                                            title = match.group(1).strip()
                                            if len(title) <= 100:
                                                break
                            
                            # If still no title, try first meaningful line (not empty, not too long)
                            if title == 'Untitled':
                                for line in lines[:20]:
                                    line_stripped = line.strip()
                                    # Skip empty lines, markdown headers, and very long lines
                                    if (line_stripped and 
                                        not line_stripped.startswith('#') and 
                                        not line_stripped.startswith('**Category') and
                                        not line_stripped.startswith('**Difficulty') and
                                        len(line_stripped) <= 100 and
                                        len(line_stripped) > 5):
                                        title = line_stripped.replace('**', '').replace('*', '').strip()
                                        if title:
                                            break
                            
                            # Last resort: use first 60 chars of first non-empty line
                            if title == 'Untitled' or len(title) > 100:
                                for line in lines:
                                    line_stripped = line.strip()
                                    if line_stripped and len(line_stripped) > 5:
                                        first_chars = line_stripped[:60]
                                        title = first_chars + '...' if len(line_stripped) > 60 else first_chars
                                        title = title.replace('**', '').replace('*', '').strip()
                                        # Remove HTML tags
                                        import re
                                        title = re.sub(r'<[^>]+>', '', title).strip()
                                        break
                            
                            # If still no good title, use a generic one based on content
                            if title == 'Untitled' or len(title) < 3 or title.startswith('<'):
                                # Try to extract from description patterns
                                desc_lower = question_data.lower()
                                if 'longest substring' in desc_lower:
                                    title = 'Longest Substring Without Repeating Characters'
                                elif 'find first' in desc_lower or 'first and last' in desc_lower:
                                    title = 'Find First and Last Position'
                                elif 'two sum' in desc_lower:
                                    title = 'Two Sum'
                                elif 'warehouse' in desc_lower or 'boxes' in desc_lower or 'findtotalweight' in desc_lower:
                                    title = 'Warehouse Box Removal'
                                elif 'turnstile' in desc_lower:
                                    title = 'Turnstile Problem'
                                else:
                                    # Use first 50 chars of description, strip HTML
                                    import re
                                    first_chars = question_data.strip().replace('\n', ' ')
                                    first_chars = re.sub(r'<[^>]+>', '', first_chars)
                                    title = first_chars[:50] + '...' if len(first_chars) > 50 else first_chars
                            
                            # Clean up title - remove HTML tags if any
                            import re
                            title = re.sub(r'<[^>]+>', '', title).strip()
                            
                            description = question_data
                        
                        # Always add question, even if no test cases (they might be file-based)
                        questions.append({
                            'id': str(row['uuid']),
                            'title': title,
                            'description': description,
                            'difficulty': row['difficulty'] or 'medium',
                            'tags': tags,
                            'test_cases': test_cases_list,
                            'sample_test_cases': sample_test_cases_list,
                            'boilerplate': boilerplate
                        })
                    except Exception as e:
                        import traceback
                        print(f"Error processing question {row['uuid']}: {e}")
                        print(traceback.format_exc())
                        continue
                
                await conn.close()
                return questions
            except Exception as e:
                print(f"Database error: {e}")
                return []
        
        try:
            questions = loop.run_until_complete(fetch_questions())
        except Exception as e:
            print(f"Error in handle_get_questions: {e}")
            import traceback
            traceback.print_exc()
            questions = []
        finally:
            loop.close()
        
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(questions).encode())
    
    def handle_get_question(self, question_id):
        """Get a specific question"""
        import asyncio
        
        async def fetch_question():
            try:
                conn = await asyncpg.connect(DB_URL)
                row = await conn.fetchrow("""
                    SELECT uuid, question, sample_test_cases, test_cases, boiler_plate, difficulty, tags
                    FROM coding_question_bank
                    WHERE uuid = $1
                """, question_id)
                
                if not row:
                    return None
                
                # Parse JSONB fields (same logic as handle_get_questions)
                import json as json_lib
                
                # Parse question (same logic as handle_get_questions)
                question_data = row['question']
                if isinstance(question_data, str):
                    try:
                        # Try to parse as JSON first
                        parsed = json_lib.loads(question_data)
                        # If it's a dict/object, use it
                        if isinstance(parsed, dict):
                            question_data = parsed
                        else:
                            # If parsed but not a dict, keep as string
                            question_data = question_data
                    except:
                        # Not JSON, keep as string - we'll extract title from it
                        question_data = question_data
                
                # Parse sample_test_cases
                sample_tests = row['sample_test_cases']
                if isinstance(sample_tests, str):
                    try:
                        sample_tests = json_lib.loads(sample_tests) if sample_tests else []
                    except:
                        sample_tests = []
                sample_tests = sample_tests if sample_tests else []
                
                # Parse test_cases
                all_tests = row['test_cases']
                if isinstance(all_tests, str):
                    try:
                        all_tests = json_lib.loads(all_tests) if all_tests else []
                    except:
                        all_tests = []
                all_tests = all_tests if all_tests else []
                
                # Parse boiler_plate
                boilerplate = row['boiler_plate']
                if isinstance(boilerplate, str):
                    try:
                        boilerplate = json_lib.loads(boilerplate) if boilerplate else {}
                    except:
                        boilerplate = {}
                boilerplate = boilerplate if boilerplate else {}
                
                # Parse tags
                tags = row['tags']
                if isinstance(tags, str):
                    try:
                        tags = json_lib.loads(tags) if tags else []
                    except:
                        tags = []
                tags = tags if isinstance(tags, list) else []
                
                # Convert test cases to proper format (filter file paths)
                test_cases_list = []
                if isinstance(all_tests, list):
                    for tc in all_tests:
                        if isinstance(tc, dict) and 'input' in tc:
                            input_val = tc.get('input', '')
                            if input_val and not input_val.startswith('/mnt/data') and not input_val.startswith('/'):
                                test_cases_list.append({
                                    'id': tc.get('id', f"test_{len(test_cases_list) + 1}"),
                                    'input': input_val,
                                    'expected_output': tc.get('output', tc.get('expected_output', ''))
                                })
                elif isinstance(all_tests, dict):
                    for key, value in all_tests.items():
                        if isinstance(value, dict) and 'input' in value:
                            input_val = value.get('input', '')
                            if input_val and not input_val.startswith('/mnt/data') and not input_val.startswith('/'):
                                test_cases_list.append({
                                    'id': key,
                                    'input': input_val,
                                    'expected_output': value.get('output', value.get('expected_output', ''))
                                })
                
                # Convert sample test cases (filter file paths)
                sample_test_cases_list = []
                if isinstance(sample_tests, list):
                    for tc in sample_tests:
                        if isinstance(tc, dict) and 'input' in tc:
                            input_val = tc.get('input', '')
                            if input_val and not input_val.startswith('/mnt/data') and not input_val.startswith('/'):
                                sample_test_cases_list.append({
                                    'id': tc.get('id', f"sample_{len(sample_test_cases_list) + 1}"),
                                    'input': input_val,
                                    'expected_output': tc.get('output', tc.get('expected_output', ''))
                                })
                elif isinstance(sample_tests, dict):
                    for key, value in sample_tests.items():
                        if isinstance(value, dict) and 'input' in value:
                            input_val = value.get('input', '')
                            if input_val and not input_val.startswith('/mnt/data') and not input_val.startswith('/'):
                                sample_test_cases_list.append({
                                    'id': key,
                                    'input': input_val,
                                    'expected_output': value.get('output', value.get('expected_output', ''))
                                })
                
                # Extract title and description (same logic as handle_get_questions)
                title = 'Untitled'
                description = ''
                if isinstance(question_data, dict):
                    title = question_data.get('title', question_data.get('name', 'Untitled'))
                    description = question_data.get('description', question_data.get('question', ''))
                elif isinstance(question_data, str):
                    # Parse markdown/text to extract title (same logic as handle_get_questions)
                    lines = question_data.strip().split('\n')
                    
                    # Look for markdown headers (# Title or ## Title)
                    for line in lines[:15]:
                        line_stripped = line.strip()
                        if line_stripped.startswith('# '):
                            title = line_stripped[2:].strip()
                            title = title.replace('**', '').replace('*', '').strip()
                            if title:
                                break
                        elif line_stripped.startswith('## ') and title == 'Untitled':
                            title = line_stripped[3:].strip()
                            title = title.replace('**', '').replace('*', '').strip()
                            if title:
                                break
                    
                    # Look for **Title** pattern
                    if title == 'Untitled':
                        for line in lines[:10]:
                            line_stripped = line.strip()
                            if '**' in line_stripped and line_stripped.count('**') >= 2:
                                import re
                                match = re.search(r'\*\*([^*]+)\*\*', line_stripped)
                                if match:
                                    title = match.group(1).strip()
                                    if len(title) <= 100:
                                        break
                    
                    # Try first meaningful line
                    if title == 'Untitled':
                        for line in lines[:20]:
                            line_stripped = line.strip()
                            if (line_stripped and 
                                not line_stripped.startswith('#') and 
                                not line_stripped.startswith('**Category') and
                                not line_stripped.startswith('**Difficulty') and
                                len(line_stripped) <= 100 and
                                len(line_stripped) > 5):
                                title = line_stripped.replace('**', '').replace('*', '').strip()
                                if title:
                                    break
                    
                    # Last resort
                    if title == 'Untitled' or len(title) < 3 or title.startswith('<'):
                        desc_lower = question_data.lower()
                        if 'longest substring' in desc_lower:
                            title = 'Longest Substring Without Repeating Characters'
                        elif 'find first' in desc_lower or 'first and last' in desc_lower:
                            title = 'Find First and Last Position'
                        elif 'two sum' in desc_lower:
                            title = 'Two Sum'
                        elif 'warehouse' in desc_lower or 'boxes' in desc_lower or 'findtotalweight' in desc_lower:
                            title = 'Warehouse Box Removal'
                        elif 'turnstile' in desc_lower:
                            title = 'Turnstile Problem'
                        else:
                            import re
                            first_chars = question_data.strip().replace('\n', ' ')
                            first_chars = re.sub(r'<[^>]+>', '', first_chars)
                            title = first_chars[:50] + '...' if len(first_chars) > 50 else first_chars
                    
                    # Clean up title - remove HTML tags if any
                    import re
                    title = re.sub(r'<[^>]+>', '', title).strip()
                    
                    description = question_data
                
                await conn.close()
                
                return {
                    'id': str(row['uuid']),
                    'title': title,
                    'description': description,
                    'difficulty': row['difficulty'] or 'medium',
                    'tags': tags,
                    'test_cases': test_cases_list,
                    'sample_test_cases': sample_test_cases_list,
                    'boilerplate': boilerplate
                }
            except Exception as e:
                print(f"Database error: {e}")
                return None
        
        question = asyncio.run(fetch_question())
        
        if question:
            self.send_response(200)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(question).encode())
        else:
            self.send_response(404)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Question not found'}).encode())
    
    def log_message(self, format, *args):
        """Override to customize logging"""
        print(f"[{self.address_string()}] {format % args}")

def main():
    PORT = int(os.getenv('QUESTIONS_API_PORT', 3002))
    
    server = HTTPServer(("", PORT), QuestionsAPIHandler)
    print(f"🚀 Questions API server running at http://localhost:{PORT}")
    print(f"📝 Endpoints:")
    print(f"   - GET /api/questions - Get all questions")
    print(f"   - GET /api/questions/<id> - Get specific question")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")

if __name__ == "__main__":
    main()

