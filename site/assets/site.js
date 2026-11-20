(() => {
  const film = document.querySelector('#hero-film');
  const toggle = document.querySelector('.film-toggle');
  if (!film || !toggle) return;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  let ready = false;
  const sync = () => { toggle.textContent = film.paused ? 'Play film' : 'Pause film'; film.classList.toggle('is-playing', !film.paused); };
  const initialize = () => {
    if (ready) return;
    ready = true;
    toggle.hidden = false;
    if (!reduced.matches) film.play().catch(sync);
    sync();
  };
  film.addEventListener('loadedmetadata', initialize);
  film.addEventListener('play', sync);
  film.addEventListener('pause', sync);
  film.addEventListener('error', () => { film.style.display = 'none'; toggle.hidden = true; });
  film.querySelector('source')?.addEventListener('error', () => { film.style.display = 'none'; toggle.hidden = true; });
  toggle.addEventListener('click', () => { if (!ready) return; if (film.paused) film.play().catch(sync); else film.pause(); });
  document.addEventListener('visibilitychange', () => { if (document.hidden) film.pause(); });
  if (film.readyState >= 1) initialize();
})();
