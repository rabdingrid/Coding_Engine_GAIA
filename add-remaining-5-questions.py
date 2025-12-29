#!/usr/bin/env python3
"""
Add remaining 5 questions properly with boilerplates and test cases
"""

import json
import os
import asyncpg
import asyncio
import uuid
from pathlib import Path
import re

DB_URL = os.getenv('DATABASE_URL', 'postgresql://postgresadmin:5oXcNX59QmEl7zmV3DbjemkiJ@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require')

# Question mappings with test case paths
QUESTIONS_CONFIG = {
    "Binary Manipulation": {
        "dir": "Binary Manipulation ",
        "test_path": "/Users/rabdin/Downloads/527749",
        "function_name": "minOperations",
        "params": [{"name": "n", "type": "long"}],
        "return_type": "int"
    },
    "Cartridge Recycling": {
        "dir": "Cartridge Recycling   ",
        "test_path": "/Users/rabdin/Downloads/725750",
        "function_name": "maxPerksItems",
        "params": [
            {"name": "cartridges", "type": "int"},
            {"name": "dollars", "type": "int"},
            {"name": "recycleReward", "type": "int"},
            {"name": "perksCost", "type": "int"}
        ],
        "return_type": "int"
    },
    "Modulo Challenge": {
        "dir": "Modulo Challenge",
        "test_path": "/Users/rabdin/Downloads/1177849",
        "function_name": "getMinLength",
        "params": [{"name": "arr", "type": "int[]"}],
        "return_type": "int"
    },
    "API Rate-Limiting": {
        "dir": "API Rate-Limiting   50 points  20 minute(s) Easy  Priority Queues  Data Structures  Interviewer Guidelines ",
        "test_path": "/Users/rabdin/Downloads/2079956",
        "function_name": "calculateSchedulingTime",
        "params": [
            {"name": "capacity", "type": "int[]"},
            {"name": "requests", "type": "long"}
        ],
        "return_type": "int"
    },
    "Maximal Permutation": {
        "dir": "Maximal Permutation ",
        "test_path": "/Users/rabdin/Downloads/325544",
        "function_name": "maximalPermutation",
        "params": [
            {"name": "container", "type": "int[]"},
            {"name": "firstPositions", "type": "int[]"},
            {"name": "secondPositions", "type": "int[]"},
            {"name": "slides", "type": "int[]"}
        ],
        "return_type": "int[]"
    }
}

def read_test_cases(test_dir):
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
        
        if i < 3:
            sample_test_cases.append(test_case)
        else:
            test_cases.append(test_case)
    
    return sample_test_cases, test_cases

def extract_metadata(question_text):
    """Extract title, difficulty, and tags"""
    lines = [l.strip() for l in question_text.split('\n') if l.strip()]
    title = lines[0] if lines else "Untitled"
    
    difficulty = "medium"
    text_lower = question_text.lower()
    if 'easy' in text_lower and 'medium' not in text_lower[:300]:
        difficulty = "easy"
    elif 'hard' in text_lower:
        difficulty = "hard"
    
    tags = []
    for i in range(min(5, len(lines))):
        if i == 0 or 'point' in lines[i].lower() or 'minute' in lines[i].lower():
            continue
        potential_tags = re.split(r'[,\s]+', lines[i])
        for tag in potential_tags:
            tag_clean = tag.strip()
            if tag_clean and len(tag_clean) > 2:
                skip = ['points', 'minute(s)', 'theme:', 'interviewer', 'guidelines', 'easy', 'medium', 'hard']
                if tag_clean.lower() not in skip and not tag_clean.isdigit():
                    tags.append(tag_clean)
        if tags:
            break
    
    if not tags:
        tags = ["algorithms", "problem solving"]
    
    return title, difficulty, tags[:5]

def format_question_html(question_text):
    """Format question as HTML"""
    lines = [l.strip() for l in question_text.split('\n') if l.strip()]
    html = "<h3>Problem</h3>\n<p>"
    
    # Skip first 4 lines (title, points, time, tags)
    content = lines[4:] if len(lines) > 4 else lines
    
    current_para = []
    for line in content:
        if not line:
            if current_para:
                html += " ".join(current_para) + "</p>\n<p>"
                current_para = []
        elif any(line.startswith(x) for x in ["Example", "Function Description", "Constraints", "Input Format"]):
            if current_para:
                html += " ".join(current_para) + "</p>"
                current_para = []
            html += f"\n<h3>{line}</h3>\n<p>"
        else:
            current_para.append(line)
    
    if current_para:
        html += " ".join(current_para) + "</p>"
    
    return html

