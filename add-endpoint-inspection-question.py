#!/usr/bin/env python3
"""
Add "Endpoint Inspection" question to coding_question_bank table
Format matches existing question structure
"""

import json
import uuid
import os
import asyncpg
import asyncio
from pathlib import Path

# Database connection
DB_URL = os.getenv('DATABASE_URL', 'postgresql://postgresadmin:5oXcNX59QmEl7zmV3DbjemkiJ@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require')

# Test cases directory
TEST_CASES_DIR = Path("/Users/rabdin/Downloads/1633778")

# Question details
QUESTION_ID = str(uuid.uuid4())
QUESTION_TITLE = "Endpoint Inspection"
QUESTION_DIFFICULTY = "Easy"
QUESTION_TAGS = ["Arrays", "Sorting", "Problem solving"]

# Problem description (HTML formatted)
PROBLEM_DESCRIPTION = """<h3>Problem</h3>

<p>Analyze a BandwidthOptimizer system that inspects API endpoints for bandwidth issues. The system operates as follows:</p>

<ul>
    <li>There are m API endpoints numbered 1 to m.</li>
    <li>n specific endpoints in the endpoint array have confirmed bandwidth issues.</li>
    <li>The optimizer takes one second to reach endpoint 1 and one second for each transition. It traverses the endpoints from 1 to m.</li>
    <li>The system inspects endpoints when either:
        <ul>
            <li>There is a known issue at that endpoint.</li>
            <li>At least k seconds have passed since the last inspection.</li>
        </ul>
    </li>
</ul>

<p><strong>Your task is to determine the minimum number of inspections required if one problematic endpoint is manually corrected, and how many endpoints achieve this minimum.</strong></p>

<h3>Example</h3>

<p>m = 5, n = 2, k = 2, endpoint = [2, 5]</p>

<p>There are 5 endpoints with 2 issues at endpoints 2 and 5. The interval between checks is 2 seconds.</p>

<ul>
    <li>If the error at endpoint 2 is manually corrected, the optimizer will check points 2, 4, and 5.</li>
    <li>If the error at endpoint 5 is manually corrected, the optimizer will check points 2 and 4.</li>
</ul>

<p>So, the minimum number of checks is two for the case when the issue at endpoint 5 is manually corrected. Only one scenario requires just two checks.</p>

<p>Hence, the answer is 2 checks and 1 scenario, i.e., [2, 1].</p>

<h3>Function Description</h3>

<p>Complete the function <code>getMinChecks</code> in the editor with the following parameter(s):</p>

<ul>
    <li><code>int endpoint[n]</code>: the API endpoints with known bandwidth issues</li>
    <li><code>int m</code>: the total number of API endpoints</li>
    <li><code>int k</code>: the time that the optimizer must wait before checking an endpoint for bandwidth issues</li>
</ul>

<p><strong>Returns:</strong> <code>int[2]</code>: the integer at the first index represents the minimum number of endpoints that must be checked after resolving the issues at one endpoint, and the second integer represents the number of endpoints where this minimum number of inspections is attained</p>

<h3>Constraints</h3>

<ul>
    <li>1 ≤ k ≤ m ≤ 10<sup>9</sup></li>
    <li>1 ≤ n ≤ min(2 × 10<sup>5</sup>, m)</li>
    <li>1 ≤ endpoint[i] ≤ m</li>
</ul>"""

