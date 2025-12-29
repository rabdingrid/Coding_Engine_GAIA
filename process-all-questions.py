#!/usr/bin/env python3
"""
Process all questions from coding questions directory
- Add solutions column to database
- Process each question with correct boilerplates
- Add correct code solutions for all languages
- Set difficulty and tags
- Remove old questions not in this format
"""

import json
import os
import asyncpg
import asyncio
import uuid
from pathlib import Path
import re

# Database connection
DB_URL = os.getenv('DATABASE_URL', 'postgresql://postgresadmin:5oXcNX59QmEl7zmV3DbjemkiJ@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require')

CODING_QUESTIONS_DIR = Path("coding questions")

# Template for correct boilerplates (same pattern as Endpoint Inspection)
def get_boilerplate_template(function_name, return_type, params, language):
    """Generate correct boilerplate for a language"""
    
    if language == "python":
        params_str = ", ".join([f"{p['name']}" for p in params])
        return f"""def {function_name}({params_str}):
    # Write your code here

{get_python_input_code(params, return_type)}"""
    
    elif language == "cpp":
        params_cpp = ", ".join([f"{p['type']} {p['name']}" for p in params])
        return_type_cpp = return_type.replace("List", "vector").replace("int", "int").replace("long", "long long")
        return f"""#include <bits/stdc++.h>
using namespace std;

string ltrim(const string &);
string rtrim(const string &);

{get_cpp_function_signature(function_name, return_type_cpp, params)}

int main()
{{
    {get_cpp_input_code(params, return_type)}
    vector<int> result = {function_name}({get_cpp_call_params(params)});
    for (size_t i = 0; i < result.size(); i++) {{
        cout << result[i];
        if (i != result.size() - 1) {{
            cout << "\\n";
        }}
    }}
    cout << "\\n";
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
    
    elif language == "java":
        params_java = ", ".join([f"{p['type']} {p['name']}" for p in params])
        return f"""import java.io.*;
import java.util.*;

class Result {{
    public static {return_type} {function_name}({params_java}) {{
    // Write your code here
    }}
}}

class Main {{
    public static void main(String[] args) throws IOException {{
        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(System.in));
        {get_java_input_code(params, return_type)}
        {return_type} result = Result.{function_name}({get_java_call_params(params)});
        System.out.println(
            result.stream()
                .map(Object::toString)
                .collect(java.util.stream.Collectors.joining("\\n"))
        );
        bufferedReader.close();
    }}
}}"""
    
    elif language == "javascript":
        params_js = ", ".join([p['name'] for p in params])
        return f"""function {function_name}({params_js}) {{
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
    {get_javascript_input_code(params, return_type)}
    const result = {function_name}({get_javascript_call_params(params)});
    console.log(result.join('\\n'));
}});"""
    
    elif language == "csharp":
        params_cs = ", ".join([f"{p['type']} {p['name']}" for p in params])
        return f"""using System;
using System.Collections.Generic;
using System.Linq;

class Result {{
    public static {return_type} {function_name}({params_cs})
    {{
    }}
}}

