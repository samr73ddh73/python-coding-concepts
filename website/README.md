# 🎓 Interview Prep Hub - Website

> Your comprehensive interview preparation platform for DSA, LLD, HLD, and Leadership

---

## 📌 Quick Start

### **Option 1: Open in Browser (Recommended)**
1. Navigate to `website/` folder
2. Open `index-new.html` in your browser
3. Or use Live Server in VS Code

### **Option 2: Local Web Server**
```bash
# Python 3.x
python -m http.server 8000 --directory website

# Then visit: http://localhost:8000/index-new.html
```

### **Option 3: Deploy Online**
1. **GitHub Pages:** Push this folder to GitHub and enable Pages
2. **Netlify:** Connect your GitHub repo, set `website/` as public directory
3. **Vercel:** Same as Netlify, can auto-deploy from git

---

## ✨ Features

### **📊 Data Structures & Algorithms**
- 6 core topics: Array, Trees, Graphs, Linked Lists, Binary Search, DP
- 10+ technique topics: Two-Pointer, Sliding Window, Backtracking, etc.
- 89+ problems with complete explanations
- 101 tips and patterns

### **💡 Study Tools**
- **Flashcards** - 101 cards with spaced repetition
- **Decision Trees** - Visual guides to choose algorithms
- **Tips & Tricks** - Essential patterns and optimizations

### **📈 Progress Tracking**
- Track topics viewed
- Monitor problems solved
- Local storage (no server needed)
- Study statistics

### **🎨 Beautiful UI**
- Dark theme with blue/purple accents
- Smooth animations and transitions
- Fully responsive (mobile, tablet, desktop)
- Glassmorphism design

---

## 📁 File Structure

```
website/
├── index-new.html              Main landing page
├── dsa-topic-new.html          Topic detail page (e.g., Array)
├── flashcards.html             Flashcard study system
├── styles-new.css              Main stylesheet
├── topic-style.css             Topic page styles
├── flashcard-style.css         Flashcard styles
├── app-new.js                  Core application logic
├── assets/
│   └── data/
│       ├── dsa.json            DSA topics and problems
│       └── flashcards.json     Flashcard data
├── README.md                   This file
├── INTEGRATION-GUIDE.md        Technical integration details
├── DESIGN-GUIDE.md             Design documentation
└── FIXES-APPLIED.md            Previous fixes documentation
```

---

## 🚀 Key Features Explained

### **1. Dynamic Data Loading**
- `app-new.js` loads `assets/data/dsa.json`
- Falls back to hardcoded data if JSON unavailable
- Automatically populates all cards and content

### **2. Topic Routing**
- Click "Explore" on any topic → loads correct topic page
- URL parameter: `dsa-topic-new.html?topic=array`
- Each topic shows its own problems, tips, and decision tree

### **3. Progress Tracking**
- Every topic view is saved to browser localStorage
- No server needed, everything works offline
- Progress persists across page reloads

### **4. Search & Filter**
- Search box filters topics in real-time
- Case-insensitive matching
- Works on mobile and desktop

---

## 🔌 How It Works

### **Data Flow:**
```
dsa.json (data source)
    ↓
app-new.js (loads and manages data)
    ↓
Landing Page (displays topics)
    ↓
Topic Page (shows problems & solutions)
    ↓
localStorage (saves progress)
```

### **Each Page:**
1. **Landing (index-new.html)**
   - Shows all 6 core topics + techniques
   - Search and filter options
   - Links to resources (Flashcards, etc.)

2. **Topic Detail (dsa-topic-new.html)**
   - Reads URL parameter: `?topic=array`
   - Loads correct topic from JSON
   - Shows problems, tips, decision tree
   - Beautiful modal for solutions

3. **Flashcards (flashcards.html)**
   - 3D flip animation
   - Progress tracking
   - Category and difficulty filters

---

## 🛠️ JavaScript API

All functionality is available through the global `app` object:

```javascript
// Check if app is loaded
if (window.app) {
  
  // Get statistics
  const stats = window.app.getProgressStats();
  console.log(stats.totalProblems); // 89
  console.log(stats.topicsViewed);  // 2 (e.g.)

  // Get all topics
  const topics = window.app.getTopics();

  // Get single topic
  const arrayTopic = window.app.getTopic('array');

  // Track progress
  window.app.markTopicViewed('trees');
  window.app.markProblemSolved('1-move-zeros.py');

  // Check progress
  if (window.app.progress.topicsViewed.includes('array')) {
    // Mark as completed
  }
}
```

---

## 🎯 Navigation

