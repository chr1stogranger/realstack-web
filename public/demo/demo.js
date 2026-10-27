// Demo pages (/demo/ops, /demo/blueprint, /demo/together): phones get the
// 9:16 cut, everything else the 16:9 one. Without JS the 16:9 cut plays.
(function () {
  var box = document.querySelector('[data-film]');
  if (!box) return;
  var video = box.querySelector('video');
  var narrow = window.matchMedia('(max-width: 768px)');
  var still = window.matchMedia('(prefers-reduced-motion: reduce)');

  function pick() {
    var shape = narrow.matches ? 'tall' : 'wide';
    var src = video.getAttribute('data-' + shape);
    box.classList.toggle('tall', shape === 'tall');
    if (video.getAttribute('src') === src) return;
    var wasPlaying = !video.paused;
    video.setAttribute('poster', video.getAttribute('data-' + shape + '-poster'));
    video.setAttribute('src', src);
    video.load();
    if (wasPlaying || video.autoplay) video.play().catch(function () {});
  }

  if (still.matches) { video.autoplay = false; video.pause(); }
  pick();
  narrow.addEventListener('change', pick);
})();
