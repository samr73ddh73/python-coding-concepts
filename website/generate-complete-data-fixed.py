#!/usr/bin/env python3
"""
COMPLETE DATA GENERATOR - FIXED
Uses data.js naming convention for topic names
"""

import json
from pathlib import Path

# Mapping from folder names to display names (matching data.js)
TOPIC_NAME_MAP = {
    "Array": "Arrays",
    "Trees": "Trees",
    "Graph": "Graphs",
    "LinkedList": "Linked Lists",
    "BinarySearch": "Binary Search",
    "DP": "Dynamic Programming",
    "Backtracking": "Backtracking",
    "Greedy": "Greedy",
    "BitManipulation": "Bit Manipulation",
    "Heap": "Heap",
    "Maps": "Maps",
    "Strings": "Strings",
    "Recursion": "Recursion",
    "MergeIntervals": "Merge Intervals",
    "Range-Query": "Range Query",
    "Matrix": "Matrix",
    "Sliding window": "Sliding Window"
}

def read_file(filepath):
    """Read any file safely"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read().strip()
    except:
        return None

def scan_topic(topic_path, display_name):
    """Scan a topic folder for problems and notes"""
    result = {
        "problems": [],
        "notes": []
    }

    # Scan for Python files (problems) - recursively
    if topic_path.exists():
        for py_file in sorted(topic_path.rglob("*.py")):
            code = read_file(py_file)
            if code:
                result["problems"].append({
                    "name": py_file.stem.replace('-', ' ').replace('_', ' ').title(),
                    "filename": py_file.name,
                    "path": str(py_file.relative_to(topic_path)),
                    "code": code
                })

    # Scan for markdown files (notes)
    notes_path = topic_path / "notes"
    if notes_path.exists():
        for md_file in sorted(notes_path.glob("*.md")):
            content = read_file(md_file)
            if content:
                result["notes"].append({
                    "name": md_file.stem.replace('-', ' ').replace('_', ' ').title(),
                    "filename": md_file.name,
                    "content": content
                })

    return result

def generate_all_data():
    """Generate complete data for all topics"""
    repo_root = Path("../")
    all_data = {}

    print("[*] GENERATING COMPLETE DATA WITH CORRECT NAMES...\n")

    total_problems = 0
    total_notes = 0

    for folder_name, display_name in sorted(TOPIC_NAME_MAP.items()):
        topic_path = repo_root / folder_name

        if topic_path.exists():
            data = scan_topic(topic_path, display_name)

            all_data[display_name] = {
                "name": display_name,
                "folder": folder_name,
                "problems": data["problems"],
                "notes": data["notes"]
            }

            total_problems += len(data["problems"])
            total_notes += len(data["notes"])

            print(f"[OK] {display_name:30} : {len(data['problems']):3} problems, {len(data['notes']):2} notes")

    # SPECIAL HANDLING FOR DP NESTED STRUCTURE
    print(f"\n[*] PROCESSING DP NESTED STRUCTURE:")
    dp_root = repo_root / "DP"
    if dp_root.exists():
        dp_categories = {}

        # Map category folders
        category_map = {
            "1-Knapsack": "0-1 Knapsack",
            "2-Unbounded-Knapsack": "Unbounded Knapsack",
            "3-LCS": "LCS (Longest Common Subsequence)",
            "4-MCM": "MCM (Matrix Chain Multiplication)",
            "DP-on-Grids": "DP on Grids"
        }

        for folder_name, display_name in category_map.items():
            cat_path = dp_root / folder_name
            if cat_path.exists():
                cat_data = scan_topic(cat_path, display_name)
                dp_categories[display_name] = {
                    "name": display_name,
                    "folder": folder_name,
                    "problems": cat_data["problems"]
                }
                total_problems += len(cat_data["problems"])
                print(f"  [OK] {display_name:35} : {len(cat_data['problems']):2} problems")

        # Update DP entry with categories
        if "Dynamic Programming" in all_data:
            all_data["Dynamic Programming"]["categories"] = dp_categories

    print(f"\n{'='*60}")
    print(f"[OK] DATA GENERATION COMPLETE!")
    print(f"{'='*60}")
    print(f"Total problems: {total_problems}")
    print(f"Total notes: {total_notes}")
    print(f"Total topics: {len(all_data)}")

    return all_data

if __name__ == "__main__":
    data = generate_all_data()

    # Save to JSON
    with open('all-data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] Saved to: all-data.json")
    print(f"\n[*] Topics in JSON:")
    for topic in sorted(data.keys()):
        print(f"    - {topic}")
