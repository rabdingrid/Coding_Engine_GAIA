import os
from datasets import load_dataset
import random

OUTPUT_DIR = "cf"
COUNT = 30
MIN_RATING = 800
MAX_RATING = 1400
TAGS_INTEREST = ["implementation", "greedy", "strings", "arrays"]

def save_problem(problem, index):
    # Create folder
    contest_id = problem['contest_id']
    prob_index = problem['index']
    folder_name = f"{contest_id}_{prob_index}"
    folder_path = os.path.join(OUTPUT_DIR, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    
    # Save Problem Markdown
    md_content = f"""# {problem['title']}

## Rating: {problem['rating']}
## Tags: {', '.join(problem['tags'])}

## Description
{problem['description']}

## Input Format
{problem['input_format']}

## Output Format
{problem['output_format']}

## Examples
"""
    for i, ex in enumerate(problem['examples']):
        md_content += f"\n### Example {i+1}\n**Input:**\n```\n{ex['input']}\n```\n**Output:**\n```\n{ex['output']}\n```\n"

    with open(os.path.join(folder_path, "problem.md"), "w") as f:
        f.write(md_content)
        
    # Save Test Cases
    tc_dir = os.path.join(folder_path, "test_cases")
    os.makedirs(tc_dir, exist_ok=True)
    
    # Combine examples and official tests
    # Use examples first
    test_cases = []
    if problem['examples']:
        test_cases.extend(problem['examples'])
    
    # Add official tests if available (limit to 20 to avoid huge storage usage)
    if problem['official_tests']:
        # Filter out duplicates from examples if possible, but simple append is fine for now
        # We'll take up to 20 official tests
        test_cases.extend(problem['official_tests'][:20])
        
    for i, tc in enumerate(test_cases):
        # Clean up input/output (sometimes they have \r\n)
        inp = tc['input'].replace('\r\n', '\n')
        out = tc['output'].replace('\r\n', '\n')
        
        with open(os.path.join(tc_dir, f"{i+1}.in"), "w") as f:
            f.write(inp)
        with open(os.path.join(tc_dir, f"{i+1}.out"), "w") as f:
            f.write(out)
            
    print(f"Saved {folder_name} with {len(test_cases)} test cases.")

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print("Loading dataset stream...")
    ds = load_dataset("open-r1/codeforces", split="train", streaming=True)
    
    collected = []
    print("Filtering problems...")
    
    for item in ds:
        # Check rating
        if item['rating'] is None or not (MIN_RATING <= item['rating'] <= MAX_RATING):
            continue
            
        # Check tags (optional, but good for interview style)
        # item['tags'] is a list of strings
        if not any(tag in item['tags'] for tag in TAGS_INTEREST):
            continue
            
        collected.append(item)
        if len(collected) >= COUNT * 2: # Collect more to shuffle
            break
            
    # Shuffle to get random selection
    random.shuffle(collected)
    selected = collected[:COUNT]
    
    print(f"Saving {len(selected)} problems...")
    for i, prob in enumerate(selected):
        save_problem(prob, i)
        
    print("Done!")

if __name__ == "__main__":
    main()
