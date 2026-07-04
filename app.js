/* ═══════════════════════════════════════════════════════════════
   DSA Practice Hub — App Logic
   Two-ring radial mind map + topic detail panel + problem modal
   ═══════════════════════════════════════════════════════════════ */

'use strict';

// ── SVG Namespace ───────────────────────────────────────────────
const SVG_NS = 'http://www.w3.org/2000/svg';

// ── State ───────────────────────────────────────────────────────
let selectedTopicId = null;
let currentProblem  = null;

// ── DOM References ──────────────────────────────────────────────
const svg          = document.getElementById('mindmapSvg');
const mapArea      = document.getElementById('mapArea');
const mapHint      = document.getElementById('mapHint');
const panelEmpty   = document.getElementById('panelEmpty');
const panelContent = document.getElementById('panelContent');
const topicIcon    = document.getElementById('topicIcon');
const topicName    = document.getElementById('topicName');
const topicBadges  = document.getElementById('topicBadges');
const tipsList     = document.getElementById('tipsList');
const problemsGrid = document.getElementById('problemsGrid');
const problemCountBadge = document.getElementById('problemCountBadge');
const backBtn      = document.getElementById('backBtn');
const resetBtn     = document.getElementById('resetBtn');
const emptyTopicsPreview = document.getElementById('emptyTopicsPreview');

const modalBackdrop = document.getElementById('modalBackdrop');
const modal         = document.getElementById('modal');
const modalTitle    = document.getElementById('modalTitle');
const modalDifficulty = document.getElementById('modalDifficulty');
const modalNum      = document.getElementById('modalNum');
const modalNotes    = document.getElementById('modalNotes');
const modalLcLink   = document.getElementById('modalLcLink');
const modalClose    = document.getElementById('modalClose');
const modalFileBtn  = document.getElementById('modalFileBtn');
const modalFilePath = document.getElementById('modalFilePath');

// ── Stats ───────────────────────────────────────────────────────
document.getElementById('totalTopics').textContent   = TOPICS.length;
document.getElementById('totalProblems').textContent = TOPICS.reduce((s, t) => s + t.problems.length, 0);

// ── Quick-access chips in empty state ───────────────────────────
TOPICS.forEach(topic => {
  const chip = document.createElement('button');
  chip.className = 'topic-chip';
  chip.style.background = hexToRgba(topic.color, 0.12);
  chip.style.color       = topic.color;
  chip.style.borderColor = hexToRgba(topic.color, 0.2);
  chip.textContent = topic.emoji + ' ' + topic.name;
  chip.addEventListener('click', () => selectTopic(topic.id));
  emptyTopicsPreview.appendChild(chip);
});

// ── Mind Map Rendering ──────────────────────────────────────────
function getMapDimensions() {
  const rect = mapArea.getBoundingClientRect();
  return { w: rect.width, h: rect.height };
}

function computeNodePositions() {
  const { w, h } = getMapDimensions();
  const cx = w / 2;
  const cy = h / 2;

  const innerR = Math.min(cx, cy) * 0.40;
  const outerR = Math.min(cx, cy) * 0.75;

  const innerTopics = TOPICS.filter(t => t.ring === 'inner');
  const outerTopics = TOPICS.filter(t => t.ring === 'outer');

  const positions = {};

  innerTopics.forEach((topic, i) => {
    const angle = (2 * Math.PI * i / innerTopics.length) - Math.PI / 2;
    positions[topic.id] = {
      x: cx + innerR * Math.cos(angle),
      y: cy + innerR * Math.sin(angle),
      ring: 'inner',
    };
  });

  outerTopics.forEach((topic, i) => {
    const angle = (2 * Math.PI * i / outerTopics.length) - Math.PI / 2;
    positions[topic.id] = {
      x: cx + outerR * Math.cos(angle),
      y: cy + outerR * Math.sin(angle),
      ring: 'outer',
    };
  });

  return { cx, cy, positions };
}