class Solution {{
    public static void Main(string[] args)
    {{
        {get_csharp_input_code(params, return_type)}
        {return_type} result = Result.{function_name}({get_csharp_call_params(params)});
        Console.WriteLine(String.Join("\\n", result));
    }}
}}"""
    
    return ""

def get_python_input_code(params, return_type):
    """Generate Python input reading code"""
    code = []
    for p in params:
        if "[]" in p['type'] or "List" in p['type']:
            code.append(f"{p['name']}_count = int(input().strip())")
            code.append(f"{p['name']} = []")
            code.append(f"for _ in range({p['name']}_count):")
            code.append(f"    {p['name']}_item = int(input().strip())")
            code.append(f"    {p['name']}.append({p['name']}_item)")
        elif "long" in p['type'].lower():
            code.append(f"{p['name']} = int(input().strip())")
        else:
            code.append(f"{p['name']} = int(input().strip())")
    
    if "[]" in return_type or "List" in return_type:
        code.append("result = " + params[0]['name'].split('_')[0] + f"({', '.join([p['name'] for p in params])})")
        code.append("print('\\n'.join(map(str, result)))")
    else:
        code.append("result = " + params[0]['name'].split('_')[0] + f"({', '.join([p['name'] for p in params])})")
        code.append("print(result)")
    
    return "\n".join(code)

def get_cpp_function_signature(function_name, return_type, params):
    """Generate C++ function signature"""
    params_cpp = ", ".join([f"{p['type']} {p['name']}" for p in params])
    return f"{return_type} {function_name}({params_cpp}) {{}}"

def get_cpp_input_code(params, return_type):
    """Generate C++ input reading code"""
    code = []
    for p in params:
        if "[]" in p['type'] or "vector" in p['type']:
            code.append(f"string {p['name']}_count_temp;")
            code.append(f"getline(cin, {p['name']}_count_temp);")
            code.append(f"int {p['name']}_count = stoi(ltrim(rtrim({p['name']}_count_temp)));")
            code.append(f"vector<int> {p['name']}({p['name']}_count);")
            code.append(f"for (int i = 0; i < {p['name']}_count; i++) {{")
            code.append(f"    string {p['name']}_item_temp;")
            code.append(f"    getline(cin, {p['name']}_item_temp);")
            code.append(f"    int {p['name']}_item = stoi(ltrim(rtrim({p['name']}_item_temp)));")
            code.append(f"    {p['name']}[i] = {p['name']}_item;")
            code.append("}")
        else:
            code.append(f"string {p['name']}_temp;")
            code.append(f"getline(cin, {p['name']}_temp);")
            code.append(f"int {p['name']} = stoi(ltrim(rtrim({p['name']}_temp)));")
    
    return "\n    ".join(code)

def get_cpp_call_params(params):
    """Generate C++ function call parameters"""
    return ", ".join([p['name'] for p in params])

def get_java_input_code(params, return_type):
    """Generate Java input reading code"""
    code = []
    for p in params:
        if "[]" in p['type'] or "List" in p['type']:
            code.append(f"int {p['name']}Count = Integer.parseInt(bufferedReader.readLine().trim());")
            code.append(f"List<Integer> {p['name']} = IntStream.range(0, {p['name']}Count).mapToObj(i -> {{")
            code.append("    try {")
            code.append("        return bufferedReader.readLine().replaceAll(\"\\\\s+$\", \"\");")
            code.append("    } catch (IOException ex) {")
            code.append("        throw new RuntimeException(ex);")
            code.append("    }")
            code.append("})")
            code.append("    .map(String::trim)")
            code.append("    .map(Integer::parseInt)")
            code.append("    .collect(java.util.stream.Collectors.toList());")
        else:
            code.append(f"int {p['name']} = Integer.parseInt(bufferedReader.readLine().trim());")
    
    return "\n        ".join(code)

def get_java_call_params(params):
    """Generate Java function call parameters"""
    return ", ".join([p['name'] for p in params])

def get_javascript_input_code(params, return_type):
    """Generate JavaScript input reading code"""
    code = []
    idx = 0
    for p in params:
        if "[]" in p['type'] or "Array" in p['type']:
            code.append(f"const {p['name']}Count = parseInt(lines[{idx}].trim(), 10);")
            code.append(f"let {p['name']} = [];")
            code.append(f"for (let i = {idx + 1}; i <= {idx} + {p['name']}Count; i++) {{")
            code.append(f"    {p['name']}.push(parseInt(lines[i].trim(), 10));")
            code.append("}")
            idx += p['name'] + "Count + 1"
        else:
            code.append(f"const {p['name']} = parseInt(lines[{idx}].trim(), 10);")
            idx += 1
    
    return "\n    ".join(code)

def get_javascript_call_params(params):
    """Generate JavaScript function call parameters"""
    return ", ".join([p['name'] for p in params])

def get_csharp_input_code(params, return_type):
    """Generate C# input reading code"""
    code = []
    for p in params:
        if "[]" in p['type'] or "List" in p['type']:
            code.append(f"int {p['name']}Count = Convert.ToInt32(Console.ReadLine().Trim());")
            code.append(f"List<int> {p['name']} = new List<int>();")
            code.append(f"for (int i = 0; i < {p['name']}Count; i++)")
            code.append("{")
            code.append(f"    int {p['name']}Item = Convert.ToInt32(Console.ReadLine().Trim());")
            code.append(f"    {p['name']}.Add({p['name']}Item);")
            code.append("}")
        else:
            code.append(f"int {p['name']} = Convert.ToInt32(Console.ReadLine().Trim());")
    
    return "\n        ".join(code)

def get_csharp_call_params(params):
    """Generate C# function call parameters"""
    return ", ".join([p['name'] for p in params])

# This is a simplified version - we'll need to parse each question individually
# For now, let me create a structure that can be extended

async def add_solutions_column():
    """Add solutions column to database"""
    conn = await asyncpg.connect(DB_URL)
    try:
        # Check if column exists
        columns = await conn.fetch("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'coding_question_bank' AND column_name = 'solutions'
        """)
        
        if not columns:
            await conn.execute("""
                ALTER TABLE coding_question_bank 
                ADD COLUMN solutions JSONB
            """)
            print("✅ Added 'solutions' column to database")
        else:
            print("✅ 'solutions' column already exists")
    finally:
        await conn.close()

if __name__ == "__main__":
    print("🚀 Processing all questions...")
    asyncio.run(add_solutions_column())
    print("✅ Database structure updated")
    print("\n📝 Next: Process individual questions...")
    print("   (This requires solving each problem - will need to be done per question)")




