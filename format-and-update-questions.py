#!/usr/bin/env python3
"""
Format questions with proper HTML and update database
Using content from read_file tool
"""

import json
import os
import asyncpg
import asyncio
import re

DB_URL = os.getenv('DATABASE_URL', 'postgresql://postgresadmin:5oXcNX59QmEl7zmV3DbjemkiJ@ai-ta-ra-postgre.postgres.database.azure.com:5432/railway?sslmode=require')

def format_question_html(question_text):
    """Format question with proper HTML structure like Endpoint Inspection"""
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

# Question content from read_file tool
QUESTIONS = {
    "13725261-21c9-424b-bced-e0be21078aeb": """Given an integer, convert its binary representation into a string or an array with digits indexed from 0 to the length of the binary string minus one. Reduce this binary representation to zero using specified operations:

Change the ith binary digit only if (i+1)th binary digit is 1 and all other binary digits from (i+2) to the end are zeros.

Change the rightmost digit without restriction.

Determine the minimum number of operations required to complete this task.

 

Example

n = 4

 

The binary representation of 4 is 100, so for the example, bin = [1, 0, 0].

100 → 101 → 111 → 110 → 010 → 011 → 001 → 000
 

bin, from left to right, has indices 0 to 3. Stepping through the operations:

Use rule 2 to change bin[2] to 1. 100 → 101
Use rule 1 to change bin[1] to 1. 101 → 111
Use rule 2 to change bin[2] to 0. 111 → 110
Use rule 1 to change bin[0] to 0. 110 → 010
Use rule 2 to change bin[2] to 1. 010 → 011
Use rule 1 to change bin[1] to 0. 011 → 001
Use rule 2 to change bin[2] to 0. 001 → 000
 

For this number, 7 operations are required to convert it to 0.

 

Note: In the binary representation of a number, the binary digits' positions are numbered as 0 to x-1 from left to right, where x is the number of digits in the binary representation of the number.

 

Function Description

Complete the function minOperations in the editor with the following parameter:

    long n:  the starting value in base 10

 

Returns

    int: the minimum number of operations required to convert n to 0

 

Constraints

1 ≤ n ≤ 1015

 

Input Format For Custom Testing
Sample Case 0
Sample Input For Custom Testing

STDIN     Function 
-----     --------
13    →   n = 13 
Sample Output

9
Explanation

The binary representation of 13 is 1101. This is the sequence of the 9 operations that change 13 to 0 according to the constraints:

1101→1100→0100→0101→0111→0110→0010→0011→0001→0000
Sample Case 1
Sample Input For Custom Testing

STDIN     Function
-----     --------
11     →  n = 11
Sample Output

13
Explanation

The binary representation of 11 is 1011. This is the sequence of the 13 operations that change 11 to 0 according to the constraints:

1011→1010→1110→1111→1101→1100→0100→0101→0111→0110→0010→0011→0001→0000""",
    
    "cf43bce1-dfc7-4d42-904b-0d9461641076": """Cartridge Recycling 
 75 points
 19 minute(s)
Ternary Search  Theme: E-commerce  Interviewer Guidelines  Math  Medium  Search 
An office supply store offers an ink cartridge recycling program where customers can either earn money for each recycled cartridge or combine recycled cartridges with cash to buy special products known as "perks items." A customer participating in this program wants to maximize the number of perks items they can purchase. Given a specific number of cartridges and dollars, determine how many perks items the customer can acquire.

 

Example

cartridges = 10

dollars = 10

recycleReward = 2, the amount earned by recycling a single cartridge

perksCost = 2, the amount required for a customer to buy a single perks item combined with a recycled cartridge

 

The best thing the customer can do is to first recycle 3 cartridges, earning 6 dollars. After this, 7 cartridges and 16 dollars are left. The 7 cartridges can be combined with 14 dollars to purchase 7 perks items. This is the maximum number of perks items that can be bought.

 

Function Description

Complete the maxPerksItems function in the editor withthe following parameter(s):

    int cartridges: the number of cartridges on-hand

    int dollars: the number of dollars on-hand

    int recycleReward: dollars earned per recycled cartridge

    int perksCost: dollar cost of a perks item, in addition to recycling a single cartridge

 

Returns

    int: the maximum number of perks items that can be bought

 

Constraints

1 ≤ cartridges, dollars, recycleReward, perksCost ≤ 109

 

Input Format For Custom Testing
Sample Case 0
Sample Input

STDIN     Function
-----     -----
4      →  cartridges = 4
8      →  dollars = 8
3      →  recycleReward = 3
4      →  perksCost = 4
Sample Output

2
Explanation

The optimal solution is to combine 2 cartridges with 8 dollars to buy 2 perks items. There is no way to obtain more than 2 perks items.

Sample Case 1
Sample Input

STDIN     Function
-----     -----
3      →  cartridges = 3
6      →  dollars = 6
4      →  recycleReward = 4
5      →  perksCost = 5
Sample Output

2
Explanation

The optimal solution is to first recycle 1 cartridge, earning 4 dollars. This leaves 2 cartridges and 10 dollars. The 2 cartridges can be combined with the 10 dollars to buy 2 perks items. There is no way to obtain more than 2 perks items.""",
    
    "2149e972-0cec-4da7-84bc-2526b4640f30": """Modulo Challenge 
 75 points
 20 minute(s)
Problem Solving  Constructive Algorithms  Medium 
 
One of the key benefits of project work is that it makes school resemble real life more closely. To create a more engaging learning experience, Professor Hill decided to teach the concepts of modulo arithmetic through a project.

 

Professor Hill presents an array of numbers to the students and asks them to perform the following operation:

Select two adjacent positive numbers, a[i] and a[i+1]
Replace them with either (a[i] % a[i+1]) or (a[i+1] % a[i]), where x % y represents x modulo y
After each operation, the array has 1 less element.

 

The objective is to determine the minimum possible length of the array, which can be achieved by performing the operation any number of times.

 

Example

Consider the array's length to be n = 4 and the array of numbers to be arr = [1, 1, 2, 3]. 

 

The following sequence of operations can be performed (0-based indexing):

arr = [1, 1, 2, 3]
Choose i = 2, so arr[i] = 2 and arr[i + 1] = 3.
We get the new value to be given by 2 % 3 = 2 or 3 % 2 = 1. The resulting array can be [1, 1, 2] or [1, 1, 1].
We choose [1, 1, 2] to minimize the array length.
arr = [1, 1, 2]: Choose i = 1, thus arr[i] = 1 and arr[i + 1] = 2. 1 % 2 = 1 and the new array is [1, 1].
arr = [1, 1]: Choose i = 0, 1 % 1 = 0 and the array is [0].
Thus the minimum possible length for the array is 1.

 

Function Description

Complete the function getMinLength in the editor with the following parameters:

    int arr[n]:  the given array of integers

 

Returns

    int: the minimum possible length of the array.

 

Constraints

1 ≤ n ≤ 105
1 ≤ arr[i]  ≤ 109 
Input Format For Custom Testing
Sample Case 0
Sample Input For Custom Testing

STDIN         FUNCTION
-----         --------
4        →    arr[] size n = 4
2        →    arr = [2, 2, 2, 2]
2
2
2
Sample Output

2
Explanation

 

Choose i = 0, 2 % 2 = 0, and arr = [0, 2, 2].

Choose i = 1, 2 % 2 = 0, and arr = [0, 0]

Since there are no two adjacent positive numbers, we cannot perform any further operations.

Sample Case 1
Sample Input For Custom Testing

STDIN         FUNCTION
-----         --------
3        →    arr[] size n = 3
1        →    arr = [1, 1, 3]
1
3
Sample Output

1
Explanation

 

Choose i = 1, 1 % 3 = 1 and arr = [1, 1].

Choose i = 0, 1 % 1 = 0 and arr = [0]""",
    
    "4d76d396-bf37-492d-86ba-2d611d2193c8": """API Rate-Limiting 
 50 points
 20 minute(s)
Easy  Priority Queues  Data Structures  Interviewer Guidelines 
You are building a system that distributes API requests across n servers. Each server has a certain capacity, given by capacity[i], which is the number of requests it can handle in 1 second. After handling requests, the server's capacity becomes half of what it was before (rounded down).

 

Implement a function that returns the minimum time required to handle all incoming requests given by requests.

 

The function calculateSchedulingTime takes the following inputs:

    int capacity[n]:  each element denotes the capacity of the ith server 

    long requests: the number of incoming API requests

 

The function should return an integer, the minimum time required to process all incoming API requests.

 

Example

n = 5 

capacity = [3, 1, 7, 2, 4]

requests = 15

 

The optimal solution is:

First, the node with capacity = 7 schedules 7 requests in one second. Now, capacity = [3, 1, 3, 2, 4] because 7 was reduced to floor(7/2). There are 15 - 7 = 8 remaining requests.

Second, the node with capacity = 4 is used. After that, capacity = [3, 1, 3, 2, 2]. Remaining requests = 8 - 4 = 4.

Third, a node with capacity = 3 is used. Now, capacity = [1, 1, 3, 2, 2]. Remaining requests = 4 - 3 = 1.

Finally, a node with a capacity of 1 is used to schedule the final request.

 

Each step requires one second of processing time, so the answer is 4.

 

Constraints

1 ≤ n ≤ 105
1 ≤ capacity[i]  ≤ 106
1 ≤ requests ≤ 1012
It is guaranteed that the requests can be scheduled using the given system.
Input Format For Custom Testing
Sample Case 0
Sample Input For Custom Testing

STDIN      Function
-----      --------
5      →   capacity[] size n = 5
2      →   capacity = [2, 1, 5, 3, 1]
1
5
3
1
17     →   requests = 17
Sample Output

9
Explanation

The optimal solution is :

After choosing the servers with capacity = 2, 5, and 3, a total of 10 requests are scheduled (requiring 3 seconds, one for each server). Now, capacity = [1, 1, 2, 1, 1] and there are 17 - 10 = 7 remaining requests.
Then choose the server with capacity = 2 to schedule 2 requests (requiring 1 second). After that, capacity = [1, 1, 1, 1, 1], and there are 7 - 2 = 5 requests remaining.
All 5 servers are used to schedule one request each (requiring 5 seconds).
 

The total time required is (3+1+5) = 9 seconds.

Sample Case 1
Sample Input For Custom Testing

STDIN      Function
-----      --------
4      →   capacity[] size n = 4
3      →   capacity = [3, 1, 4, 2]
1
4
2
3      →   requests = 3
Sample Output

1
Explanation

Choose the server with capacity = 3. All 3 requests are scheduled, and the total time required is 1 second.""",
    
    "66f674e3-b85e-4175-8bcc-a25e9eeb8324": """Maximal Permutation 
 75 points
 37 minute(s)
Algorithms  Graphs  Data Structures  Disjoint Sets  Medium  Depth First Search  Problem Solving 
You have a circular list of integers called container. Two index arrays, firstPositions and secondPositions, along with an integer array slides, define possible swaps. For each element i in slides, determine:

The index in container corresponding to firstPositions[i] - slides[i]
The index in container corresponding to secondPositions[i] + slides[i]
Values at these index pairs may be swapped any number of times. Find the lexicographically maximal permutation possible after performing any number of these swaps.

 

Example

container = [1, 2, 3, 4, 5]

firstPositions = [2, 2]

secondPositions = [3, 3]

slides = [1, 3]

 

Return: [1, 5, 3, 4, 2]

 

Explanation:

From slides[0], we can swap container[1] = 2 and container[4] = 5
From slides[1], we can also swap container[4] = 5 and container[1] = 2
Swapping these values gives [1, 5, 3, 4, 2], which is lexicographically greater than [1, 2, 3, 4, 5]
 
Function Description

 

Complete the maximalPermutation function in the editor with the following parameters:

    int container[n]: the integers to permute

    int firstPositions[m]: the indices to slide using operation 1

    int secondPositions[m]: the indices to slide using operation 2

    int slides[m]: how far to slide each index

 

Returns

    int[n]: the maximal permutation of container

 

Constraints

1 ≤ n, m ≤ 105
1 ≤ container[j] ≤ 109 where 0 ≤  j < n
0 ≤ firstPositions[i], secondPositions[i] < m, where 0 ≤ i < m
0 ≤ slides[i] ≤ 109, where 0 ≤ i < m
 
Input Format For Custom Testing
The first line contains an integer, n,the size of container.

Each line j of the n subsequent lines (where 0 ≤ j < n) contains an integer, container[j].

The next line contains an integer, m, the size of firstPositions.

Each line i of the m subsequent lines (where 0 ≤ i < m) contains an integer, firstPositions[i].

The next line contains an integer, m, the size of secondPositions.

Each line i of the m subsequent lines (where 0 ≤ i < m) contains an integer, secondPositions[i].

The next line contains an integer, m, the size of slides.

Each line i of the m subsequent lines (where 0 ≤ i < m) contains an integer, slides[i].

Sample Case 0
Sample Input 0

STDIN       Function
-----       --------
4           container[] size n = 4
2           container = [2, 4, 3, 1]
4
3
1
2           firstPostions[] size m = 2
0           firstPostions = [0, 1]
1
2           secondPositions[] size m = 2
2           secondPostions = [2, 3]
3
2           slides[] size m = 2
0           slides = [0, 4]
4
 

Sample Output 0

3
4
2
1"""
}

async def update_all():
    """Update all questions with properly formatted HTML"""
    conn = await asyncpg.connect(DB_URL)
    
    try:
        print("📝 Formatting and updating questions...")
        
        for uuid_val, question_text in QUESTIONS.items():
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
                print(f"   ✅ Updated: {uuid_val[:8]}... (first para: {len(first_para)} chars)")
            else:
                print(f"   ⚠️  First para too short: {uuid_val[:8]}...")
        
        print("\n✅ All questions updated!")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(update_all())