function renderMindMap() {
  svg.innerHTML = `
    <defs>
      <radialGradient id="centerGrad" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="#7C3AED"/>
        <stop offset="100%" stop-color="#4338CA"/>
      </radialGradient>
      <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
        <feGaussianBlur stdDeviation="4" result="blur"/>
        <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
      </filter>
      <filter id="softGlow" x="-60%" y="-60%" width="220%" height="220%">
        <feGaussianBlur stdDeviation="10" result="blur"/>
        <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
      </filter>
    </defs>
  `;

  const { cx, cy, positions } = computeNodePositions();

  // ── Draw connection lines ──────────────────────────────────
  const linesGroup = makeSvgEl('g', { id: 'mm-lines' });
  svg.appendChild(linesGroup);

  TOPICS.forEach((topic, i) => {
    const pos = positions[topic.id];
    const delay = i * 0.03;

    const line = makeSvgEl('line', {
      id: `line-${topic.id}`,
      class: 'mm-line',
      x1: cx, y1: cy,
      x2: pos.x, y2: pos.y,
      stroke: topic.color,
      style: `animation-delay: ${delay}s`,
    });
    linesGroup.appendChild(line);
  });

  // ── Center node ────────────────────────────────────────────
  const centerGroup = makeSvgEl('g', {});

  // Pulse ring
  const pulseRing = makeSvgEl('circle', {
    class: 'center-pulse-ring',
    cx, cy, r: 42,
  });
  centerGroup.appendChild(pulseRing);

  // Glow circle
  const centerGlow = makeSvgEl('circle', {
    cx, cy, r: 38,
    fill: 'rgba(124,58,237,0.08)',
    filter: 'url(#softGlow)',
  });
  centerGroup.appendChild(centerGlow);

  // Main circle
  const centerCircle = makeSvgEl('circle', {
    cx, cy, r: 34,
    fill: 'url(#centerGrad)',
    stroke: 'rgba(167,139,250,0.5)',
    'stroke-width': 1.5,
    filter: 'url(#glow)',
  });
  centerGroup.appendChild(centerCircle);

  // Center text
  const centerLabel = makeSvgEl('text', {
    x: cx, y: cy - 7,
    class: 'mm-node-label',
    style: 'font-size:15px; font-weight:800; fill:#e2e8f0; font-family:Inter,sans-serif;',
    'text-anchor': 'middle',
    'dominant-baseline': 'middle',
  });
  centerLabel.textContent = 'DSA';
  centerGroup.appendChild(centerLabel);

  const centerSub = makeSvgEl('text', {
    x: cx, y: cy + 10,
    style: 'font-size:9px; fill:rgba(167,139,250,0.7); font-family:Inter,sans-serif; text-anchor:middle;',
  });
  centerSub.textContent = 'Practice Hub';
  centerGroup.appendChild(centerSub);

  svg.appendChild(centerGroup);

  // ── Topic nodes ────────────────────────────────────────────
  const nodesGroup = makeSvgEl('g', { id: 'mm-nodes' });
  svg.appendChild(nodesGroup);

  TOPICS.forEach((topic, i) => {
    const pos = positions[topic.id];
    const delay = 0.1 + i * 0.04;
    const isInner = topic.ring === 'inner';
    const r = isInner ? 32 : 28;

    const nodeGroup = makeSvgEl('g', {
      id: `node-${topic.id}`,
      class: 'mm-node',
      style: `animation-delay: ${delay}s`,
      'data-id': topic.id,
    });

    // Glow background (hidden until hover/selected)
    const glowCircle = makeSvgEl('circle', {
      cx: pos.x, cy: pos.y,
      r: r + 8,
      fill: hexToRgba(topic.color, 0.1),
      class: 'mm-glow',
      style: 'transition: opacity 0.2s; opacity: 0;',
    });
    nodeGroup.appendChild(glowCircle);

    // Fill circle
    const fillCircle = makeSvgEl('circle', {
      cx: pos.x, cy: pos.y, r,
      fill: hexToRgba(topic.color, 0.12),
      stroke: topic.color,
      'stroke-width': isInner ? 2 : 1.5,
      class: 'mm-node-circle',
      style: 'transition: all 0.2s;',
    });
    nodeGroup.appendChild(fillCircle);

    // Emoji
    const emoji = makeSvgEl('text', {
      x: pos.x, y: pos.y,
      class: 'mm-node-emoji',
      'text-anchor': 'middle',
      'dominant-baseline': 'middle',
      style: `font-size: ${isInner ? 18 : 15}px;`,
    });
    emoji.textContent = topic.emoji;
    nodeGroup.appendChild(emoji);

    // Label — position it outside the circle
    const { lx, ly, anchor } = getLabelPosition(pos.x, pos.y, cx, cy, r + 10);

    const label = makeSvgEl('text', {
      x: lx, y: ly,
      'text-anchor': anchor,
      class: 'mm-node-label',
      style: `font-size: ${isInner ? 11 : 10}px; fill: rgba(226,232,240,0.85);`,
    });
    label.textContent = shortName(topic.name);
    nodeGroup.appendChild(label);

    // Interaction
    nodeGroup.addEventListener('click', () => selectTopic(topic.id));
    nodeGroup.addEventListener('mouseenter', () => {
      glowCircle.style.opacity = '1';
      fillCircle.setAttribute('fill', hexToRgba(topic.color, 0.2));
    });
    nodeGroup.addEventListener('mouseleave', () => {
      if (selectedTopicId !== topic.id) {
        glowCircle.style.opacity = '0';
        fillCircle.setAttribute('fill', hexToRgba(topic.color, 0.12));
      }
    });

    nodesGroup.appendChild(nodeGroup);
  });
}