# Import boilerplate generators from previous script
def generate_boilerplates(q_config):
    """Generate boilerplates - simplified version"""
    fn = q_config["function_name"]
    params = q_config["params"]
    ret_type = q_config["return_type"]
    
    # Python
    params_py = ", ".join([p["name"] for p in params])
    python_input = generate_python_input(params, ret_type, fn)
    python_bp = f"def {fn}({params_py}):\n    # Write your code here\n\n{python_input}"
    
    # C++
    params_cpp = ", ".join([f"{'long long' if p['type'] == 'long' else 'int'} {p['name']}" + ("[]" if "[]" in p['type'] else "") for p in params])
    ret_cpp = "vector<int>" if "[]" in ret_type else ("long long" if "long" in ret_type.lower() else "int")
    cpp_bp = generate_cpp_boilerplate(fn, params_cpp, ret_cpp, params, ret_type)
    
    # Java
    params_java = ", ".join([f"{'List<Integer>' if '[]' in p['type'] else ('long' if p['type'] == 'long' else 'int')} {p['name']}" for p in params])
    ret_java = "List<Integer>" if "[]" in ret_type else ("long" if "long" in ret_type.lower() else "int")
    java_bp = generate_java_boilerplate(fn, params_java, ret_java, params, ret_type)
    
    # JavaScript
    params_js = ", ".join([p["name"] for p in params])
    js_bp = generate_javascript_boilerplate(fn, params_js, params, ret_type)
    
    # C#
    params_cs = ", ".join([f"{'List<int>' if '[]' in p['type'] else 'int'} {p['name']}" for p in params])
    ret_cs = "List<int>" if "[]" in ret_type else "int"
    cs_bp = generate_csharp_boilerplate(fn, params_cs, ret_cs, params, ret_type)
    
    return {
        "python": python_bp,
        "cpp": cpp_bp,
        "java": java_bp,
        "javascript": js_bp,
        "csharp": cs_bp
    }

def generate_python_input(params, ret_type, fn):
    """Generate Python input reading code"""
    code = []
    for p in params:
        if "[]" in p['type']:
            code.append(f"{p['name']}_count = int(input().strip())")
            code.append(f"{p['name']} = []")
            code.append(f"for _ in range({p['name']}_count):")
            code.append(f"    {p['name']}_item = int(input().strip())")
            code.append(f"    {p['name']}.append({p['name']}_item)")
        elif "long" in p['type'].lower():
            code.append(f"{p['name']} = int(input().strip())")
        else:
            code.append(f"{p['name']} = int(input().strip())")
    
    params_str = ", ".join([p['name'] for p in params])
    if "[]" in ret_type:
        code.append(f"result = {fn}({params_str})")
        code.append("print('\\n'.join(map(str, result)))")
    else:
        code.append(f"result = {fn}({params_str})")
        code.append("print(result)")
    
    return "\n".join(code)

def generate_cpp_boilerplate(fn, params_cpp, ret_cpp, params, ret_type):
    """Generate C++ boilerplate"""
    input_code = []
    for p in params:
        if "[]" in p['type']:
            input_code.append(f"string {p['name']}_count_temp;")
            input_code.append(f"getline(cin, {p['name']}_count_temp);")
            input_code.append(f"int {p['name']}_count = stoi(ltrim(rtrim({p['name']}_count_temp)));")
            input_code.append(f"vector<int> {p['name']}({p['name']}_count);")
            input_code.append(f"for (int i = 0; i < {p['name']}_count; i++) {{")
            input_code.append(f"    string {p['name']}_item_temp;")
            input_code.append(f"    getline(cin, {p['name']}_item_temp);")
            input_code.append(f"    int {p['name']}_item = stoi(ltrim(rtrim({p['name']}_item_temp)));")
            input_code.append(f"    {p['name']}[i] = {p['name']}_item;")
            input_code.append("}")
        else:
            input_code.append(f"string {p['name']}_temp;")
            input_code.append(f"getline(cin, {p['name']}_temp);")
            type_str = "long long" if "long" in p['type'].lower() else "int"
            input_code.append(f"{type_str} {p['name']} = stoi(ltrim(rtrim({p['name']}_temp)));")
    
    call_params = ", ".join([p['name'] for p in params])
    output_code = []
    if "[]" in ret_type:
        output_code.append(f"vector<int> result = {fn}({call_params});")
        output_code.append("for (size_t i = 0; i < result.size(); i++) {")
        output_code.append("    cout << result[i];")
        output_code.append("    if (i != result.size() - 1) {")
        output_code.append("        cout << \"\\n\";")
        output_code.append("    }")
        output_code.append("}")
        output_code.append("cout << \"\\n\";")
    else:
        output_code.append(f"{ret_cpp} result = {fn}({call_params});")
        output_code.append("cout << result << \"\\n\";")
    
    return f"""#include <bits/stdc++.h>
using namespace std;

string ltrim(const string &);
string rtrim(const string &);

{ret_cpp} {fn}({params_cpp}) {{
}}

int main()
{{
    {"    ".join(input_code)}
    {"    ".join(output_code)}
    return 0;
}}

string ltrim(const string &str) {{
    string s(str);
    s.erase(
        s.begin(),
        find_if(s.begin(), s.end(), not1(ptr_fun<int, int>(isspace)))
    );
    return s;
}}

string rtrim(const string &str) {{
    string s(str);
    s.erase(
        find_if(s.rbegin(), s.rend(), not1(ptr_fun<int, int>(isspace))).base(),
        s.end()
    );
    return s;
}}"""

