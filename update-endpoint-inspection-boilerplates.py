#!/usr/bin/env python3
"""
Update boilerplates for Endpoint Inspection question with corrected versions
"""

import json
import os
import asyncpg
import asyncio

# Database connection
DB_URL = os.getenv('DATABASE_URL', 'postgresql://postgresadmin:5oXcNX59QmEl7zmV3DbjemkiJ@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require')

QUESTION_UUID = "eaec23b4-be2c-4b65-8745-15c265a56f75"

# Corrected boilerplates (matching working test versions)
CORRECTED_BOILERPLATES = {
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
        cout << result[i];
        if (i != result.size() - 1) {
            cout << "\\n";
        }
    }
    cout << "\\n";
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

class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(System.in));
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
        System.out.println(
            result.stream()
                .map(Object::toString)
                .collect(joining("\\n"))
        );
        bufferedReader.close();
    }
}""",
    
    "python": """def getMinChecks(endpoint, m, k):
    # Write your code here

endpoint_count = int(input().strip())
endpoint = []
for _ in range(endpoint_count):
    endpoint_item = int(input().strip())
    endpoint.append(endpoint_item)
m = int(input().strip())
k = int(input().strip())
result = getMinChecks(endpoint, m, k)
print('\\n'.join(map(str, result)))""",
    
    "javascript": """function getMinChecks(endpoint, m, k) {
    // Write your code here
}

const readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false
});

const lines = [];
rl.on('line', (line) => {
    lines.push(line);
});

rl.on('close', () => {
    const endpointCount = parseInt(lines[0].trim(), 10);
    let endpoint = [];
    for (let i = 1; i <= endpointCount; i++) {
        endpoint.push(parseInt(lines[i].trim(), 10));
    }
    const m = parseInt(lines[endpointCount + 1].trim(), 10);
    const k = parseInt(lines[endpointCount + 2].trim(), 10);
    const result = getMinChecks(endpoint, m, k);
    console.log(result.join('\\n'));
});""",
    
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
        Console.WriteLine(String.Join("\\n", result));
    }
}"""
}

async def update_boilerplates():
    """Update boilerplates in the database"""
    conn = await asyncpg.connect(DB_URL)
    
    try:
        # Get current question
        row = await conn.fetchrow(
            "SELECT boiler_plate FROM coding_question_bank WHERE uuid = $1",
            QUESTION_UUID
        )
        
        if not row:
            print(f"❌ Question {QUESTION_UUID} not found!")
            return
        
        # Update boilerplates
        await conn.execute("""
            UPDATE coding_question_bank
            SET boiler_plate = $1
            WHERE uuid = $2
        """,
            json.dumps(CORRECTED_BOILERPLATES),
            QUESTION_UUID
        )
        
        print(f"✅ Boilerplates updated successfully!")
        print(f"   Question UUID: {QUESTION_UUID}")
        print(f"   Languages updated: {', '.join(CORRECTED_BOILERPLATES.keys())}")
        print(f"\n📋 Changes made:")
        print(f"   - Python: Removed blocked imports, using print()")
        print(f"   - Java: Changed to Main class, using System.out.println()")
        print(f"   - JavaScript: Removed require('fs'), using readline + console.log()")
        print(f"   - C++: Changed to cout instead of ofstream")
        print(f"   - C#: Changed to Console.WriteLine() instead of StreamWriter")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(update_boilerplates())