// Helper: compute label position outside the node circle
function getLabelPosition(nx, ny, cx, cy, offset) {
  const dx = nx - cx;
  const dy = ny - cy;
  const len = Math.sqrt(dx * dx + dy * dy) || 1;
  const lx = nx + (dx / len) * offset;
  const ly = ny + (dy / len) * offset + 4;

  // Determine text-anchor based on horizontal position relative to center
  const anchor = dx < -10 ? 'end' : dx > 10 ? 'start' : 'middle';

  return { lx, ly, anchor };
}

// ── Topic Selection ─────────────────────────────────────────────
function selectTopic(id) {
  const topic = TOPICS.find(t => t.id === id);
  if (!topic) return;

  // Deselect previous
  if (selectedTopicId) {
    const prev = document.getElementById(`node-${selectedTopicId}`);
    if (prev) {
      prev.classList.remove('selected');
      const glow   = prev.querySelector('.mm-glow');
      const circle = prev.querySelector('.mm-node-circle');
      const topicPrev = TOPICS.find(t => t.id === selectedTopicId);
      if (glow)   glow.style.opacity = '0';
      if (circle) circle.setAttribute('fill', hexToRgba(topicPrev.color, 0.12));
      // Dim the line
      const line = document.getElementById(`line-${selectedTopicId}`);
      if (line) line.classList.remove('active');
    }
  }

  selectedTopicId = id;

  // Highlight selected node
  const node = document.getElementById(`node-${id}`);
  if (node) {
    node.classList.add('selected');
    const glow   = node.querySelector('.mm-glow');
    const circle = node.querySelector('.mm-node-circle');
    if (glow)   glow.style.opacity = '1';
    if (circle) circle.setAttribute('fill', hexToRgba(topic.color, 0.25));
    const line = document.getElementById(`line-${id}`);
    if (line) line.classList.add('active');
  }

  // Show hint → hide
  mapHint.classList.add('hidden');

  // Render panel
  renderTopicPanel(topic);
}