def generate_java_boilerplate(fn, params_java, ret_java, params, ret_type):
    """Generate Java boilerplate"""
    input_code = []
    for p in params:
        if "[]" in p['type']:
            input_code.append(f"int {p['name']}Count = Integer.parseInt(bufferedReader.readLine().trim());")
            input_code.append(f"List<Integer> {p['name']} = new ArrayList<>();")
            input_code.append(f"for (int i = 0; i < {p['name']}Count; i++) {{")
            input_code.append(f"    int {p['name']}Item = Integer.parseInt(bufferedReader.readLine().trim());")
            input_code.append(f"    {p['name']}.add({p['name']}Item);")
            input_code.append("}")
        else:
            type_str = "long" if "long" in p['type'].lower() else "int"
            if type_str == "long":
                input_code.append(f"long {p['name']} = Long.parseLong(bufferedReader.readLine().trim());")
            else:
                input_code.append(f"int {p['name']} = Integer.parseInt(bufferedReader.readLine().trim());")
    
    call_params = ", ".join([p['name'] for p in params])
    output_code = []
    if "[]" in ret_type:
        output_code.append(f"{ret_java} result = Result.{fn}({call_params});")
        output_code.append("System.out.println(")
        output_code.append("    result.stream()")
        output_code.append("        .map(Object::toString)")
        output_code.append("        .collect(java.util.stream.Collectors.joining(\"\\n\"))")
        output_code.append(");")
    else:
        output_code.append(f"{ret_java} result = Result.{fn}({call_params});")
        output_code.append("System.out.println(result);")
    
    return f"""import java.io.*;
import java.util.*;

class Result {{
    public static {ret_java} {fn}({params_java}) {{
    // Write your code here
    }}
}}

class Main {{
    public static void main(String[] args) throws IOException {{
        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(System.in));
        {"        ".join(input_code)}
        {"        ".join(output_code)}
        bufferedReader.close();
    }}
}}"""

def generate_javascript_boilerplate(fn, params_js, params, ret_type):
    """Generate JavaScript boilerplate"""
    input_code = []
    for i, p in enumerate(params):
        if "[]" in p['type']:
            if i == 0:
                input_code.append(f"const {p['name']}Count = parseInt(lines[0].trim(), 10);")
                input_code.append(f"let {p['name']} = [];")
                input_code.append(f"for (let i = 1; i < 1 + {p['name']}Count; i++) {{")
                input_code.append(f"    {p['name']}.push(parseInt(lines[i].trim(), 10));")
                input_code.append("}")
                input_code.append(f"let idx = 1 + {p['name']}Count;")
            else:
                input_code.append(f"const {p['name']}Count = parseInt(lines[idx].trim(), 10);")
                input_code.append(f"let {p['name']} = [];")
                input_code.append(f"for (let i = idx + 1; i < idx + 1 + {p['name']}Count; i++) {{")
                input_code.append(f"    {p['name']}.push(parseInt(lines[i].trim(), 10));")
                input_code.append("}")
                input_code.append(f"idx = idx + 1 + {p['name']}Count;")
        else:
            if i == 0:
                input_code.append(f"const {p['name']} = parseInt(lines[0].trim(), 10);")
                input_code.append("let idx = 1;")
            else:
                input_code.append(f"const {p['name']} = parseInt(lines[idx].trim(), 10);")
                input_code.append("idx++;")
    
    call_params = ", ".join([p['name'] for p in params])
    if "[]" in ret_type:
        output_code = f"    const result = {fn}({call_params});\n    console.log(result.join('\\n'));"
    else:
        output_code = f"    const result = {fn}({call_params});\n    console.log(result);"
    
    return f"""function {fn}({params_js}) {{
    // Write your code here
}}

const readline = require('readline');
const rl = readline.createInterface({{
    input: process.stdin,
    output: process.stdout,
    terminal: false
}});

const lines = [];
rl.on('line', (line) => {{
    lines.push(line);
}});

rl.on('close', () => {{
    {"    ".join(input_code)}
    {output_code}
}});"""