# Boilerplates
BOILERPLATES = {
    "cpp": """#include <bits/stdc++.h>
using namespace std;

string ltrim(const string &);
string rtrim(const string &);

/*
 * Complete the 'getMinChecks' function below.
 *
 * The function is expected to return an INTEGER_ARRAY.
 * The function accepts following parameters:
 *  1. INTEGER_ARRAY endpoint
 *  2. INTEGER m
 *  3. INTEGER k
 */
vector<int> getMinChecks(vector<int> endpoint, int m, int k) {
}

int main()
{
    ofstream fout(getenv("OUTPUT_PATH"));
    string endpoint_count_temp;
    getline(cin, endpoint_count_temp);
    int endpoint_count = stoi(ltrim(rtrim(endpoint_count_temp)));
    vector<int> endpoint(endpoint_count);
    for (int i = 0; i < endpoint_count; i++) {
        string endpoint_item_temp;
        getline(cin, endpoint_item_temp);
        int endpoint_item = stoi(ltrim(rtrim(endpoint_item_temp)));
        endpoint[i] = endpoint_item;
    }
    string m_temp;
    getline(cin, m_temp);
    int m = stoi(ltrim(rtrim(m_temp)));
    string k_temp;
    getline(cin, k_temp);
    int k = stoi(ltrim(rtrim(k_temp)));
    vector<int> result = getMinChecks(endpoint, m, k);
    for (size_t i = 0; i < result.size(); i++) {
        fout << result[i];
        if (i != result.size() - 1) {
            fout << "\\n";
        }
    }
    fout << "\\n";
    fout.close();
    return 0;
}

string ltrim(const string &str) {
    string s(str);
    s.erase(
        s.begin(),
        find_if(s.begin(), s.end(), not1(ptr_fun<int, int>(isspace)))
    );
    return s;
}

string rtrim(const string &str) {
    string s(str);
    s.erase(
        find_if(s.rbegin(), s.rend(), not1(ptr_fun<int, int>(isspace))).base(),
        s.end()
    );
    return s;
}""",
    
    "java": """import java.io.*;
import java.math.*;
import java.security.*;
import java.text.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.function.*;
import java.util.regex.*;
import java.util.stream.*;
import static java.util.stream.Collectors.joining;
import static java.util.stream.Collectors.toList;

class Result {
    /*
     * Complete the 'getMinChecks' function below.
     *
     * The function is expected to return an INTEGER_ARRAY.
     * The function accepts following parameters:
     *  1. INTEGER_ARRAY endpoint
     *  2. INTEGER m
     *  3. INTEGER k
     */
    public static List<Integer> getMinChecks(List<Integer> endpoint, int m, int k) {
    // Write your code here
    }
}

public class Solution {
    public static void main(String[] args) throws IOException {
        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(System.in));
        BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter(System.getenv("OUTPUT_PATH")));
        int endpointCount = Integer.parseInt(bufferedReader.readLine().trim());
        List<Integer> endpoint = IntStream.range(0, endpointCount).mapToObj(i -> {
            try {
                return bufferedReader.readLine().replaceAll("\\\\s+$", "");
            } catch (IOException ex) {
                throw new RuntimeException(ex);
            }
        })
            .map(String::trim)
            .map(Integer::parseInt)
            .collect(toList());
        int m = Integer.parseInt(bufferedReader.readLine().trim());
        int k = Integer.parseInt(bufferedReader.readLine().trim());
        List<Integer> result = Result.getMinChecks(endpoint, m, k);
        bufferedWriter.write(
            result.stream()
                .map(Object::toString)
                .collect(joining("\\n"))
            + "\\n"
        );
        bufferedReader.close();
        bufferedWriter.close();
    }
}""",
    
    "python": """#!/bin/python3
import math
import os
import random
import re
import sys

#
# Complete the 'getMinChecks' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts following parameters:
#  1. INTEGER_ARRAY endpoint
#  2. INTEGER m
#  3. INTEGER k
#
def getMinChecks(endpoint, m, k):
    # Write your code here

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    endpoint_count = int(input().strip())
    endpoint = []
    for _ in range(endpoint_count):
        endpoint_item = int(input().strip())
        endpoint.append(endpoint_item)
    m = int(input().strip())
    k = int(input().strip())
    result = getMinChecks(endpoint, m, k)
    fptr.write('\\n'.join(map(str, result)))
    fptr.write('\\n')
    fptr.close()""",
    
    "javascript": """'use strict';
const fs = require('fs');
process.stdin.resume();
process.stdin.setEncoding('utf-8');
let inputString = '';
let currentLine = 0;
process.stdin.on('data', function(inputStdin) {
    inputString += inputStdin;
});
process.stdin.on('end', function() {
    inputString = inputString.split('\\n');
    main();
});
function readLine() {
    return inputString[currentLine++];
}
/*
 * Complete the 'getMinChecks' function below.
 *
 * The function is expected to return an INTEGER_ARRAY.
 * The function accepts following parameters:
 *  1. INTEGER_ARRAY endpoint
 *  2. INTEGER m
 *  3. INTEGER k
 */
function getMinChecks(endpoint, m, k) {
    // Write your code here
}
function main() {
    const ws = fs.createWriteStream(process.env.OUTPUT_PATH);
    const endpointCount = parseInt(readLine().trim(), 10);
    let endpoint = [];
    for (let i = 0; i < endpointCount; i++) {
        const endpointItem = parseInt(readLine().trim(), 10);
        endpoint.push(endpointItem);
    }
    const m = parseInt(readLine().trim(), 10);
    const k = parseInt(readLine().trim(), 10);
    const result = getMinChecks(endpoint, m, k);
    ws.write(result.join('\\n') + '\\n');
    ws.end();
}""",
    
    "csharp": """using System.CodeDom.Compiler;
using System.Collections.Generic;
using System.Collections;
using System.ComponentModel;
using System.Diagnostics.CodeAnalysis;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.Serialization;
using System.Text.RegularExpressions;
using System.Text;
using System;

class Result {
    /*
     * Complete the 'getMinChecks' function below.
     *
     * The function is expected to return an INTEGER_ARRAY.
     * The function accepts following parameters:
     *  1. INTEGER_ARRAY endpoint
     *  2. INTEGER m
     *  3. INTEGER k
     */
    public static List<int> getMinChecks(List<int> endpoint, int m, int k)
    {
    }
}

class Solution {
    public static void Main(string[] args)
    {
        TextWriter textWriter = new StreamWriter(@System.Environment.GetEnvironmentVariable("OUTPUT_PATH"), true);
        int endpointCount = Convert.ToInt32(Console.ReadLine().Trim());
        List<int> endpoint = new List<int>();
        for (int i = 0; i < endpointCount; i++)
        {
            int endpointItem = Convert.ToInt32(Console.ReadLine().Trim());
            endpoint.Add(endpointItem);
        }
        int m = Convert.ToInt32(Console.ReadLine().Trim());
        int k = Convert.ToInt32(Console.ReadLine().Trim());
        List<int> result = Result.getMinChecks(endpoint, m, k);
        textWriter.WriteLine(String.Join("\\n", result));
        textWriter.Flush();
        textWriter.Close();
    }
}"""
}

