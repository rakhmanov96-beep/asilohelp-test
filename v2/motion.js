// asilohelp — анимации сайта (в паре с motion.css). Карта: /animacii/
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // 5. Появление при прокрутке, один раз. Лесенка: data-reveal-group на родителе.
  document.querySelectorAll('[data-reveal-group]').forEach(group => {
    const step = parseFloat(group.dataset.revealGroup) || 0.08;
    group.querySelectorAll('[data-reveal]').forEach((el, i) => el.style.setProperty('--reveal-delay', Math.min(i * step, 0.36) + 's'));
  });
  const shown = el => el.classList.add('is-shown');
  if (reduce || !('IntersectionObserver' in window)) {
    document.querySelectorAll('[data-reveal]').forEach(shown);
  } else {
    const io = new IntersectionObserver(entries => entries.forEach(e => {
      if (e.isIntersecting) { shown(e.target); io.unobserve(e.target); countUp(e.target); }
    }), { rootMargin: '0px 0px -10% 0px', threshold: 0.1 });
    document.querySelectorAll('[data-reveal]').forEach(el => io.observe(el));
  }

  // 14. Счётчик цифр (по желанию): <span data-count="187">187</span> внутри блока с data-reveal.
  function countUp(root) {
    root.querySelectorAll('[data-count]').forEach(el => {
      const to = parseInt(el.dataset.count, 10); if (!to || reduce) return;
      const t0 = performance.now(), dur = 1200;
      const tick = t => {
        const p = Math.min(1, (t - t0) / dur), eased = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(to * eased).toLocaleString('ru-RU');
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    });
  }

  // 8. Шапка прячется при прокрутке вниз и возвращается при прокрутке вверх.
  const header = document.querySelector('.m-header');
  if (header && !reduce) {
    let last = scrollY;
    addEventListener('scroll', () => {
      const y = scrollY;
      header.classList.toggle('is-hidden', y > last && y > 120);
      last = y;
    }, { passive: true });
  }

  // 10. Отзывы на телефоне: открываются нажатием.
  document.querySelectorAll('.m-review').forEach(card => {
    card.addEventListener('click', () => { if (!matchMedia('(hover: hover)').matches) card.classList.toggle('is-open'); });
  });
})();
