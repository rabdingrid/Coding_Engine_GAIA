#!/bin/bash

# Export all coding_question_bank questions to a formatted markdown file

set -e

export PATH="/opt/homebrew/opt/postgresql@17/bin:$PATH"
AZURE_DB=$(cat .postgres-connection.txt)

if [ -z "$AZURE_DB" ]; then
    echo "❌ Error: Azure database connection string not found"
    exit 1
fi

OUTPUT_FILE="coding_question_bank_export.md"
JSON_FILE="coding_questions_temp.json"

echo "📊 Exporting all questions from coding_question_bank..."
echo ""

# Get total count
TOTAL=$(psql "$AZURE_DB" -t -c "SELECT COUNT(*) FROM coding_question_bank;" | xargs)
echo "   Found $TOTAL questions"

echo ""
echo "📥 Step 1: Exporting to JSON..."

# Export to JSON
psql "$AZURE_DB" -t -A -c "
SELECT json_agg(
    json_build_object(
        'uuid', uuid,
        'question', question,
        'difficulty', difficulty,
        'tags', tags,
        'sample_test_cases', sample_test_cases,
        'test_cases', test_cases,
        'boiler_plate', boiler_plate
    )
)
FROM (
    SELECT uuid, question, difficulty, tags, sample_test_cases, test_cases, boiler_plate
    FROM coding_question_bank
    ORDER BY uuid
) t;
" > "$JSON_FILE" 2>&1

if [ ! -s "$JSON_FILE" ]; then
    echo "❌ Failed to export JSON"
    exit 1
fi

echo "   ✅ JSON exported"
echo ""
echo "📝 Step 2: Converting to formatted Markdown..."

# Create markdown file header
cat > "$OUTPUT_FILE" << EOF
# Coding Question Bank - Complete List

This file contains all questions from the \`coding_question_bank\` table.

**Generated:** $(date '+%Y-%m-%d %H:%M:%S')
**Total Questions:** $TOTAL

---

EOF

# Use Node.js to parse JSON and format (if available) or use a simpler approach
if command -v node &> /dev/null; then
    node << 'NODEEOF'
const fs = require('fs');
const jsonData = fs.readFileSync('coding_questions_temp.json', 'utf8');
const questions = JSON.parse(jsonData);

let output = '';
questions.forEach((q, idx) => {
    const num = idx + 1;
    const uuid = q.uuid || 'N/A';
    const difficulty = q.difficulty || 'N/A';
    const tags = q.tags ? (Array.isArray(q.tags) ? q.tags.join(', ') : q.tags) : 'N/A';
    const question = q.question || '';
    const boiler = q.boiler_plate || '';
    const sampleTc = q.sample_test_cases || [];
    const testTc = q.test_cases || [];
    
    const sampleCount = Array.isArray(sampleTc) ? sampleTc.length : 0;
    const testCount = Array.isArray(testTc) ? testTc.length : 0;
    
    output += `\n## Question #${num}\n\n`;
    output += `**UUID:** \`${uuid}\`  \n`;
    output += `**Difficulty:** ${difficulty}  \n`;
    output += `**Tags:** ${tags}  \n`;
    output += `**Sample Test Cases:** ${sampleCount}  \n`;
    output += `**Test Cases:** ${testCount}  \n\n`;
    output += `### Question Description\n\n`;
    output += `${question}\n\n`;
    
    if (boiler) {
        output += `### Boilerplate Code\n\n`;
        output += '```\n';
        output += `${boiler}\n`;
        output += '```\n\n';
    }
    
    if (sampleTc && sampleTc.length > 0) {
        output += `### Sample Test Cases\n\n`;
        output += '```json\n';
        output += `${JSON.stringify(sampleTc, null, 2)}\n`;
        output += '```\n\n';
    }
    
    if (testTc && testTc.length > 0) {
        output += `### Test Cases\n\n`;
        output += '```json\n';
        output += `${JSON.stringify(testTc, null, 2)}\n`;
        output += '```\n\n';
    }
    
    output += '---\n';
    
    if ((idx + 1) % 10 === 0) {
        console.log(`  ✅ Processed ${idx + 1}/${questions.length} questions...`);
    }
});

// Append to existing file
const existing = fs.readFileSync('coding_question_bank_export.md', 'utf8');
fs.writeFileSync('coding_question_bank_export.md', existing + output);

console.log(`  ✅ Exported ${questions.length} questions`);
NODEEOF
else
    # Fallback: Use Python if available
    if command -v python3 &> /dev/null; then
        python3 << 'PYTHONEOF'
import json
import sys

try:
    with open('coding_questions_temp.json', 'r', encoding='utf-8') as f:
        json_str = f.read().strip()
        questions = json.loads(json_str)
    
    output = ''
    for idx, q in enumerate(questions, 1):
        uuid = q.get('uuid', 'N/A')
        difficulty = q.get('difficulty', 'N/A')
        tags = q.get('tags', [])
        if isinstance(tags, list):
            tags_str = ', '.join(tags) if tags else 'N/A'
        else:
            tags_str = str(tags) if tags else 'N/A'
        
        question = q.get('question', '')
        boiler = q.get('boiler_plate', '')
        sample_tc = q.get('sample_test_cases', [])
        test_tc = q.get('test_cases', [])
        
        sample_count = len(sample_tc) if isinstance(sample_tc, list) else 0
        test_count = len(test_tc) if isinstance(test_tc, list) else 0
        
        output += f'\n## Question #{idx}\n\n'
        output += f'**UUID:** `{uuid}`  \n'
        output += f'**Difficulty:** {difficulty}  \n'
        output += f'**Tags:** {tags_str}  \n'
        output += f'**Sample Test Cases:** {sample_count}  \n'
        output += f'**Test Cases:** {test_count}  \n\n'
        output += f'### Question Description\n\n'
        output += f'{question}\n\n'
        
        if boiler:
            output += f'### Boilerplate Code\n\n'
            output += '```\n'
            output += f'{boiler}\n'
            output += '```\n\n'
        
        if sample_tc:
            output += f'### Sample Test Cases\n\n'
            output += '```json\n'
            output += f'{json.dumps(sample_tc, indent=2, ensure_ascii=False)}\n'
            output += '```\n\n'
        
        if test_tc:
            output += f'### Test Cases\n\n'
            output += '```json\n'
            output += f'{json.dumps(test_tc, indent=2, ensure_ascii=False)}\n'
            output += '```\n\n'
        
        output += '---\n'
        
        if idx % 10 == 0:
            print(f'  ✅ Processed {idx}/{len(questions)} questions...', file=sys.stderr)
    
    # Append to existing file
    with open('coding_question_bank_export.md', 'a', encoding='utf-8') as f:
        f.write(output)
    
    print(f'  ✅ Exported {len(questions)} questions')
except Exception as e:
    print(f'❌ Error: {e}', file=sys.stderr)
    sys.exit(1)
PYTHONEOF
    else
        echo "❌ Error: Neither Node.js nor Python3 found. Cannot format JSON."
        exit 1
    fi
fi

# Cleanup
rm -f "$JSON_FILE"

echo ""
echo "✅ Export complete!"
echo "   File: $OUTPUT_FILE"
echo "   Questions: $TOTAL"
echo ""
echo "📄 File size:"
ls -lh "$OUTPUT_FILE" | awk '{print "   " $5}'
