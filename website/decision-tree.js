/**
 * Decision Tree Parser and Renderer
 * Converts ASCII tree format to interactive visual trees
 */

class DecisionTree {
  constructor(markdownText) {
    this.raw = markdownText;
    this.root = this.parse();
  }

  parse() {
    const lines = this.raw.split('\n');
    const codeBlock = [];
    let inCode = false;

    // Extract the ASCII tree from code block
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      if (line.trim().startsWith('```')) {
        inCode = !inCode;
        continue;
      }
      if (inCode) {
        codeBlock.push(line);
      }
    }

    if (codeBlock.length === 0) return null;

    // Parse tree structure
    const root = {
      text: codeBlock[0].replace(/[├─└│]/g, '').trim(),
      children: [],
      level: 0
    };

    let stack = [root];

    for (let i = 1; i < codeBlock.length; i++) {
      const line = codeBlock[i];
      if (!line.trim()) continue;

      const level = this.getLevel(line);
      const text = line.replace(/[├─└│\s]/g, '').trim();

      if (!text) continue;

      const node = { text, children: [], level };

      // Find parent
      while (stack.length > 1 && stack[stack.length - 1].level >= level) {
        stack.pop();
      }

      const parent = stack[stack.length - 1];
      parent.children.push(node);
      stack.push(node);
    }

    return root;
  }

  getLevel(line) {
    let level = 0;
    for (let i = 0; i < line.length; i++) {
      if (line[i] === ' ') level++;
      else if (['├', '─', '└', '│'].includes(line[i])) continue;
      else break;
    }
    return Math.floor(level / 4);
  }

  renderHTML() {
    if (!this.root) return '<p>No decision tree found</p>';

    // Calculate positions first
    this.positions = new Map();
    this.calculatePositions(this.root, 200, 30, 80);

    // Build SVG string
    let svgContent = '<svg class="tree-svg" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">';

    // Draw lines (connections)
    svgContent += this.buildLines(this.root);

    // Draw nodes (circles with text)
    svgContent += this.buildNodes(this.root);

    svgContent += '</svg>';

    return `<div class="tree-container">${svgContent}</div>`;
  }

  calculatePositions(node, x, y, xOffset) {
    this.positions.set(node, { x, y });

    if (node.children.length > 0) {
      const totalWidth = (node.children.length - 1) * xOffset;
      const startX = x - totalWidth / 2;

      node.children.forEach((child, i) => {
        const childX = startX + i * xOffset;
        const childY = y + 70;
        this.calculatePositions(child, childX, childY, xOffset * 0.6);
      });
    }
  }

  buildLines(node) {
    const pos = this.positions.get(node);
    if (!pos) return '';

    let lines = '';

    node.children.forEach(child => {
      const childPos = this.positions.get(child);
      lines += `<line x1="${pos.x}" y1="${pos.y + 20}" x2="${childPos.x}" y2="${childPos.y - 20}"
                      stroke="rgba(168, 85, 247, 0.5)" stroke-width="2" class="tree-connector"/>`;
      lines += this.buildLines(child);
    });

    return lines;
  }

  buildNodes(node) {
    const pos = this.positions.get(node);
    if (!pos) return '';

    const text = node.text.length > 25 ? node.text.substring(0, 22) + '...' : node.text;
    const isRoot = pos.y < 50;
    const color = isRoot ? '#7C3AED' : '#0ea5e9';

    let nodes = `<circle cx="${pos.x}" cy="${pos.y}" r="20" fill="${color}" stroke="${color}" stroke-width="2" class="tree-node-circle"/>`;
    nodes += `<text x="${pos.x}" y="${pos.y}" text-anchor="middle" dominant-baseline="middle"
                    fill="white" font-size="10" font-weight="600" class="tree-node-text">${this.escapeHtml(text)}</text>`;

    node.children.forEach(child => {
      nodes += this.buildNodes(child);
    });

    return nodes;
  }

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
}

// Flashcard implementation
class Flashcard {
  constructor(question, answer) {
    this.question = question;
    this.answer = answer;
    this.isFlipped = false;
  }

  toggle() {
    this.isFlipped = !this.isFlipped;
  }

  renderHTML() {
    return `
      <div class="flashcard ${this.isFlipped ? 'flipped' : ''}" onclick="this.classList.toggle('flipped')">
        <div class="flashcard-inner">
          <div class="flashcard-front">
            <div class="flashcard-label">Question</div>
            <div class="flashcard-content">${this.escapeHtml(this.question)}</div>
          </div>
          <div class="flashcard-back">
            <div class="flashcard-label">Answer</div>
            <div class="flashcard-content">${this.escapeHtml(this.answer)}</div>
          </div>
        </div>
      </div>
    `;
  }

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
}

// Generate flashcards from topic tips
function generateFlashcardsFromTips(tips) {
  return tips.map((tip, idx) => new Flashcard(
    `Tip ${idx + 1}`,
    tip
  ));
}

// Render flashcard deck
function renderFlashcardDeck(flashcards) {
  if (flashcards.length === 0) {
    return '<p style="color: var(--text-secondary); font-size: 0.9rem;">No flashcards available for this topic</p>';
  }

  return `
    <div class="flashcard-deck">
      <div class="deck-header">
        <h3 style="margin: 0; font-size: 1rem;">Quick Tips (${flashcards.length} cards)</h3>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.85rem; color: var(--text-secondary);">Click to flip</p>
      </div>
      <div class="flashcard-container">
        ${flashcards.map((card, idx) => `
          <div class="flashcard-wrapper">
            ${card.renderHTML()}
            <div class="card-indicator">${idx + 1}/${flashcards.length}</div>
          </div>
        `).join('')}
      </div>
    </div>
  `;
}
