#!/usr/bin/env python3
"""
Build script to convert markdown notes and Python code into JavaScript data structure.
This scans the repo for all .md files and Python files, organizes by directory,
and generates notes-data.js and code-data.js for the website.
"""

import os
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Root directory of the project
REPO_ROOT = Path(__file__).parent.parent
TOPICS_DIR = REPO_ROOT / "topics"

# Directory name to topic name mapping
DIRECTORY_MAPPING = {
    'Fundamentals': 'Fundamentals',
    'Array': 'Arrays',
    'Arrays': 'Arrays',
    'BinarySearch': 'Binary Search',
    'Binary Search': 'Binary Search',
    'LinkedList': 'Linked Lists',
    'Linked Lists': 'Linked Lists',
    'Trees': 'Trees',
    'Tree': 'Trees',
    'Graph': 'Graphs',
    'Graphs': 'Graphs',
    'DP': 'Dynamic Programming',
    'Dynamic Programming': 'Dynamic Programming',
    'Backtracking': 'Backtracking',
    'Strings': 'Strings',
    'String': 'Strings',
    'Sliding window': 'Sliding Window',
    'Sliding_window': 'Sliding Window',
    'Cyclic Sort': 'Cyclic Sort',
    'Cyclic_sort': 'Cyclic Sort',
    'Cyclic_Sort': 'Cyclic Sort',
    'BitManipulation': 'Bit Manipulation',
    'Bit Manipulation': 'Bit Manipulation',
    'Heap': 'Heap',
    'Heaps': 'Heap',
    'Maps': 'Maps & Hashmaps',
    'Maths': 'Mathematics',
    'Math': 'Mathematics',
    'LLD': 'Low Level Design',
    'System Design Notes': 'System Design',
    'Data Structures Internals': 'Data Structures',
}

# Parent directories that should group their subdirectories
PARENT_GROUPS = {
    'DP': 'Dynamic Programming',
}

# Exclude these directories from scanning
EXCLUDE_DIRS = {'.git', '.vscode', '.claude', '__pycache__', 'website', 'node_modules', '.pytest_cache'}

def read_file(filepath):
    """Read file content safely."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return None

def get_topic_name(directory_name):
    """Convert directory name to topic name."""
    # Direct mapping if exists
    if directory_name in DIRECTORY_MAPPING:
        return DIRECTORY_MAPPING[directory_name]

    # Try with spaces
    spaced = directory_name.replace('_', ' ').replace('-', ' ')
    if spaced in DIRECTORY_MAPPING:
        return DIRECTORY_MAPPING[spaced]

    # Try with title case
    titled = directory_name.replace('_', ' ').replace('-', ' ').title()
    if titled in DIRECTORY_MAPPING:
        return DIRECTORY_MAPPING[titled]

    # Default: title case
    return titled

def should_group_under_parent(parts, index):
    """Check if directory at index should be grouped under parent(s)."""
    # Check if any ancestor is in PARENT_GROUPS
    for i in range(index - 1, -1, -1):
        if parts[i] in PARENT_GROUPS:
            return True, i
    return False, -1

def get_grouped_topic_name(parts, current_index):
    """Get topic name for a nested directory that should be grouped."""
    should_group, parent_index = should_group_under_parent(parts, current_index)
    if should_group and parent_index >= 0:
        parent_topic = PARENT_GROUPS[parts[parent_index]]
        # Get all parts between parent and current for full path
        subpath = ' > '.join(parts[parent_index + 1:current_index + 1])
        return f"{parent_topic} > {subpath}"
    return get_topic_name(parts[current_index])

def scan_all_markdown():
    """Scan entire repo for ALL markdown files, organized by directory."""
    topics_data = defaultdict(lambda: defaultdict(str))

    for md_file in REPO_ROOT.rglob('*.md'):
        # Skip website directory
        if 'website' in md_file.parts or '.git' in md_file.parts:
            continue

        # Get all directory parts
        relative_parts = list(md_file.parent.relative_to(REPO_ROOT).parts)
        if not relative_parts:
            continue

        # Find relevant directory (skip parent directories that are generic)
        parent_dir = md_file.parent.name
        if not parent_dir or parent_dir in EXCLUDE_DIRS:
            continue

        # Check if this should be grouped
        should_group, parent_idx = should_group_under_parent(relative_parts, len(relative_parts) - 1)

        if should_group and parent_idx >= 0:
            topic_name = get_grouped_topic_name(relative_parts, len(relative_parts) - 1)
        else:
            topic_name = get_topic_name(parent_dir)

        # Get section from filename
        filename = md_file.stem.lower()

        # Determine section type
        section = 'content'
        if 'theory' in filename or 'note' in filename or filename.startswith('0'):
            section = 'theory'
        elif 'pattern' in filename:
            section = 'patterns'
        elif 'question' in filename or 'problem' in filename:
            section = 'questions'
        elif 'trick' in filename or 'gotcha' in filename:
            section = 'tricks'

        content = read_file(md_file)
        if not content:
            continue

        # Append to section (allow multiple files per section)
        if topics_data[topic_name][section]:
            topics_data[topic_name][section] += "\n\n---\n\n"

        topics_data[topic_name][section] += content

    return dict(topics_data)

def scan_all_python_code():
    """Scan repo for Python files with code examples."""
    code_data = defaultdict(list)

    for py_file in REPO_ROOT.rglob('*.py'):
        # Skip website and test files
        if 'website' in py_file.parts or '__pycache__' in py_file.parts:
            continue
        if py_file.name.startswith('test_') or py_file.name.startswith('build_'):
            continue

        # Get all directory parts
        relative_parts = list(py_file.parent.relative_to(REPO_ROOT).parts)
        if not relative_parts:
            continue

        # Find relevant directory
        parent_dir = py_file.parent.name
        if not parent_dir or parent_dir in EXCLUDE_DIRS:
            continue

        # Check if this should be grouped
        should_group, parent_idx = should_group_under_parent(relative_parts, len(relative_parts) - 1)

        if should_group and parent_idx >= 0:
            topic_name = get_grouped_topic_name(relative_parts, len(relative_parts) - 1)
        else:
            topic_name = get_topic_name(parent_dir)

        content = read_file(py_file)
        if not content:
            continue

        # Extract docstring and first few lines
        lines = content.split('\n')
        docstring = ''
        code = content

        # Try to extract docstring
        if lines and (lines[0].startswith('"""') or lines[0].startswith("'''")):
            quote_type = lines[0][:3]
            docstring_lines = [lines[0]]
            for i, line in enumerate(lines[1:], 1):
                docstring_lines.append(line)
                if quote_type in line:
                    docstring = '\n'.join(docstring_lines)
                    code = '\n'.join(lines[i+1:])
                    break

        code_data[topic_name].append({
            'filename': py_file.name,
            'path': str(py_file.relative_to(REPO_ROOT)),
            'docstring': docstring[:200],  # First 200 chars
            'code': code[:500],  # First 500 chars
            'full_code': code,
        })

    return dict(code_data)

