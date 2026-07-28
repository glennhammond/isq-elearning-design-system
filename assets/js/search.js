// Search — loads the generated JSON index and filters it client-side.
// No server or external search service. Requires the site to be served
// over http(s) (a local static server is fine) rather than opened via
// file:// in browsers that block fetch() on the file protocol.
(function () {
  var input = document.querySelector('[data-docs-search-input]');
  var resultsBox = document.querySelector('[data-docs-search-results]');
  if (!input || !resultsBox) return;

  var index = null;
  var basePath = input.getAttribute('data-base') || '';

  function loadIndex() {
    if (index) return Promise.resolve(index);
    return fetch(basePath + 'data/search-index.json')
      .then(function (res) { return res.json(); })
      .then(function (json) { index = json; return index; })
      .catch(function () {
        resultsBox.innerHTML = '<p class="docs-search-empty">Search index unavailable — this page may have been opened without a local server.</p>';
        return [];
      });
  }

  function render(matches, query) {
    if (!query) {
      resultsBox.hidden = true;
      resultsBox.innerHTML = '';
      return;
    }
    resultsBox.hidden = false;
    if (matches.length === 0) {
      resultsBox.innerHTML = '<p class="docs-search-empty">No matches for &ldquo;' + escapeHtml(query) + '&rdquo;. Try a component name, class name, learning purpose or platform.</p>';
      return;
    }
    resultsBox.innerHTML = matches.slice(0, 12).map(function (item) {
      return '<a class="docs-search-result" href="' + basePath + item.url + '">' +
        '<span class="docs-search-result__kind">' + item.kind + '</span>' +
        '<span class="docs-search-result__name">' + escapeHtml(item.name) + '</span>' +
        '<span class="docs-search-result__desc">' + escapeHtml(item.summary || '') + '</span>' +
        '</a>';
    }).join('');
  }

  function escapeHtml(str) {
    return String(str).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function search(query) {
    var q = query.trim().toLowerCase();
    if (!q) return [];
    return index.filter(function (item) {
      return item.haystack.indexOf(q) !== -1;
    });
  }

  var debounceTimer;
  input.addEventListener('input', function () {
    clearTimeout(debounceTimer);
    var query = input.value;
    debounceTimer = setTimeout(function () {
      loadIndex().then(function () {
        render(search(query), query.trim());
      });
    }, 120);
  });

  // Close results when focus leaves the search widget.
  document.addEventListener('click', function (event) {
    if (!event.target.closest('.docs-search-wrap')) {
      resultsBox.hidden = true;
    }
  });
})();
