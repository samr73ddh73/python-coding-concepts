#!/usr/bin/env python3
"""
Generate comprehensive data for ALL topics from repo structure
Scans problem folders and creates structured data for website
"""

import os
import json
from pathlib import Path

def read_python_file(filepath):
    """Read Python file and extract code"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except:
        return None

def read_markdown_file(filepath):
    """Read markdown file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except:
        return None

def scan_topic_folder(topic_path):
    """Generically scan any topic folder for problems and notes"""
    result = {
        "problems": [],
        "notes": {}
    }

    # Scan for Python files (problems)
    for py_file in sorted(topic_path.glob("**/*.py")):
        code = read_python_file(py_file)
        if code:
            result["problems"].append({
                "name": py_file.stem.replace('-', ' ').title(),
                "filename": py_file.name,
                "path": str(py_file.relative_to(topic_path)),
                "code": code
            })

    # Scan for markdown files (notes)
    notes_path = topic_path / "notes"
    if notes_path.exists():
        for md_file in sorted(notes_path.glob("*.md")):
            content = read_markdown_file(md_file)
            if content:
                result["notes"][md_file.stem] = content

    return result

def scan_all_topics():
    """Scan all DSA topics in the repo"""
    repo_root = Path("../../")  # Adjust to repo root
    results = {}

    # Define main topics to scan
    topics = [
        "Array", "Trees", "Graph", "LinkedList", "BinarySearch", "DP",
        "Backtracking", "Greedy", "BitManipulation", "Heap", "Maps",
        "Strings", "Recursion", "Matrix", "MergeIntervals", "Range-Query"
    ]

    total_problems = 0
    total_notes = 0

    for topic in topics:
        topic_path = repo_root / topic
        if topic_path.exists():
            print(f"[*] Scanning {topic}...")
            data = scan_topic_folder(topic_path)

            results[topic] = {
                "problems_count": len(data["problems"]),
                "notes_count": len(data["notes"]),
                "problems": data["problems"],
                "notes": list(data["notes"].keys())
            }

            total_problems += len(data["problems"])
            total_notes += len(data["notes"])

            print(f"    - {len(data['problems'])} problems")
            print(f"    - {len(data['notes'])} notes")

    # Special handling for DP nested structure
    dp_root = repo_root / "DP"
    if dp_root.exists():
        print(f"[*] Scanning DP (with nested structure)...")
        dp_categories = {}

        for subfolder in sorted(dp_root.iterdir()):
            if subfolder.is_dir() and not subfolder.name == "notes":
                category_data = scan_topic_folder(subfolder)
                dp_categories[subfolder.name] = {
                    "problems_count": len(category_data["problems"]),
                    "problems": category_data["problems"]
                }
                total_problems += len(category_data["problems"])

        if "DP" in results:
            results["DP"]["categories"] = dp_categories

    return results, total_problems, total_notes

def generate_javascript_object(problems_dict):
    """Generate JavaScript object string for embedding"""

    # Count total problems
    total = sum(len(v) for v in problems_dict.values())

    print(f"Found {total} DP problems across {len(problems_dict)} categories:\n")

    for category, problems in problems_dict.items():
        print(f"  {category}: {len(problems)} problems")
        for p in problems:
            print(f"    - {p['name']}")

    print(f"\n[OK] Total DP Problems: {total}")
    print("\n[*] JavaScript Data Structure (ready to embed in dsa-topic-new.html):")
    print("=" * 60)

    # Generate the data structure
    output = """
    // AUTO-GENERATED DP PROBLEMS DATA
    const dpProblems = {
"""

    for category, problems in problems_dict.items():
        output += f'      "{category}": {{\n'
        output += f'        "name": "{category.replace("-", " ").title()}",\n'
        output += f'        "problems": [\n'

        for i, problem in enumerate(problems):
            code_escaped = problem['code'].replace('`', '\\`').replace('"', '\\"')
            output += f'''          {{
            "name": "{problem['name']}",
            "filename": "{problem['filename']}",
            "code": `{code_escaped}`
          }}'''
            if i < len(problems) - 1:
                output += ','
            output += '\n'

        output += '        ]\n'
        output += '      }'

        # Check if not last category
        categories = list(problems_dict.keys())
        if category != categories[-1]:
            output += ','
        output += '\n'

    output += '    };\n'

    return output, total

if __name__ == "__main__":
    print("[*] Scanning DP folder structure...\n")

    problems = get_dp_structure()
    js_output, total = generate_javascript_object(problems)

    # Save to file
    with open('dp-problems-generated.js', 'w', encoding='utf-8') as f:
        f.write(js_output)

    print("\n✅ Generated dp-problems-generated.js")
    print(f"📊 Total problems embedded: {total}")
    print("\n📝 Next steps:")
    print("   1. Copy the generated JavaScript object")
    print("   2. Paste into dsa-topic-new.html DP section")
    print("   3. Update HTML to display categorized problems")
