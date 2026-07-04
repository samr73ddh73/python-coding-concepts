/* ═══════════════════════════════════════════════════════════════
   NOTES SECTION — Tab switching, sidebar, markdown renderer
   ═══════════════════════════════════════════════════════════════ */

'use strict';

// ── DOM refs ────────────────────────────────────────────────────
const mainLayout        = document.querySelector('.main-layout');
const notesLayout       = document.getElementById('notesLayout');
const notesNav          = document.getElementById('notesNav');
const notesSearch       = document.getElementById('notesSearch');
const notesEmpty        = document.getElementById('notesEmpty');
const notesViewer       = document.getElementById('notesViewer');
const notesViewerHeader = document.getElementById('notesViewerHeader');
const notesMd           = document.getElementById('notesMd');
const tabBtns           = document.querySelectorAll('.tab-btn');

let activeNoteId = null;

// ── Tab Switching ───────────────────────────────────────────────
tabBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    const tab = btn.dataset.tab;
    tabBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    if (tab === 'mindmap') {
      mainLayout.style.display = '';
      notesLayout.classList.add('hidden');
    } else {
      mainLayout.style.display = 'none';
      notesLayout.classList.remove('hidden');
      if (notesNav.children.length === 0) buildNotesSidebar();
    }
  });
});

// ── Build sidebar ───────────────────────────────────────────────
function buildNotesSidebar() {
  const categories = {};
  NOTES.forEach(note => {
    if (!categories[note.category]) categories[note.category] = [];
    categories[note.category].push(note);
  });

  const catOrder = ['Python', 'Concepts', 'Data Structures', 'Patterns'];
  const orderedCats = [
    ...catOrder,
    ...Object.keys(categories).filter(c => !catOrder.includes(c)),
  ];

  orderedCats.forEach(cat => {
    if (!categories[cat]) return;

    const group = document.createElement('div');
    group.className = 'notes-category';

    const label = document.createElement('div');
    label.className = 'notes-category-label';
    label.textContent = cat;
    group.appendChild(label);

    categories[cat].forEach(note => {
      const item = document.createElement('div');
      item.className = 'note-item';
      item.dataset.id    = note.id;
      item.dataset.title = note.title.toLowerCase();

      const emojiEl = document.createElement('span');
      emojiEl.className   = 'note-item-emoji';
      emojiEl.textContent = note.emoji;

      const titleEl = document.createElement('span');
      titleEl.className   = 'note-item-title';
      titleEl.textContent = note.title;

      item.appendChild(emojiEl);
      item.appendChild(titleEl);
      item.addEventListener('click', () => openNote(note.id));
      group.appendChild(item);
    });

    notesNav.appendChild(group);
  });
}

// ── Open a note ─────────────────────────────────────────────────
function openNote(id) {
  const note = NOTES.find(n => n.id === id);
  if (!note) return;

  activeNoteId = id;

  // Sidebar highlight
  document.querySelectorAll('.note-item').forEach(el => {
    el.classList.toggle('active', el.dataset.id === id);
  });

  // Swap empty → viewer
  notesEmpty.style.display = 'none';
  notesViewer.classList.remove('hidden');

  // Header
  notesViewerHeader.innerHTML =
    '<div class="notes-viewer-title">' +
      '<span>' + note.emoji + '</span>' +
      '<h2>' + note.title + '</h2>' +
    '</div>' +
    '<div class="notes-viewer-meta">' +
      '<span class="badge badge-ring-outer">' + note.category + '</span>' +
    '</div>';

  // Render
  notesMd.innerHTML  = renderMd(note.content);
  notesMd.scrollTop  = 0;
}

// ── Search ──────────────────────────────────────────────────────
notesSearch.addEventListener('input', () => {
  const q = notesSearch.value.toLowerCase().trim();
  document.querySelectorAll('.note-item').forEach(el => {
    const matches = !q || el.dataset.title.includes(q);
    el.classList.toggle('search-hidden', !matches);
  });
});

