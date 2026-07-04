# 📱 Phase 1 Testing Guide

## ✅ What's Ready to Test

### Desktop First
1. Open PowerShell in `website/` folder
2. Run: `python -m http.server 8000`
3. Go to: `http://localhost:8000/index-new.html`

### Test Checklist:
- [ ] Click "Explore" on Array → page loads
- [ ] Click "View Code" on a problem → code displays in modal with syntax highlighting
- [ ] Code is fully readable (not cut off)
- [ ] Click note in sidebar → markdown renders as formatted HTML (not raw text)
- [ ] Press Escape → modal closes
- [ ] Click other nav buttons (Patterns, Tips, Problems, Decision Tree)
- [ ] F12 Console → no errors

### Then Test on Phone
1. Find your computer's IP: run `ipconfig` in PowerShell
2. On phone browser: `http://[YOUR_IP]:8000/index-new.html`

### Phone Checklist:
- [ ] Page loads and is readable
- [ ] Code blocks scroll horizontally (don't break layout)
- [ ] Modal fits on screen
- [ ] Navigation buttons work
- [ ] Notes render properly (formatted, not raw markdown)
- [ ] Text is large enough
- [ ] No layout breaks

---

## 🎯 Phase 1 Accomplishments

✅ **Markdown Rendering** - md-renderer.js converts markdown to HTML
✅ **Code Display** - Syntax highlighting, proper scrolling, mobile-friendly
✅ **Mobile Optimization** - Responsive grid, flexible fonts, touch-friendly
✅ **Modal Handling** - Works on all screen sizes
✅ **Foundation CSS** - enhanced.css for all styling

---

## 📋 Current Content Status

### Embedded in Website:
- Array (5 problems, 3 patterns, notes)
- Trees (4 problems, 3 patterns, notes)
- Graph (4 problems, 3 patterns, notes)
- LinkedList (3 problems, 3 patterns, notes)
- BinarySearch (4 problems, 3 patterns, notes)
- DP (4 problems, 3 patterns, notes)

### Missing (Phase 2):
- Backtracking full page (have notes, need dedicated page)
- Greedy full page (have notes, need dedicated page)
- Bit Manipulation full page (need notes + page)
- Heap full page (need notes + page)
- DP detailed hierarchy (Knapsack, LCS, MCM, etc.)
- All Graph/DP problems from repo

---

## 🚀 Phase 2 Plan (After Testing)

### Week 1 - Additional Topics:
1. Create /technique-backtracking.html
2. Create /technique-greedy.html
3. Create /technique-bitmanip.html
4. Create /technique-heap.html
5. Embed ALL notes from repo into each

### Week 2 - DP Hierarchy:
1. Add DP subfolder navigation (0-1-Knapsack, LCS, MCM, etc.)
2. Load ALL problems from each subfolder
3. Use proper DECISION-TREE.md from repo

### Week 3 - Final Polish:
1. Add flashcards with templates
2. Full testing on all devices
3. Deployment prep

---

## 📞 If Issues on Phone:

**Code block overflows?**
- Browser refresh (Ctrl+Shift+R on desktop, or force refresh on phone)
- Or resize browser window

**Notes show raw markdown?**
- Refresh page
- Check browser console (F12) for errors

**Modal doesn't fit?**
- Should auto-resize - try refreshing
- Test on different phone sizes

---

## ✨ Report Back With:

1. What works well on phone
2. What doesn't render properly
3. Any layout issues
4. Font size feedback
5. Speed/loading time

Then we'll tackle Phase 2 with full notes and problems!

---

**Current Status: Phase 1 Foundation Complete ✅**
**Next: Test on Phone 📱**
