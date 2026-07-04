#!/usr/bin/env python3
"""
COMPLETE DATA GENERATOR - FINAL VERSION
Uses folder names as JSON keys, but displays data.js names
"""

import json
from pathlib import Path

# Mapping from folder names to display names (for UI)
# Match data.js topic names exactly
DISPLAY_NAMES = {
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
    "Range-Query": "Range Queries",
    "Matrix": "Matrix",
    "Sliding window": "Sliding Window",
    "Maths": "Maths",
    "sorting": "Sorting",
    "prefixSum": "Prefix Sum",
    "google": "Google / Misc",
    "Cyclic Sort": "Cyclic Sort",
}

def read_file(filepath):
    """Read any file safely"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read().strip()
    except:
        return None

def scan_topic(topic_path):
    """Scan a topic folder for problems and notes"""
    result = {
        "problems": [],
        "notes": [],
        "decisionTree": None
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
                # Check if this is a decision tree
                if md_file.name.upper() == "DECISION-TREE.MD":
                    result["decisionTree"] = content
                else:
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

    print("[*] GENERATING COMPLETE DATA (FOLDER NAMES AS KEYS)...\n")

    total_problems = 0
    total_notes = 0

    for folder_name, display_name in sorted(DISPLAY_NAMES.items()):
        topic_path = repo_root / folder_name

        if topic_path.exists():
            data = scan_topic(topic_path)

            all_data[folder_name] = {
                "displayName": display_name,
                "folderName": folder_name,
                "problems": data["problems"],
                "notes": data["notes"],
                "decisionTree": data["decisionTree"]
            }

            total_problems += len(data["problems"])
            total_notes += len(data["notes"])

            print(f"[OK] {folder_name:20} => {display_name:30} : {len(data['problems']):3} problems, {len(data['notes']):2} notes")

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
                cat_data = scan_topic(cat_path)
                dp_categories[display_name] = {
                    "name": display_name,
                    "folder": folder_name,
                    "problems": cat_data["problems"]
                }
                total_problems += len(cat_data["problems"])
                print(f"  [OK] {display_name:35} : {len(cat_data['problems']):2} problems")

        # Update DP entry with categories
        if "DP" in all_data:
            all_data["DP"]["categories"] = dp_categories

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
    print(f"\n[*] JSON Keys (use these in URLs):")
    for key in sorted(data.keys()):
        print(f"    - {key} => {data[key]['displayName']}")