def generate_notes_javascript(topics_data):
    """Generate JavaScript code for notes-data.js."""
    js_content = """// Generated by build_notes.py - DO NOT EDIT MANUALLY
// Run: python website/build_notes.py to regenerate

const NOTES_DATA = {
"""

    for topic in sorted(topics_data.keys()):
        sections = topics_data[topic]
        js_content += f'    "{topic}": {{\n'

        for section, content in sections.items():
            escaped_content = json.dumps(content)
            js_content += f'        {section}: {escaped_content},\n'

        js_content = js_content.rstrip(',\n') + '\n'
        js_content += '    },\n'

    js_content = js_content.rstrip(',\n') + '\n'
    js_content += '};\n'

    return js_content

def generate_code_javascript(code_data):
    """Generate JavaScript code for code-data.js."""
    js_content = """// Generated by build_notes.py - DO NOT EDIT MANUALLY
// Run: python website/build_notes.py to regenerate

const CODE_DATA = {
"""

    for topic in sorted(code_data.keys()):
        files = code_data[topic]
        js_content += f'    "{topic}": [\n'

        for file_info in files:
            js_content += '        {\n'
            js_content += f'            filename: {json.dumps(file_info["filename"])},\n'
            js_content += f'            path: {json.dumps(file_info["path"])},\n'
            js_content += f'            docstring: {json.dumps(file_info["docstring"])},\n'
            js_content += f'            preview: {json.dumps(file_info["code"])},\n'
            js_content += f'            full_code: {json.dumps(file_info["full_code"])},\n'
            js_content += '        },\n'

        js_content = js_content.rstrip(',\n') + '\n'
        js_content += '    ],\n'

    js_content = js_content.rstrip(',\n') + '\n'
    js_content += '};\n'

    return js_content

def main():
    """Main build process."""
    print("🔨 Building DSA notes and code data...\n")

    # Scan all markdown files
    print("📝 Scanning markdown files...")
    topics_data = scan_all_markdown()
    total_files = sum(1 for _ in REPO_ROOT.rglob('*.md')
                     if 'website' not in str(_) and '.git' not in str(_))
    print(f"   Found {total_files} markdown files")
    print(f"   Organized into {len(topics_data)} topics\n")

    # Scan all Python code
    print("🐍 Scanning Python code files...")
    code_data = scan_all_python_code()
    total_py_files = sum(len(files) for files in code_data.values())
    print(f"   Found {total_py_files} Python files")
    print(f"   Organized into {len(code_data)} topics\n")

    # Generate JavaScript files
    print("⚙️  Generating JavaScript data files...\n")

    # Notes data
    notes_js = generate_notes_javascript(topics_data)
    notes_file = Path(__file__).parent / "notes-data.js"
    with open(notes_file, 'w', encoding='utf-8') as f:
        f.write(notes_js)
    print(f"✅ Generated {notes_file.name}")

    # Code data
    code_js = generate_code_javascript(code_data)
    code_file = Path(__file__).parent / "code-data.js"
    with open(code_file, 'w', encoding='utf-8') as f:
        f.write(code_js)
    print(f"✅ Generated {code_file.name}\n")

    # Summary
    print("📊 COVERAGE SUMMARY:\n")
    print("NOTES BY TOPIC:")
    for topic in sorted(topics_data.keys()):
        sections = list(topics_data[topic].keys())
        print(f"   {topic}: {', '.join(sections)}")

    print("\nCODE FILES BY TOPIC:")
    for topic in sorted(code_data.keys()):
        count = len(code_data[topic])
        print(f"   {topic}: {count} files")
        for file_info in code_data[topic][:3]:  # Show first 3 files
            print(f"      - {file_info['filename']}")
        if count > 3:
            print(f"      ... and {count - 3} more")

    print("\n" + "="*50)
    print(f"Total Topics: {len(set(list(topics_data.keys()) + list(code_data.keys())))}")
    print(f"Total Markdown Files: {total_files}")
    print(f"Total Python Files: {total_py_files}")
    print("="*50)

if __name__ == '__main__':
    main()
