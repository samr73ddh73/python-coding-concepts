# 🎨 Interview Prep Hub — Design Guide

> Modern, clean design for interview preparation platform

---

## Design Overview

We've created a completely fresh, professional design focused on:
- **Clean Typography** - Clear hierarchy with Geist font
- **Dark Mode** - Easier on eyes, modern aesthetic
- **Minimal Colors** - Blue accent (#3B82F6) with purple secondary (#8B5CF6)
- **Card-Based Layout** - Scannable, organized content
- **Excellent UX** - Intuitive navigation, smooth interactions
- **Fully Responsive** - Works on mobile, tablet, desktop

---

## Pages Created

### 1. **index-new.html** - Landing Page
**Purpose:** Entry point to the entire platform

**Sections:**
- **Navbar** - Sticky navigation with logo and section links
- **Hero Section** - Eye-catching intro with call-to-action
  - Title: "Master Your Interviews"
  - 3 floating stat cards (89 Problems, 101 Tips, 17 Topics)
  - Get Started button
  
- **DSA Section** - Main content area
  - 6 Core Topics (cards with large icons)
    - Array, Trees, Graphs, Linked Lists, Binary Search, Dynamic Programming
  - 10+ Technique Topics (smaller cards)
    - Two-Pointer, Sliding Window, Backtracking, Greedy, etc.
  - Study Resources (3 cards: Flashcards, Decision Trees, Tips)
  
- **Coming Soon Sections**
  - LLD (Low-Level Design)
  - HLD (High-Level Design)
  - Leadership & Behavioral

- **Footer** - Simple, clean footer

**Design Features:**
- Grid layout for topics (responsive 1-3 columns)
- Color-coded badges (Core, Pattern, etc.)
- Hover effects on cards (lift + shadow)
- Smooth scrolling between sections

---

### 2. **dsa-topic.html** - Topic Detail Page
**Purpose:** Detailed view of a specific topic (e.g., Array)

**Layout:**
- **Top Section** - Hero with topic info
  - Back button, topic icon, title, description
  - Statistics (# problems, # tips)
  
- **Two-Column Layout** (responsive)
  - **Left Sidebar** - Navigation menu
    - Overview, Tips & Patterns, Problems, Decision Tree
    - Sticky positioning
    - Active indicator on current section
  
  - **Right Content Area** - Displays selected section
    - **Overview** - Quick reference cards
      - Core Patterns
      - Key Concepts
      - When to Use
    
    - **Tips & Patterns** - Card grid
      - Pattern tips
      - Important insights
      - Tricks and optimizations
      - Each card shows: label, title, description, complexity
    
    - **Problems** - Card grid of all problems
      - Problem name
      - Difficulty badge (Easy/Medium/Hard)
      - Short description
      - Pattern tags
      - View Solution button
    
    - **Decision Tree** - How to choose algorithms
      - Visual tree structure
      - When-to-use guide

**Design Features:**
- Sticky sidebar navigation
- Smooth section transitions
- Color-coded difficulty badges
- Pattern tag system
- Hover effects on all interactive elements

---

### 3. **flashcards.html** - Flashcard Study System
**Purpose:** Spaced repetition learning through flashcards

**Layout:**
- **Header** - Title and description

- **Filter Section** - Control which cards to study
  - Category dropdown (All Topics, Arrays, Trees, etc.)
  - Difficulty dropdown (All Levels, Beginner, Intermediate, Advanced)
  - Search input
  - All filters in one sticky bar

- **Card Display** - Main flashcard
  - Large clickable card (400px height)
  - Front side: question with category label
  - Back side: answer (revealed on click)
  - Smooth flip animation
  - Navigation: Previous / Card Count / Next buttons
  - Progress bar showing position in deck

- **Statistics Section** - Track progress
  - 4 stat cards showing:
    - Cards Studied
    - Correct Answers
    - Mastered Cards
    - Study Streak

- **Study Tips Section** - 4 numbered tips
  - Regular Review
  - Active Recall
  - Spaced Repetition
  - Mix Topics

**Design Features:**
- 3D flip animation on cards
- Progress visualization
- Keyboard shortcuts (← → Space)
- Smooth transitions
- Clear visual hierarchy

---

## Color Palette

```
Primary Background:  #0F1419 (very dark blue)
Secondary BG:        #1A1F2E (dark blue-gray)
Tertiary BG:         #252D3D (slightly lighter)
Hover BG:            #2A3142 (light on hover)

Text Primary:        #FFFFFF (white)
Text Secondary:      #B4B8BF (light gray)
Text Muted:          #7A7E85 (medium gray)

Accent Primary:      #3B82F6 (bright blue)
Accent Secondary:    #8B5CF6 (purple)
Accent Light:        #60A5FA (light blue)

Success:             #10B981 (green)
Warning:             #F59E0B (orange)
Danger:              #EF4444 (red)
```

---

## Typography

- **Font Family:** -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif
- **Mono Font:** 'JetBrains Mono'

### Heading Sizes
- H1: 48px (hero), 36px (section), 28px (page)
- H2: 28px, 20px (subsections)
- H3: 18px, 16px (card titles)
- H4: 16px (sub-content)

### Text Sizes
- Body: 14-16px
- Labels: 12-14px
- Small: 13px

---

## Component Library

### Buttons
- **Primary Button** - Gradient background, hover lift effect
- **Card Button** - Ghost style, border + accent color
- **Control Button** - Flex layout with icon spacing
- **Filter Button** - Consistent styling across filters

### Cards
- **Topic Card** - Grid item with icon, title, meta, skills, CTA
- **Tip Card** - Color-coded label, title, description
- **Problem Card** - Header with difficulty badge, description, tags
- **Stat Card** - Number + label, hover effect
- **Resource Card** - Large icon, title, description

### Tags & Badges
- **Pattern Tag** - Small blue background
- **Difficulty Badge** - Color-coded (green/orange/red)
- **Category Badge** - Purple background
- **Skill Tag** - Blue background

### Layout System
- **Grid Columns**
  - Auto-fit minmax (280px-320px on desktop)
  - Single column on mobile
  - Gap: 16px-24px

- **Spacing Scale**
  - xs: 4px, sm: 8px, md: 16px, lg: 24px, xl: 32px, 2xl: 48px

- **Border Radius**
  - sm: 6px, md: 10px, lg: 16px, xl: 24px

---

## Animations

- **Transitions** - 0.2s cubic-bezier(0.4, 0, 0.2, 1)
- **Slow Transitions** - 0.4s (for larger movements)
- **Flip Animation** - 0.6s (for flashcards)
- **Float Animation** - 6s infinite (hero cards)
- **Heartbeat** - 1.5s infinite (footer heart)

### Hover Effects
- Transform: translateY(-2px to -4px)
- Box-shadow: Various levels
- Border color: Accent on hover
- Background: Slight brightening

---

## Responsive Design

### Breakpoints
- **Desktop:** Full grid layouts, sidebars visible
- **Tablet:** Adjusted grids (2 columns where needed)
- **Mobile:** Single column, stacked navigation

### Key Adaptations
- Navbar: Vertical navigation on mobile
- Hero: Single column, no visual section
- Topic Page: Sidebar becomes horizontal
- Flashcards: All controls stack
- Grids: 1 column on mobile

---

## File Structure

```
website/
├── index-new.html           Landing page
├── dsa-topic.html           Topic detail page  
├── flashcards.html          Flashcard study system
├── styles-new.css           Main styles (shared)
├── topic-style.css          Topic page specific styles
├── flashcard-style.css      Flashcard page specific styles
├── assets/
│   └── data/
│       ├── dsa.json         Topic data
│       └── flashcards.json  Flashcard data
└── (old files kept for reference)
```

---

## Features by Page

### Landing Page
- ✅ Sticky navbar with section navigation
- ✅ Hero section with floating cards
- ✅ Topic cards with difficulty/pattern badges
- ✅ Topic divider with visual separator
- ✅ Coming Soon sections for future features
- ✅ Resource cards for tools
- ✅ Fully responsive

### Topic Detail Page
- ✅ Sticky sidebar navigation
- ✅ Beautiful hero section
- ✅ Overview cards
- ✅ Tips with color-coded labels
- ✅ Problem cards with difficulty
- ✅ Decision tree section
- ✅ Smooth section transitions
- ✅ Keyboard-friendly

### Flashcard Page
- ✅ Filter by category and difficulty
- ✅ Search functionality
- ✅ 3D card flip animation
- ✅ Navigation (prev/next)
- ✅ Progress bar and counter
- ✅ Statistics tracking
- ✅ Keyboard shortcuts (arrows, space)
- ✅ Study tips section

---

## How to Use These Files

### Development
1. Open `index-new.html` in browser to see landing page
2. Each page is standalone HTML file
3. CSS files are separate and linked
4. JavaScript is inline (small amount)

### Data Integration
To connect with actual data:
1. Load `assets/data/dsa.json` for topic information
2. Load `assets/data/flashcards.json` for card data
3. Implement JavaScript to:
   - Parse JSON files
   - Populate cards dynamically
   - Handle navigation/filtering
   - Save progress locally

### Deployment
1. Files are 100% static (no backend needed)
2. Deploy to GitHub Pages, Netlify, or Vercel
3. Works offline if data is cached

---

## Next Steps

### To Make Interactive
- [ ] Load real JSON data
- [ ] Implement card population from JSON
- [ ] Add local storage for progress
- [ ] Connect topic links to detail pages
- [ ] Add search functionality
- [ ] Implement filter logic

### To Enhance
- [ ] Add LLD section design
- [ ] Add HLD section design
- [ ] Add Leadership section design
- [ ] Create admin dashboard
- [ ] Add user accounts
- [ ] Track analytics

---

## Design Principles

1. **Clarity** - Every element has a clear purpose
2. **Consistency** - Same components look the same everywhere
3. **Minimalism** - Remove unnecessary elements
4. **Contrast** - Dark theme with bright accents
5. **Spacing** - Generous whitespace for breathing room
6. **Responsiveness** - Works on all screen sizes
7. **Performance** - Smooth animations, fast interactions
8. **Accessibility** - Clear labels, good contrast ratios

---

*Design by: Claude Code*
*Last Updated: 2026-07-01*
