#!/usr/bin/env python3
"""
Generic data generator for ALL topics
Scans repo structure and generates complete data for website
"""

import json
from pathlib import Path

def read_python_file(filepath):
    """Read Python file"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read().strip()
    except:
        return None

def scan_folder_for_problems(folder_path):
    """Find all .py files in a folder (including subfolders)"""
    problems = []
    if folder_path.exists():
        for py_file in sorted(folder_path.rglob("*.py")):
            code = read_python_file(py_file)
            if code:
                problems.append({
                    "name": py_file.stem.replace('-', ' ').replace('_', ' ').title(),
                    "file": py_file.name,
                    "code_preview": code[:200] + "..." if len(code) > 200 else code
                })
    return problems

def scan_all_topics():
    """Scan ALL topics and generate data"""
    repo_root = Path("../")  # One level up from website/ is python-coding-concepts/

    results = {}

    topics_to_scan = [
        "Array", "Trees", "Graph", "LinkedList", "BinarySearch",
        "Backtracking", "Greedy", "BitManipulation", "Heap", "Maps",
        "Strings", "Recursion", "DP", "MergeIntervals", "Range-Query",
        "Matrix", "Sliding window"
    ]

    print("[*] SCANNING ALL TOPICS FROM REPO...\n")

    total_problems = 0
    total_notes = 0

    for topic_name in topics_to_scan:
        topic_path = repo_root / topic_name

        if topic_path.exists():
            problems = scan_folder_for_problems(topic_path)

            # Scan for notes
            notes_path = topic_path / "notes"
            notes_count = 0
            notes_list = []
            if notes_path.exists():
                notes_list = [f.name for f in notes_path.glob("*.md")]
                notes_count = len(notes_list)

            results[topic_name] = {
                "problem_count": len(problems),
                "note_count": notes_count,
                "problems": [p["name"] for p in problems],
                "notes": notes_list
            }

            total_problems += len(problems)
            total_notes += notes_count

            print(f"[OK] {topic_name:20} : {len(problems):2} problems, {notes_count:2} notes")

    # Special handling for DP nested structure
    dp_root = repo_root / "DP"
    if dp_root.exists():
        print(f"\n[*] DP NESTED STRUCTURE:")
        dp_categories = {}

        for subfolder in sorted(dp_root.iterdir()):
            if subfolder.is_dir() and subfolder.name != "notes":
                probs = scan_folder_for_problems(subfolder)
                dp_categories[subfolder.name] = {
                    "problem_count": len(probs),
                    "problems": [p["name"] for p in probs]
                }
                total_problems += len(probs)
                print(f"  - {subfolder.name:30} : {len(probs):2} problems")

        results["DP"]["categories"] = dp_categories

    return results, total_problems, total_notes

if __name__ == "__main__":
    data, total_probs, total_notes = scan_all_topics()

    print(f"\n{'='*60}")
    print(f"[OK] SCAN COMPLETE!")
    print(f"{'='*60}")
    print(f"\nTOTAL PROBLEMS: {total_probs}")
    print(f"TOTAL NOTE FILES: {total_notes}")
    print(f"TOTAL TOPICS: {len(data)}")

    # Save JSON
    with open('complete-problem-inventory.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    print(f"\n[OK] Saved to: complete-problem-inventory.json")
    print(f"\nFILE STRUCTURE:")
    print(f"  - Top-level topics: {len(data)}")
    print(f"  - Total problems across all topics: {total_probs}")
    print(f"  - DP subcategories: {len(data.get('DP', {}).get('categories', {}))}")

    print(f"\n[*] Use this data to update the website!")
