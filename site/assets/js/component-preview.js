// Component preview — copy-code buttons and desktop/mobile toggle
// for live preview frames. No dependency on other modules.
(function () {
  // Copy buttons
  document.querySelectorAll('[data-docs-copy]').forEach(function (button) {
    button.addEventListener('click', function () {
      var targetId = button.getAttribute('data-docs-copy');
      var target = document.getElementById(targetId);
      if (!target) return;
      var text = target.textContent;
      navigator.clipboard.writeText(text).then(function () {
        var original = button.textContent;
        button.textContent = 'Copied';
        setTimeout(function () { button.textContent = original; }, 1600);
      }).catch(function () {
        button.textContent = 'Copy failed';
      });
    });
  });

  // Desktop / mobile preview toggle
  document.querySelectorAll('[data-docs-preview]').forEach(function (preview) {
    var frame = preview.querySelector('.docs-preview__frame');
    var buttons = preview.querySelectorAll('[data-docs-preview-mode]');
    buttons.forEach(function (button) {
      button.addEventListener('click', function () {
        var mode = button.getAttribute('data-docs-preview-mode');
        frame.classList.toggle('is-mobile', mode === 'mobile');
        buttons.forEach(function (b) { b.setAttribute('aria-pressed', String(b === button)); });
      });
    });
  });
})();