// ── Markdown renderer ───────────────────────────────────────────
function renderMd(raw) {
  let html = raw;

  // 1. Extract fenced code blocks before escaping HTML
  const codeBlocks = [];
  html = html.replace(/```(\w*)\n([\s\S]*?)```/g, function(_, lang, code) {
    const idx = codeBlocks.length;
    codeBlocks.push({ lang: lang || '', code: code });
    return '\x00CODE' + idx + '\x00';
  });

  // 2. Escape HTML in remaining text
  html = html
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');

  // 3. Block elements
  html = html.replace(/^#### (.+)$/gm, '<h4>$1</h4>');
  html = html.replace(/^### (.+)$/gm,  '<h3>$1</h3>');
  html = html.replace(/^## (.+)$/gm,   '<h2>$1</h2>');
  html = html.replace(/^# (.+)$/gm,    '<h1>$1</h1>');
  html = html.replace(/^---+$/gm, '<hr>');

  // Blockquotes
  html = html.replace(/^&gt;\s?(.*)$/gm, '<blockquote><p>$1</p></blockquote>');
  html = html.replace(/<\/blockquote>\n<blockquote>/g, '\n');

  // Tables — detect blocks where most lines contain |
  html = html.replace(/((?:^[^\n]*\|[^\n]*\n)+)/gm, function(block) {
    var lines = block.trim().split('\n');
    if (lines.length < 2) return block;
    var sepIdx = -1;
    for (var i = 0; i < lines.length; i++) {
      if (/^\|?[\s\-|:]+\|?$/.test(lines[i].trim())) { sepIdx = i; break; }
    }
    if (sepIdx < 1) return block;

    function parseRow(line, tag) {
      var cells = line.replace(/^\||\|$/g, '').split('|');
      return '<tr>' + cells.map(function(c) {
        return '<' + tag + '>' + inlineMd(c.trim()) + '</' + tag + '>';
      }).join('') + '</tr>';
    }

    var thead = '<thead>' + parseRow(lines[sepIdx - 1], 'th') + '</thead>';
    var tbody = '<tbody>' + lines.slice(sepIdx + 1).filter(Boolean).map(function(l) {
      return parseRow(l, 'td');
    }).join('') + '</tbody>';
    return '<table>' + thead + tbody + '</table>';
  });

  // Unordered lists
  html = html.replace(/((?:^[*\-] .+$\n?)+)/gm, function(block) {
    var items = block.trim().split('\n').filter(Boolean).map(function(l) {
      return '<li>' + inlineMd(l.replace(/^[*\-] /, '').trim()) + '</li>';
    }).join('');
    return '<ul>' + items + '</ul>';
  });

  // Ordered lists
  html = html.replace(/((?:^\d+\. .+$\n?)+)/gm, function(block) {
    var items = block.trim().split('\n').filter(Boolean).map(function(l) {
      return '<li>' + inlineMd(l.replace(/^\d+\. /, '').trim()) + '</li>';
    }).join('');
    return '<ol>' + items + '</ol>';
  });

  // 4. Restore code blocks
  html = html.replace(/\x00CODE(\d+)\x00/g, function(_, idx) {
    var b    = codeBlocks[+idx];
    var high = highlightCode(b.code, b.lang);
    return '<pre><code class="lang-' + b.lang + '">' + high + '</code></pre>';
  });

  // 5. Paragraphs — wrap orphan text chunks
  var blockStarts = ['<h1', '<h2', '<h3', '<h4', '<ul', '<ol', '<pre',
                     '<table', '<hr', '<blockquote', '<p'];
  html = html.split(/\n{2,}/).map(function(chunk) {
    chunk = chunk.trim();
    if (!chunk) return '';
    if (blockStarts.some(function(t) { return chunk.startsWith(t); })) return chunk;
    return '<p>' + inlineMd(chunk.replace(/\n/g, ' ')) + '</p>';
  }).join('\n');

  return html;
}

function inlineMd(text) {
  return text
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
}

// ── Minimal syntax highlighting for Python ──────────────────────
// Single-pass tokenizer — never re-processes already-emitted spans.
function highlightCode(code, lang) {
  function esc(s) {
    return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  }

  if (lang !== 'python') return esc(code);

  var KWS = new Set([
    'def','class','return','if','elif','else','for','while','in',
    'not','and','or','import','from','as','pass','break','continue',
    'lambda','yield','with','try','except','finally','raise',
    'True','False','None','global','nonlocal','del','assert','is',
  ]);

  var out = '';
  var i   = 0;
  var n   = code.length;

  while (i < n) {
    var c = code[i];

    // Comment: # to end of line
    if (c === '#') {
      var j = i;
      while (j < n && code[j] !== '\n') j++;
      out += '<span class="cm">' + esc(code.slice(i, j)) + '</span>';
      i = j;
      continue;
    }

    // String: triple-quoted then single-quoted
    if (c === '"' || c === "'") {
      var q = c;
      var j = i;
      if (code.slice(i, i + 3) === q + q + q) {
        j = i + 3;
        while (j < n && code.slice(j, j + 3) !== q + q + q) {
          if (code[j] === '\\') j++;
          j++;
        }
        j = Math.min(j + 3, n);
      } else {
        j = i + 1;
        while (j < n && code[j] !== q && code[j] !== '\n') {
          if (code[j] === '\\') j++;
          j++;
        }
        if (j < n && code[j] === q) j++;
      }
      out += '<span class="str">' + esc(code.slice(i, j)) + '</span>';
      i = j;
      continue;
    }

    // Keyword or plain identifier
    if (/[a-zA-Z_]/.test(c)) {
      var j = i;
      while (j < n && /\w/.test(code[j])) j++;
      var word = code.slice(i, j);
      out += KWS.has(word)
        ? '<span class="kw">' + esc(word) + '</span>'
        : esc(word);
      i = j;
      continue;
    }

    // Number
    if (/\d/.test(c)) {
      var j = i;
      while (j < n && /[\d.]/.test(code[j])) j++;
      out += '<span class="num">' + esc(code.slice(i, j)) + '</span>';
      i = j;
      continue;
    }

    // Any other character
    out += esc(c);
    i++;
  }

  return out;
}
