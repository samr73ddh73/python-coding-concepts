// Simple Markdown to HTML Renderer
function markdownToHTML(md) {
  let html = md;

  // Escape HTML special characters first
  html = html.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

  // Code blocks with language support
  html = html.replace(/```(\w*)\n([\s\S]*?)```/g, (match, lang, code) => {
    const language = lang || 'python';
    const escapedCode = code.trim();
    return `<pre class="code-block language-${language}"><code>${escapedCode}</code></pre>`;
  });

  // Inline code
  html = html.replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>');

  // Headers
  html = html.replace(/^### (.*?)$/gm, '<h3 class="md-h3">$1</h3>');
  html = html.replace(/^## (.*?)$/gm, '<h2 class="md-h2">$1</h2>');
  html = html.replace(/^# (.*?)$/gm, '<h1 class="md-h1">$1</h1>');

  // Bold and italic
  html = html.replace(/\*\*\*(.*?)\*\*\*/g, '<strong><em>$1</em></strong>');
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
  html = html.replace(/__(.*?)__/g, '<strong>$1</strong>');
  html = html.replace(/_(.*?)_/g, '<em>$1</em>');

  // Lists
  html = html.replace(/^\* (.*?)$/gm, '<li>$1</li>');
  html = html.replace(/^\- (.*?)$/gm, '<li>$1</li>');
  html = html.replace(/^\d+\. (.*?)$/gm, '<li>$1</li>');
  html = html.replace(/(<li>.*<\/li>)/s, '<ul class="md-list">$1</ul>');

  // Line breaks
  html = html.replace(/\n\n/g, '</p><p>');
  html = '<p>' + html + '</p>';
  html = html.replace(/<p><\/p>/g, '');

  // Links
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" class="md-link">$1</a>');

  // Horizontal rules
  html = html.replace(/^---$/gm, '<hr class="md-hr">');

  // Blockquotes
  html = html.replace(/^> (.*?)$/gm, '<blockquote class="md-blockquote">$1</blockquote>');

  return html;
}

// Syntax highlighting for Python code
function highlightPythonCode(codeElement) {
  let code = codeElement.textContent;

  // Python keywords
  const keywords = ['def', 'class', 'if', 'else', 'elif', 'for', 'while', 'return', 'import', 'from', 'as', 'try', 'except', 'finally', 'with', 'lambda', 'pass', 'break', 'continue', 'True', 'False', 'None', 'and', 'or', 'not', 'in', 'is'];
  const builtins = ['len', 'range', 'print', 'enumerate', 'zip', 'map', 'filter', 'sorted', 'sum', 'max', 'min', 'str', 'int', 'list', 'dict', 'set', 'tuple'];

  // Highlight keywords
  keywords.forEach(keyword => {
    const regex = new RegExp(`\\b${keyword}\\b`, 'g');
    code = code.replace(regex, `<span class="keyword">${keyword}</span>`);
  });

  // Highlight builtins
  builtins.forEach(builtin => {
    const regex = new RegExp(`\\b${builtin}\\b`, 'g');
    code = code.replace(regex, `<span class="builtin">${builtin}</span>`);
  });

  // Highlight strings
  code = code.replace(/(['"])([^'"]*)\1/g, '<span class="string">$1$2$1</span>');

  // Highlight comments
  code = code.replace(/#(.*?)(?=\n|$)/g, '<span class="comment">#$1</span>');

  // Highlight numbers
  code = code.replace(/\b(\d+)\b/g, '<span class="number">$1</span>');

  codeElement.innerHTML = code;
}

// Apply syntax highlighting to all code blocks
function highlightAllCode() {
  document.querySelectorAll('code.inline-code').forEach(el => {
    if (!el.classList.contains('highlighted')) {
      highlightPythonCode(el);
      el.classList.add('highlighted');
    }
  });
}

// Export for use
window.markdownToHTML = markdownToHTML;
window.highlightPythonCode = highlightPythonCode;
window.highlightAllCode = highlightAllCode;