def generate_csharp_boilerplate(fn, params_cs, ret_cs, params, ret_type):
    """Generate C# boilerplate"""
    input_code = []
    for p in params:
        if "[]" in p['type']:
            input_code.append(f"int {p['name']}Count = Convert.ToInt32(Console.ReadLine().Trim());")
            input_code.append(f"List<int> {p['name']} = new List<int>();")
            input_code.append(f"for (int i = 0; i < {p['name']}Count; i++) {{")
            input_code.append(f"    int {p['name']}Item = Convert.ToInt32(Console.ReadLine().Trim());")
            input_code.append(f"    {p['name']}.Add({p['name']}Item);")
            input_code.append("}")
        else:
            input_code.append(f"int {p['name']} = Convert.ToInt32(Console.ReadLine().Trim());")
    
    call_params = ", ".join([p['name'] for p in params])
    if "[]" in ret_type:
        output_code = f"List<int> result = Result.{fn}({call_params});\n        Console.WriteLine(String.Join(\"\\n\", result));"
    else:
        output_code = f"int result = Result.{fn}({call_params});\n        Console.WriteLine(result);"
    
    return f"""using System;
using System.Collections.Generic;
using System.Linq;

class Result {{
    public static {ret_cs} {fn}({params_cs})
    {{
    }}
}}

class Solution {{
    public static void Main(string[] args)
    {{
        {"        ".join(input_code)}
        {output_code}
    }}
}}"""

async def add_all_questions():
    """Add all 5 remaining questions"""
    conn = await asyncpg.connect(DB_URL)
    
    try:
        for title, q_config in QUESTIONS_CONFIG.items():
            print(f"\n📝 Processing: {title}")
            
            # Read question file
            q_dir = Path(f"coding questions/{q_config['dir']}")
            question_file = q_dir / "question"
            
            if not question_file.exists():
                print(f"   ⚠️  Question file not found")
                continue
            
            question_text = question_file.read_text()
            extracted_title, difficulty, tags = extract_metadata(question_text)
            
            # Use config title if extraction failed
            if not extracted_title or extracted_title == "Untitled":
                extracted_title = title
            
            # Read test cases
            test_dir_path = Path(q_config['test_path'])
            sample_test_cases, test_cases = read_test_cases(test_dir_path)
            
            print(f"   📊 Test cases: {len(sample_test_cases)} sample, {len(test_cases)} regular")
            
            # Generate boilerplates
            boilerplates = generate_boilerplates(q_config)
            
            # Format question HTML
            question_html = format_question_html(question_text)
            
            # Create UUID
            question_uuid = str(uuid.uuid4())
            
            # Insert question
            await conn.execute("""
                INSERT INTO coding_question_bank (
                    uuid, question, difficulty, tags,
                    boiler_plate, sample_test_cases, test_cases
                ) VALUES ($1, $2, $3, $4, $5, $6, $7)
            """,
                question_uuid,
                question_html,
                difficulty,
                json.dumps([tag.lower() for tag in tags]),
                json.dumps(boilerplates),
                json.dumps(sample_test_cases),
                json.dumps(test_cases)
            )
            
            print(f"   ✅ Added: {extracted_title}")
            print(f"      UUID: {question_uuid}")
            print(f"      Difficulty: {difficulty}, Tags: {tags[:3]}")
            print(f"      Boilerplates: {len(boilerplates)} languages")
    
    finally:
        await conn.close()

if __name__ == "__main__":
    print("🚀 Adding Remaining 5 Questions")
    print("=" * 60)
    asyncio.run(add_all_questions())
    print("\n✅ All questions added!")