function deselectTopic() {
  if (selectedTopicId) {
    const prev = document.getElementById(`node-${selectedTopicId}`);
    if (prev) {
      prev.classList.remove('selected');
      const glow   = prev.querySelector('.mm-glow');
      const circle = prev.querySelector('.mm-node-circle');
      const topicPrev = TOPICS.find(t => t.id === selectedTopicId);
      if (glow)   glow.style.opacity = '0';
      if (circle) circle.setAttribute('fill', hexToRgba(topicPrev.color, 0.12));
      const line = document.getElementById(`line-${selectedTopicId}`);
      if (line) line.classList.remove('active');
    }
  }
  selectedTopicId = null;
  panelContent.classList.add('hidden');
  panelEmpty.style.display = '';
  mapHint.classList.remove('hidden');
}

// ── Topic Panel ─────────────────────────────────────────────────
function renderTopicPanel(topic) {
  // Switch views
  panelEmpty.style.display = 'none';
  panelContent.classList.remove('hidden');

  // Scroll to top
  document.getElementById('panelScroll').scrollTop = 0;

  // Icon
  topicIcon.textContent = topic.emoji;
  topicIcon.style.background = hexToRgba(topic.color, 0.15);
  topicIcon.style.border = `1px solid ${hexToRgba(topic.color, 0.25)}`;

  // Name
  topicName.textContent = topic.name;
  topicName.style.color = topic.color;

  // Set "Explore Full Topic" link using folder name mapping
  const exploreLink = document.getElementById('exploreTopicLink');
  if (exploreLink) {
    const folderNameMap = {
      // Core topics
      'Arrays': 'Array',
      'Binary Search': 'BinarySearch',
      'Linked Lists': 'LinkedList',
      'Trees': 'Trees',
      'Graphs': 'Graph',
      'Dynamic Programming': 'DP',
      // Technique topics
      'Backtracking': 'Backtracking',
      'Sliding Window': 'Sliding window',
      'Strings': 'Strings',
      'Merge Intervals': 'MergeIntervals',
      'Range Queries': 'Range-Query',
      'Recursion': 'Recursion',
      'Maths': 'Maths',
      'Bit Manipulation': 'BitManipulation',
      'Cyclic Sort': 'Cyclic Sort',
      'Prefix Sum': 'prefixSum',
      'Sorting': 'sorting',
      'Google / Misc': 'google',
      'Greedy': 'Greedy',
      'Heap': 'Heap'
    };
    const folderName = folderNameMap[topic.name] || topic.name;
    exploreLink.href = `dsa-topic-dynamic.html?topic=${encodeURIComponent(folderName)}`;
  }

  // Badges
  topicBadges.innerHTML = '';
  const ringBadge = document.createElement('span');
  ringBadge.className = 'badge ' + (topic.ring === 'inner' ? 'badge-ring-inner' : 'badge-ring-outer');
  ringBadge.textContent = topic.ring === 'inner' ? 'Core Topic' : 'Technique';
  topicBadges.appendChild(ringBadge);

  const countBadge = document.createElement('span');
  countBadge.className = 'badge badge-count';
  countBadge.textContent = `${topic.problems.length} problem${topic.problems.length !== 1 ? 's' : ''}`;
  topicBadges.appendChild(countBadge);

  // Problem count label
  problemCountBadge.textContent = topic.problems.length;
  problemCountBadge.className = 'badge badge-count';

  // Tips
  tipsList.innerHTML = '';
  topic.tips.forEach(tip => {
    const li = document.createElement('li');
    const dot = document.createElement('span');
    dot.className = 'tip-bullet';
    dot.style.background = topic.color;
    const text = document.createElement('span');
    text.textContent = tip;
    li.appendChild(dot);
    li.appendChild(text);
    tipsList.appendChild(li);
  });

  // Problems
  problemsGrid.innerHTML = '';
  topic.problems.forEach((problem, idx) => {
    const card = document.createElement('div');
    card.className = `problem-card ${problem.difficulty.toLowerCase()}`;
    card.style.setProperty('--topic-color', topic.color);
    card.style.animationDelay = `${idx * 0.04}s`;

    const diffBadge = document.createElement('span');
    diffBadge.className = `diff-badge ${problem.difficulty.toLowerCase()}`;
    diffBadge.textContent = problem.difficulty;

    const info = document.createElement('div');
    info.className = 'problem-info';

    const name = document.createElement('div');
    name.className = 'problem-name';
    name.textContent = problem.name;

    const lcNum = document.createElement('div');
    lcNum.className = 'problem-lc-num';
    lcNum.textContent = problem.leetcodeNum ? `LC #${problem.leetcodeNum}` : 'Custom / No LC';

    info.appendChild(name);
    info.appendChild(lcNum);

    const actions = document.createElement('div');
    actions.className = 'problem-actions';

    // Notes button
    const notesBtn = document.createElement('button');
    notesBtn.className = 'action-btn';
    notesBtn.title = 'View notes';
    notesBtn.textContent = '📋';
    notesBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      openModal(problem);
    });

    // LeetCode button
    const lcBtn = document.createElement('a');
    lcBtn.className = 'action-btn';
    lcBtn.title = 'Open LeetCode';
    lcBtn.textContent = '↗';
    if (problem.leetcodeNum && problem.leetcode) {
      lcBtn.href = problem.leetcode;
      lcBtn.target = '_blank';
      lcBtn.rel = 'noopener noreferrer';
    } else {
      lcBtn.href = '#';
      lcBtn.style.opacity = '0.3';
      lcBtn.style.cursor = 'not-allowed';
      lcBtn.addEventListener('click', e => e.preventDefault());
    }

    actions.appendChild(notesBtn);
    actions.appendChild(lcBtn);

    card.appendChild(diffBadge);
    card.appendChild(info);
    card.appendChild(actions);

    // Click whole card to open notes
    card.addEventListener('click', () => openModal(problem));

    problemsGrid.appendChild(card);
  });
}

