#!/usr/bin/env python3
"""
COMPLETE DATA GENERATOR
Reads ALL problems and notes from repo
Outputs master JSON for website
"""

import json
from pathlib import Path

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

    topics = [
        "Array", "Trees", "Graph", "LinkedList", "BinarySearch",
        "DP", "Backtracking", "Greedy", "BitManipulation", "Heap",
        "Maps", "Strings", "Recursion", "DP", "MergeIntervals",
        "Range-Query", "Matrix", "Sliding window"
    ]

    print("[*] GENERATING COMPLETE DATA...\n")

    total_problems = 0
    total_notes = 0

    for topic_name in sorted(set(topics)):
        topic_path = repo_root / topic_name

        if topic_path.exists():
            data = scan_topic(topic_path)

            all_data[topic_name] = {
                "name": topic_name,
                "problems": data["problems"],
                "notes": data["notes"]
            }

            total_problems += len(data["problems"])
            total_notes += len(data["notes"])

            print(f"[OK] {topic_name:20} : {len(data['problems']):3} problems, {len(data['notes']):2} notes")

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
    print(f"\n[*] Website can now load:")
    print(f"    - All 127+ problems")
    print(f"    - All 40 notes")
    print(f"    - DP with 5 categories")
