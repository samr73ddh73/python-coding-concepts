#!/usr/bin/env python3
"""
Compare notes coverage: website vs repo
"""

import json

# Load inventory
with open('complete-problem-inventory.json', 'r') as f:
    inventory = json.load(f)

# Website notes coverage (from inspection of dsa-topic-new.html)
# Counting unique note names embedded in the HTML
website_notes = {
    "Array": ["Two-Pointer Pattern", "Sliding Window"],  # 2 notes
    "Trees": ["Tree Traversals"],  # 1 note
    "Graph": ["Graph Patterns"],  # 1 note
    "LinkedList": ["Floyd's Algorithm"],  # 1 note
    "BinarySearch": ["Binary Search Patterns"],  # 1 note
    "DP": ["DP Fundamentals", "DP on Grids"],  # 2 notes
}

print("=" * 70)
print("NOTES COVERAGE: WEBSITE vs REPO")
print("=" * 70)

total_repo_notes = 0
total_website_notes = 0

for topic in sorted(inventory.keys()):
    if inventory[topic]["note_count"] > 0:
        repo_notes = inventory[topic]["note_count"]
        website_notes_count = len(website_notes.get(topic, []))

        total_repo_notes += repo_notes
        total_website_notes += website_notes_count

        coverage = (website_notes_count / repo_notes * 100) if repo_notes > 0 else 0

        print(f"\n{topic}:")
        print(f"  Repo:     {repo_notes} notes")
        print(f"  Website:  {website_notes_count} notes")
        print(f"  Coverage: {coverage:.1f}%")
        if repo_notes > website_notes_count:
            print(f"  Missing:  {repo_notes - website_notes_count} notes [MISSING]")

            # Show what's missing
            if topic in inventory and inventory[topic]["notes"]:
                embedded = website_notes.get(topic, [])
                print(f"    Repo has: {inventory[topic]['notes']}")
                print(f"    Embedded: {embedded}")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print(f"\nAll topics combined:")
print(f"  Repo total:     {total_repo_notes} note files")
print(f"  Website total:  {total_website_notes} notes embedded")
print(f"  Coverage:       {(total_website_notes/total_repo_notes*100):.1f}%")
print(f"  Missing:        {total_repo_notes - total_website_notes} notes [MISSING]")

print(f"\n[BREAKDOWN BY TOPIC]")
topics_with_notes = [(t, inventory[t]["note_count"]) for t in inventory if inventory[t]["note_count"] > 0]
topics_with_notes.sort(key=lambda x: x[1], reverse=True)

for topic, count in topics_with_notes:
    embedded = len(website_notes.get(topic, []))
    status = "[OK]" if embedded == count else "[MISSING]"
    print(f"  {topic:20} : {count:2} in repo, {embedded:2} on website {status}")