// ── Modal ───────────────────────────────────────────────────────
function openModal(problem) {
  currentProblem = problem;

  // Difficulty
  modalDifficulty.textContent = problem.difficulty;
  modalDifficulty.className = `modal-difficulty ${problem.difficulty.toLowerCase()}`;

  // LC number
  modalNum.textContent = problem.leetcodeNum ? `LeetCode #${problem.leetcodeNum}` : '';

  // Title
  modalTitle.textContent = problem.name;

  // Notes — format nicely
  modalNotes.textContent = '';
  renderNotes(problem.notes);

  // LeetCode link
  if (problem.leetcodeNum && problem.leetcode) {
    modalLcLink.href = problem.leetcode;
    modalLcLink.classList.remove('no-link');
    modalLcLink.querySelector('span.btn-arrow').textContent = '↗';
  } else {
    modalLcLink.href = '#';
    modalLcLink.classList.add('no-link');
    modalLcLink.addEventListener('click', e => e.preventDefault());
    modalLcLink.querySelector('span.btn-arrow').textContent = '';
  }

  // File path
  modalFilePath.classList.add('hidden');
  modalFilePath.textContent = problem.file ? `python-coding-concepts/${problem.file}` : 'N/A';
  modalFileBtn.querySelector('span:last-child') && null;

  // Show modal
  modalBackdrop.classList.remove('hidden');
  document.body.style.overflow = 'hidden';
}

