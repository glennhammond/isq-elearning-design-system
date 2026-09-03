// Navigation — complete information architecture plus mobile menu behaviour.
(function () {
  var toggle = document.querySelector('.docs-nav-toggle');
  var nav = document.querySelector('.docs-primary-nav');
  if (!nav) return;

  var searchInput = document.querySelector('[data-docs-search-input]');
  var base = searchInput ? (searchInput.getAttribute('data-base') || '') : '';
  var path = window.location.pathname;
  var items = [
    ['Overview', 'overview/index.html', '/overview/'],
    ['Foundations', 'foundations/index.html', '/foundations/'],
    ['Learning design', 'learning-design/index.html', '/learning-design/'],
    ['Learning patterns', 'patterns/index.html', '/patterns/'],
    ['Components', 'components/index.html', '/components/'],
    ['Platforms', 'platforms/rise/index.html', '/platforms/'],
    ['Imagery & media', 'media/index.html', '/media/'],
    ['Implementations', 'implementations/index.html', '/implementations/'],
    ['Applications', 'applications/index.html', '/applications/'],
    ['Resources', 'resources/index.html', '/resources/'],
    ['Governance', 'governance/index.html', '/governance/'],
    ['Changelog', 'changelog/index.html', '/changelog/']
  ];

  nav.textContent = '';
  items.forEach(function (item) {
    var link = document.createElement('a');
    link.className = 'docs-nav-link';
    link.href = base + item[1];
    link.textContent = item[0];
    if (path.indexOf(item[2]) !== -1) link.setAttribute('aria-current', 'page');
    nav.appendChild(link);
  });

  if (!toggle) return;
  toggle.addEventListener('click', function () {
    var isOpen = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(isOpen));
  });

  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape' && nav.classList.contains('is-open')) {
      nav.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.focus();
    }
  });
})();
