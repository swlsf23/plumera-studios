(() => {
  let current = null;

  document.addEventListener('click', (event) => {
    const button = event.target.closest('button.inline-audio');
    if (!button) return;

    const src = button.getAttribute('data-src');
    if (!src) return;

    event.preventDefault();

    if (current) {
      current.pause();
      current = null;
      document.querySelectorAll('button.inline-audio.is-playing').forEach((el) => {
        el.classList.remove('is-playing');
      });
    }

    const audio = new Audio(src);
    current = audio;
    button.classList.add('is-playing');

    const clear = () => {
      if (current === audio) current = null;
      button.classList.remove('is-playing');
    };

    audio.addEventListener('ended', clear);
    audio.addEventListener('pause', clear);
    void audio.play().catch(clear);
  });
})();