| Page | URL | Purpose |
|------|-----|---------|
| Landing | `index-new.html` | Main entry point |
| Array Topic | `dsa-topic-new.html?topic=array` | Array problems & tips |
| Trees Topic | `dsa-topic-new.html?topic=trees` | Tree algorithms |
| Graphs Topic | `dsa-topic-new.html?topic=graph` | Graph algorithms |
| Linked Lists | `dsa-topic-new.html?topic=linkedlist` | Linked list patterns |
| Binary Search | `dsa-topic-new.html?topic=binarysearch` | BS variations |
| Dynamic Prog. | `dsa-topic-new.html?topic=dp` | DP problems |
| Flashcards | `flashcards.html` | Study system |

---

## 🌐 Deployment Instructions

### **Deploy to GitHub Pages:**
1. Create GitHub repository
2. Push `website/` folder
3. Go to Settings → Pages
4. Select branch and `/root` folder
5. Wait for deployment
6. Access at `https://username.github.io/python-coding-concepts/website/`

### **Deploy to Netlify:**
1. Connect GitHub repository
2. Build settings:
   - Base directory: `website`
   - No build command needed
3. Deploy
4. Custom domain (optional)

### **Deploy to Vercel:**
1. Import from GitHub
2. Root directory: `website`
3. Framework: None (static)
4. Deploy
5. Auto-redeploys on push

---

## 💾 Data Format

### **JSON Structure (dsa.json):**
```json
{
  "version": "1.0",
  "lastUpdated": "2026-07-01",
  "topics": [
    {
      "id": "array",
      "name": "Array",
      "problems": [
        {
          "name": "1-move-zeros.py",
          "path": "Array/1-move-zeros.py",
          "type": "implementation"
        }
      ],
      "tips": [ /* ... */ ],
      "decisionTree": null
    }
  ]
}
```

### **Local Storage (automatic):**
```json
{
  "topicsViewed": ["array", "trees"],
  "problemsSolved": ["1-move-zeros.py"],
  "lastVisit": "2026-07-01T10:30:00Z",
  "flashcardsLearned": []
}
```

---

## 🐛 Troubleshooting

### **Pages not loading CSS?**
- Clear browser cache: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
- Verify CSS files are in same directory as HTML

### **Data not showing?**
- Check browser console (F12 → Console)
- Verify `assets/data/dsa.json` exists
- Look for fetch errors in Network tab

### **Progress not saving?**
- localStorage should work by default
- Check if browser is in private/incognito mode
- Verify not out of storage quota

### **Links not working?**
- Verify filenames match exactly (case-sensitive)
- Check URL parameters: `?topic=array`
- Test in different browser

---

## 🎨 Customization

### **Change Colors:**
Edit `styles-new.css` and modify CSS variables:
```css
:root {
  --bg-primary: #0F1419;        /* Main background */
  --accent-primary: #3B82F6;    /* Main blue */
  --accent-secondary: #8B5CF6;  /* Purple accent */
}
```

### **Change Fonts:**
Update font imports in HTML `<head>`:
```html
<link href="https://fonts.googleapis.com/css2?family=YourFont:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### **Add More Topics:**
1. Add to `dsa.json` in same format
2. Update `app-new.js` topic icons/descriptions if needed
3. Links auto-generate for new topics

---

## 🔐 Privacy & Security

- **No tracking** - No analytics or external services
- **No cookies** - Only localStorage for user progress
- **No login** - Everything works locally
- **Works offline** - Static files, no server needed
- **Open source** - All code visible and customizable

---

## 📚 Additional Resources

- **INTEGRATION-GUIDE.md** - Technical implementation details
- **DESIGN-GUIDE.md** - Design system and component library
- **FIXES-APPLIED.md** - Previous bug fixes and improvements

---

## ✅ Checklist for First Launch

- [ ] Open `index-new.html` in browser
- [ ] Click "Get Started" → lands on DSA section
- [ ] Click "Explore" on Array topic → opens Array page
- [ ] Click "View Solution" on a problem → modal appears
- [ ] Press Escape → modal closes
- [ ] Use search box to filter topics
- [ ] Click Flashcards → opens flashcard system
- [ ] Refresh page → progress persists

---

## 🚀 Production Ready

✅ All files are static (no backend needed)  
✅ Optimized for performance  
✅ Mobile responsive  
✅ Accessible (keyboard navigation)  
✅ SEO friendly  
✅ Fast loading times  
✅ Works offline (cached)  

---

## 📧 Support

For issues or questions:
1. Check browser console (F12)
2. Review INTEGRATION-GUIDE.md
3. Check FIXES-APPLIED.md for common issues
4. Contact through GitHub issues

---

**Status:** ✅ **FULLY FUNCTIONAL**  
**Last Updated:** 2026-07-01  
**Version:** 1.0

Ready to deploy! 🎉
