#!/bin/bash

# Get a question from database and create curl command for /runall

DB_URL="postgresql://postgresadmin:5oXcNX59QmEl7zmV3DbjemkiJ@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require"
EXECUTOR_URL="${EXECUTOR_URL:-http://localhost:8000}"

echo "📋 Fetching question from database..."
echo ""

# Get first question with test cases
QUESTION_DATA=$(psql "$DB_URL" -t -A -F"|SEPARATOR|" -c "
SELECT 
    uuid,
    question,
    test_cases::text,
    sample_test_cases::text,
    boiler_plate::text
FROM coding_question_bank 
WHERE jsonb_array_length(test_cases) > 0 
LIMIT 1;
" 2>&1)

if [ $? -ne 0 ]; then
    echo "❌ Database connection failed"
    echo "Trying alternative method..."
    # Use Python to fetch
    python3 << 'PYTHON_SCRIPT'
import json
import os
import subprocess

db_url = "postgresql://postgresadmin:5oXcNX59QmEl7zmV3DbjemkiJ@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require"

try:
    result = subprocess.run(
        ['psql', db_url, '-t', '-A', '-F', '|SEPARATOR|', '-c', 
         "SELECT uuid, question, test_cases::text, sample_test_cases::text, boiler_plate::text FROM coding_question_bank WHERE jsonb_array_length(test_cases) > 0 LIMIT 1;"],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    if result.returncode == 0 and result.stdout.strip():
        data = result.stdout.strip().split('|SEPARATOR|')
        if len(data) >= 5:
            uuid_val = data[0]
            question = data[1]
            test_cases = json.loads(data[2])
            sample_test_cases = json.loads(data[3]) if data[3] else []
            boiler_plate = json.loads(data[4]) if data[4] else {}
            
            print(f"✅ Found question: {uuid_val}")
            print(f"   Test cases: {len(test_cases)}")
            print(f"   Sample test cases: {len(sample_test_cases)}")
            print(f"   Languages: {list(boiler_plate.keys())}")
            
            # Save to temp file
            with open('/tmp/question_data.json', 'w') as f:
                json.dump({
                    'uuid': uuid_val,
                    'question': question,
                    'test_cases': test_cases,
                    'sample_test_cases': sample_test_cases,
                    'boiler_plate': boiler_plate
                }, f, indent=2)
        else:
            print("❌ Invalid data format")
    else:
        print("❌ No questions found or error:", result.stderr)
except Exception as e:
    print(f"❌ Error: {e}")
PYTHON_SCRIPT
fi

# If we have question data, create curl command
if [ -f /tmp/question_data.json ]; then
    echo ""
    echo "✅ Question loaded! Creating curl command..."
    python3 << 'PYTHON_SCRIPT'
import json
import sys
import os

executor_url = os.environ.get('EXECUTOR_URL', 'http://localhost:8000')

with open('/tmp/question_data.json', 'r') as f:
    data = json.load(f)

# Use Python boilerplate (or first available language)
language = 'python'
if 'python' in data['boiler_plate']:
    code = data['boiler_plate']['python']
elif data['boiler_plate']:
    language = list(data['boiler_plate'].keys())[0]
    code = data['boiler_plate'][language]
else:
    print("❌ No boilerplate found")
    sys.exit(1)

# Get all test cases (excluding sample)
all_test_cases = data['test_cases']
sample_ids = {tc.get('id') for tc in data.get('sample_test_cases', [])}
test_cases = [tc for tc in all_test_cases if tc.get('id') not in sample_ids]

if not test_cases:
    test_cases = all_test_cases  # Use all if no sample separation

print(f"\n🧪 Testing with {len(test_cases)} test cases")
print(f"   Language: {language}")
print(f"   Question UUID: {data['uuid']}")
print(f"\n📝 Code snippet:")
print("   " + code.split('\n')[0] + "...")

# Create test cases JSON
test_cases_json = json.dumps([{
    'id': tc.get('id', f'test_{i}'),
    'input': tc.get('input', ''),
    'expected_output': tc.get('expected_output', '')
} for i, tc in enumerate(test_cases, 1)])

# Escape code for JSON
code_escaped = json.dumps(code)

# Create curl command
curl_cmd = f'''curl -X POST {executor_url}/runall \\
  -H "Content-Type: application/json" \\
  -d '{{
    "language": "{language}",
    "code": {code_escaped},
    "test_cases": {test_cases_json},
    "sample_test_cases": [],
    "user_id": "test_user_db",
    "question_id": "{data['uuid']}",
    "timeout": 5
  }}' '''

print(f"\n📋 CURL COMMAND:")
print("=" * 70)
print(curl_cmd)
print("=" * 70)

# Also save to file
with open('/tmp/curl_command.sh', 'w') as f:
    f.write("#!/bin/bash\n")
    f.write(curl_cmd)
    f.write("\n")

print(f"\n✅ Command saved to: /tmp/curl_command.sh")
print(f"   Run: bash /tmp/curl_command.sh")
PYTHON_SCRIPT
else
    echo "❌ Could not load question data"
fi

