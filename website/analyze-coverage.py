#!/usr/bin/env python3
"""
Compare website coverage vs repo inventory
"""

import json

# Load inventory
with open('complete-problem-inventory.json', 'r') as f:
    inventory = json.load(f)

# Website problem counts (from manual inspection of dsa-topic-new.html)
website_counts = {
    "Array": 5,
    "Trees": 4,  # Max Depth, Check Balanced, Diameter, Level Order
    "Graph": 4,  # DFS, BFS, Cycle Detection, Topological Sort
    "LinkedList": 4,  # Reverse, Detect Cycle, Find Cycle Start, Remove Nth
    "BinarySearch": 4,  # Binary Search, Rotated Array, Peak Element, Find Min
    "DP": 4  # Fibonacci, Coin Change, Unique Paths, LCS
}

print("=" * 70)
print("PROBLEM COVERAGE: WEBSITE vs REPO")
print("=" * 70)

topics_to_check = ["Trees", "Graph", "DP"]

for topic in topics_to_check:
    repo_count = inventory[topic]["problem_count"]

    if topic == "DP" and "categories" in inventory[topic]:
        # Count nested DP
        nested_count = sum(cat["problem_count"] for cat in inventory[topic]["categories"].values())
        total_repo = repo_count + nested_count
    else:
        total_repo = repo_count

    website_count = website_counts.get(topic, 0)
    coverage = (website_count / total_repo * 100) if total_repo > 0 else 0

    print(f"\n{topic.upper()}:")
    print(f"  Repo:     {total_repo} problems")
    print(f"  Website:  {website_count} problems")
    print(f"  Coverage: {coverage:.1f}%")
    print(f"  Missing:  {total_repo - website_count} problems")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

total_repo = (inventory["Trees"]["problem_count"] +
              inventory["Graph"]["problem_count"] +
              inventory["DP"]["problem_count"] +
              sum(cat["problem_count"] for cat in inventory["DP"].get("categories", {}).values()))

total_website = sum(website_counts.get(t, 0) for t in topics_to_check)

print(f"\nThese 3 topics combined:")
print(f"  Repo total:     {total_repo} problems")
print(f"  Website total:  {total_website} problems")
print(f"  Coverage:       {(total_website/total_repo*100):.1f}%")
