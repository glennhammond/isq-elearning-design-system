// Filters — narrows the visible component cards on the components index page.
// Pure client-side; reads data attributes already present on each card.
(function () {
  var bar = document.querySelector('[data-docs-filter-bar]');
  if (!bar) return;

  var cards = Array.prototype.slice.call(document.querySelectorAll('[data-docs-filterable]'));
  var countEl = document.querySelector('[data-docs-filter-count]');
  var selects = Array.prototype.slice.call(bar.querySelectorAll('select'));

  function apply() {
    var active = {};
    selects.forEach(function (select) {
      if (select.value) active[select.name] = select.value;
    });

    var visible = 0;
    cards.forEach(function (card) {
      var matches = Object.keys(active).every(function (key) {
        var cardValue = card.getAttribute('data-' + key) || '';
        return cardValue.split(' ').indexOf(active[key]) !== -1;
      });
      card.hidden = !matches;
      if (matches) visible++;
    });

    if (countEl) {
      countEl.textContent = visible + (visible === 1 ? ' component' : ' components');
    }
  }

  selects.forEach(function (select) {
    select.addEventListener('change', apply);
  });

  apply();
})();