def read_test_cases(test_dir):
    """Read all test cases from the directory"""
    test_cases = []
    sample_test_cases = []
    
    # Get all input files sorted
    input_files = sorted([f for f in test_dir.glob("input*.txt")])
    
    for i, input_file in enumerate(input_files):
        # Extract test case number
        test_num = input_file.stem.replace("input", "")
        output_file = test_dir / f"output{test_num}.txt"
        
        if not output_file.exists():
            print(f"Warning: {output_file} not found, skipping test case {test_num}")
            continue
        
        # Read input and output
        with open(input_file, 'r') as f:
            input_data = f.read().strip()
        
        with open(output_file, 'r') as f:
            output_data = f.read().strip()
        
        test_case = {
            "id": f"test_case_{test_num}",
            "input": input_data,
            "expected_output": output_data
        }
        
        # First 3 are sample test cases (000, 001, 002)
        if i < 3:
            sample_test_cases.append(test_case)
        else:
            test_cases.append(test_case)
    
    return sample_test_cases, test_cases

async def add_question_to_db():
    """Add the question to the database"""
    # Read test cases
    sample_test_cases, test_cases = read_test_cases(TEST_CASES_DIR)
    
    print(f"📊 Found {len(sample_test_cases)} sample test cases and {len(test_cases)} regular test cases")
    
    # Connect to database
    conn = await asyncpg.connect(DB_URL)
    
    try:
        # Prepare data - match existing table structure
        # boiler_plate is stored as JSON string (text), not JSONB
        boilerplate_json = json.dumps(BOILERPLATES)
        
        # Convert tags to lowercase to match existing format
        tags_lower = [tag.lower() for tag in QUESTION_TAGS]
        
        # Insert question - match existing table structure
        await conn.execute("""
            INSERT INTO coding_question_bank (
                uuid, question, difficulty, tags,
                boiler_plate, sample_test_cases, test_cases
            ) VALUES ($1, $2, $3, $4, $5, $6, $7)
            ON CONFLICT (uuid) DO UPDATE SET
                question = EXCLUDED.question,
                difficulty = EXCLUDED.difficulty,
                tags = EXCLUDED.tags,
                boiler_plate = EXCLUDED.boiler_plate,
                sample_test_cases = EXCLUDED.sample_test_cases,
                test_cases = EXCLUDED.test_cases
        """,
            QUESTION_ID,
            PROBLEM_DESCRIPTION,
            QUESTION_DIFFICULTY.lower(),  # lowercase to match existing
            json.dumps(tags_lower),
            boilerplate_json,
            json.dumps(sample_test_cases),
            json.dumps(test_cases)
        )
        
        print(f"✅ Question added successfully!")
        print(f"   UUID: {QUESTION_ID}")
        print(f"   Title: {QUESTION_TITLE}")
        print(f"   Difficulty: {QUESTION_DIFFICULTY}")
        print(f"   Tags: {QUESTION_TAGS}")
        print(f"   Sample Test Cases: {len(sample_test_cases)}")
        print(f"   Regular Test Cases: {len(test_cases)}")
        print(f"   Total Test Cases: {len(sample_test_cases) + len(test_cases)}")
        print(f"   Languages: {list(BOILERPLATES.keys())}")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(add_question_to_db())