function renderNotes(notesText) {
  // Split into segments and highlight lines that look like headings
  modalNotes.textContent = '';
  const lines = (notesText || 'No notes available.').split('\n');
  const fragment = document.createDocumentFragment();

  lines.forEach((line, i) => {
    const span = document.createElement('span');

    // Detect "section headers" — lines ending with : or in ALL CAPS words
    if (line.match(/^[A-Z][^a-z]{2,}:?\s*$/) || line.match(/^\*\*/) ||
        (line.endsWith(':') && line.length < 40 && !line.startsWith('•') && !line.startsWith('-'))) {
      span.style.color = '#e2e8f0';
      span.style.fontWeight = '600';
    } else if (line.startsWith('•') || line.startsWith('  -') || line.startsWith('-')) {
      span.style.color = '#94a3b8';
    } else if (line.match(/^Time:|^Space:/)) {
      span.style.color = '#4ade80';
      span.style.fontWeight = '500';
    } else {
      span.style.color = '#94a3b8';
    }

    span.textContent = line;
    fragment.appendChild(span);

    if (i < lines.length - 1) {
      fragment.appendChild(document.createTextNode('\n'));
    }
  });

  modalNotes.appendChild(fragment);
}

function closeModal() {
  modalBackdrop.classList.add('hidden');
  document.body.style.overflow = '';
  currentProblem = null;
  modalFilePath.classList.add('hidden');
}

// ── Event Listeners ─────────────────────────────────────────────
modalClose.addEventListener('click', closeModal);
modalBackdrop.addEventListener('click', (e) => {
  if (e.target === modalBackdrop) closeModal();
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    if (!modalBackdrop.classList.contains('hidden')) {
      closeModal();
    } else if (selectedTopicId) {
      deselectTopic();
    }
  }
});

backBtn.addEventListener('click', deselectTopic);

resetBtn.addEventListener('click', () => {
  deselectTopic();
});

modalFileBtn.addEventListener('click', () => {
  modalFilePath.classList.toggle('hidden');
});

// ── Resize handling ─────────────────────────────────────────────
let resizeTimer;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => {
    renderMindMap();
    // Re-highlight if a topic was selected
    if (selectedTopicId) {
      const node = document.getElementById(`node-${selectedTopicId}`);
      if (node) {
        const topic = TOPICS.find(t => t.id === selectedTopicId);
        const glow   = node.querySelector('.mm-glow');
        const circle = node.querySelector('.mm-node-circle');
        if (glow)   glow.style.opacity = '1';
        if (circle) circle.setAttribute('fill', hexToRgba(topic.color, 0.25));
        const line = document.getElementById(`line-${selectedTopicId}`);
        if (line) line.classList.add('active');
      }
    }
  }, 150);
});

// ── Utilities ───────────────────────────────────────────────────
function makeSvgEl(tag, attrs) {
  const el = document.createElementNS(SVG_NS, tag);
  Object.entries(attrs).forEach(([k, v]) => el.setAttribute(k, v));
  return el;
}

function hexToRgba(hex, alpha) {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  return `rgba(${r},${g},${b},${alpha})`;
}

function shortName(name) {
  const map = {
    'Dynamic Programming': 'Dyn. Prog.',
    'Binary Search': 'Binary Search',
    'Linked Lists': 'Linked Lists',
    'Backtracking': 'Backtracking',
    'Sliding Window': 'Sliding Window',
    'Merge Intervals': 'Merge Intervals',
    'Range Queries': 'Range Queries',
    'Bit Manipulation': 'Bit Manip.',
    'Cyclic Sort': 'Cyclic Sort',
    'Prefix Sum': 'Prefix Sum',
    'Google / Misc': 'Google / Misc',
  };
  return map[name] || name;
}

// ── Section Navigation ──────────────────────────────────────────
function showSection(section) {
  if (section === 'dsa') {
    // Already on DSA, just refresh
    deselectTopic();
  } else {
    alert(section.toUpperCase() + ' section is coming soon! 🚀\n\nCurrently available: DSA Practice');
  }
}

// ── Init ────────────────────────────────────────────────────────
// Wait for layout to settle before measuring dimensions
requestAnimationFrame(() => {
  setTimeout(() => {
    renderMindMap();
  }, 50);
});
