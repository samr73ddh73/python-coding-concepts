# ⚡ Quick Reference Card

## Open the Website
```
Double-click: website/dsa-complete.html
```
That's it! Your notes load automatically.

---

## To Update Notes

### Step 1: Edit or Add Notes
Create/edit markdown files in `topics/[topic-name]/`:
```
topics/
├── arrays/
│   ├── theory.md
│   ├── patterns.md
│   └── ...
├── linked-lists/
│   └── ...
```

### Step 2: Run Build Script
```bash
cd website
python build_notes.py
```

### Step 3: Refresh Browser
Press `Ctrl+F5` (hard refresh) to see changes.

---

## Website Structure

### Sidebar (Left)
- Click topic name to load that topic
- Active topic is highlighted in blue

### Section Buttons (Top Right)
- 📖 **Theory** — Your theory notes
- 🎯 **Patterns** — Pattern explanations + code
- ❓ **Questions** — Practice problems
- ⚡ **Tricks** — Common gotchas
- 🎓 **Flashcards** — Test yourself

### Content Area (Center)
- Shows markdown content with proper formatting
- Tables, code blocks, lists all styled
- Click on flashcard to flip

---

## Current Topics Available

```
✅ Arrays
✅ Backtracking
✅ Binary Search
✅ Dynamic Programming
✅ Graphs
✅ Trees
```

To add more: Create `topics/[new-topic]/` directory

---

## File Format Reference

### For theory.md:
```markdown
# Topic Theory

## Core Concepts
...

## Time Complexity
| Op | Time | Space |
|----|------|-------|

## Key Points
- Point 1
```

### For patterns.md:
```markdown
## Pattern: Name

**When to use:** Description

**Code:**
\`\`\`python
code here
\`\`\`

**Complexity:** O(...)
```

### For questions.md:
```markdown
## Easy
- LC 1: Name

## Medium
- LC 2: Name

## Hard
- LC 3: Name
```

### For tricks.md:
```markdown
## Trick: Name
**Trap:** What goes wrong
**Solution:** How to fix
**Example:** Code
```

---

## Common Commands

### Build notes (after editing)
```bash
cd website && python build_notes.py
```

### Start local server (optional)
```bash
cd website && python -m http.server 8000
# Visit: http://localhost:8000/dsa-complete.html
```

### View generated data
```bash
# Check size
ls -lh website/notes-data.js

# Check what's in it
grep -c "theory" website/notes-data.js
```

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+F5` | Hard refresh website |
| `F12` | Open browser console (for debugging) |
| `Escape` | Close flashcard (if flipped) |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Website blank | Refresh (Ctrl+F5), check console (F12) |
| Notes don't appear | Run build script, refresh |
| Old content showing | Hard refresh (Ctrl+F5) |
| Formatting wrong | Check markdown syntax in .md file |
| Topics missing | Make sure .md file exists, run build |

---

## File Locations

```
website/
├── dsa-complete.html       ← OPEN THIS FILE
├── notes-data.js           ← AUTO-GENERATED (don't edit)
├── build_notes.py          ← Run this after editing notes
├── SETUP-GUIDE.md          ← Full setup guide
├── QUICK-REFERENCE.md      ← This file
└── ...

topics/
├── arrays/
│   ├── theory.md
│   ├── patterns.md
│   ├── questions.md        ← Optional
│   └── tricks.md           ← Optional
├── [other topics]/
└── ...
```

---

## Progress Flow

```
1. Add/Edit notes
   ↓
2. Run: python website/build_notes.py
   ↓
3. Refresh browser (Ctrl+F5)
   ↓
4. See your changes!
```

---

## Tips

✨ **Keep your notes clean** — Well-formatted markdown renders beautifully

✨ **Use code blocks** — Wrap code in triple backticks for syntax highlighting

✨ **Use tables** — Complex info looks great in tables

✨ **Regular updates** — Run build script regularly as you add content

✨ **Mobile friendly** — Check on phone/tablet for responsive design

---

## Deploy (Optional)

### GitHub Pages:
```bash
git add website/
git commit -m "update notes"
git push
```

### Netlify:
Drag `website/` folder to Netlify dashboard

---

**Remember:** Open `website/dsa-complete.html` and start studying! 🚀
