// ═══════════════════════════════════════════════════════════════
// Interview Prep Hub - Main Application
// Handles data loading, filtering, and progress tracking
// ═══════════════════════════════════════════════════════════════

class InterviewHub {
  constructor() {
    this.dsaData = null;
    this.progress = this.loadProgress();
    this.init();
  }

  // Initialize app
  async init() {
    await this.loadData();
    this.setupEventListeners();
  }

  // Load JSON data
  async loadData() {
    try {
      const response = await fetch('assets/data/dsa.json');
      if (response.ok) {
        this.dsaData = await response.json();
        console.log('✓ DSA data loaded successfully', this.dsaData);
      } else {
        console.warn('Could not load dsa.json, using fallback data');
        this.dsaData = this.getFallbackData();
      }
    } catch (error) {
      console.warn('Error loading JSON, using fallback:', error);
      this.dsaData = this.getFallbackData();
    }
  }

  // Fallback data if JSON not available
  getFallbackData() {
    return {
      version: '1.0',
      lastUpdated: '2026-07-01',
      topics: [
        {
          id: 'array',
          name: 'Array',
          problems: [
            { name: '1-move-zeros.py', path: 'Array/1-move-zeros.py', type: 'implementation' },
            { name: '2-remove-duplicates.py', path: 'Array/2-remove-duplicates.py', type: 'implementation' }
          ],
          tips: [
            { category: 'Two-Pointer', text: 'Use two pointers for in-place modifications' }
          ],
          decisionTree: null
        }
      ]
    };
  }

  // Setup event listeners
  setupEventListeners() {
    // Search input
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
      searchInput.addEventListener('input', (e) => this.filterTopics(e.target.value));
    }

    // Category filter
    const categoryFilter = document.getElementById('categoryFilter');
    if (categoryFilter) {
      categoryFilter.addEventListener('change', (e) => this.filterByCategory(e.target.value));
    }

    // Difficulty filter
    const difficultyFilter = document.getElementById('difficultyFilter');
    if (difficultyFilter) {
      difficultyFilter.addEventListener('change', (e) => this.filterByDifficulty(e.target.value));
    }
  }

  // Filter topics by search query
  filterTopics(query) {
    const cards = document.querySelectorAll('.topic-card');
    query = query.toLowerCase();

    cards.forEach(card => {
      const title = card.querySelector('h3')?.textContent.toLowerCase() || '';
      const matches = title.includes(query);
      card.style.display = matches ? '' : 'none';
    });
  }

  // Filter by category (placeholder)
  filterByCategory(category) {
    console.log('Filter by category:', category);
  }

  // Filter by difficulty (placeholder)
  filterByDifficulty(difficulty) {
    console.log('Filter by difficulty:', difficulty);
  }

  // Local Storage: Save progress
  saveProgress() {
    localStorage.setItem('interviewHub_progress', JSON.stringify(this.progress));
  }

  // Local Storage: Load progress
  loadProgress() {
    const saved = localStorage.getItem('interviewHub_progress');
    return saved ? JSON.parse(saved) : {
      topicsViewed: [],
      problemsSolved: [],
      lastVisit: new Date().toISOString(),
      flashcardsLearned: []
    };
  }

  // Mark topic as viewed
  markTopicViewed(topicId) {
    if (!this.progress.topicsViewed.includes(topicId)) {
      this.progress.topicsViewed.push(topicId);
      this.progress.lastVisit = new Date().toISOString();
      this.saveProgress();
    }
  }

  // Mark problem as solved
  markProblemSolved(problemId) {
    if (!this.progress.problemsSolved.includes(problemId)) {
      this.progress.problemsSolved.push(problemId);
      this.saveProgress();
    }
  }

  // Get topic by ID
  getTopic(topicId) {
    if (!this.dsaData) return null;
    return this.dsaData.topics.find(t => t.id === topicId);
  }

  // Get all topics
  getTopics() {
    return this.dsaData ? this.dsaData.topics : [];
  }

  // Get progress stats
  getProgressStats() {
    if (!this.dsaData) return { topicsViewed: 0, problemsSolved: 0, totalTopics: 0, totalProblems: 0 };

    const totalProblems = this.dsaData.topics.reduce((sum, t) => sum + (t.problems ? t.problems.length : 0), 0);

    return {
      topicsViewed: this.progress.topicsViewed.length,
      problemsSolved: this.progress.problemsSolved.length,
      totalTopics: this.dsaData.topics.length,
      totalProblems: totalProblems
    };
  }
}

// Initialize on page load
let app = null;
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    app = new InterviewHub();
  });
} else {
  app = new InterviewHub();
}
