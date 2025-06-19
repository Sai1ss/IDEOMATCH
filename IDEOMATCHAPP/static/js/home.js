document.addEventListener('DOMContentLoaded', () => {
  // ───────── Animaciones al hacer scroll ─────────
  const animatedItems = document.querySelectorAll('.animated-on-scroll');
  if ('IntersectionObserver' in window) {
    const obs = new IntersectionObserver((entries, observer) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('is-visible');
          observer.unobserve(e.target);
        }
      });
    }, { threshold: 0.15 });
    animatedItems.forEach(el => obs.observe(el));
  } else {
    animatedItems.forEach(el => el.classList.add('is-visible'));
  }

  // ───────── Smooth scroll para anclas ─────────
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const tgt = document.querySelector(a.getAttribute('href'));
      if (tgt) {
        e.preventDefault();
        tgt.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // ───────── Banner de bienvenida ─────────
  setTimeout(() => {
    const b = document.getElementById('welcome-banner');
    if (b) {
      b.style.transition = 'opacity 1s ease-out';
      b.style.opacity = 0;
      setTimeout(() => b.style.display = 'none', 1000);
    }
  }, 6000);

  // ───────── Rotador “¿Sabías que…?” ─────────
  const facts = [
    'El 48 % de los chilenos decide su voto basándose en debates televisivos.',
    'Sólo 1 de cada 4 electores lee el programa completo de su candidato.',
    'La participación juvenil creció 12 puntos en la última elección.',
    'Más del 70 % de los votantes prioriza seguridad y salud.',
    'Un post viral puede subir 3 puntos la intención de voto en 48 h.'
  ];
  const box = document.getElementById('factHomeBox');
  if (box) {
    let i = 0;
    const show = () => {
      box.style.opacity = 0;
      setTimeout(() => {
        box.textContent = facts[i];
        box.style.opacity = 1;
        i = (i + 1) % facts.length;
      }, 400);
    };
    show();
    setInterval(show, 5000);
  }

  // ───────── Inicializar Swiper ─────────
  new Swiper('.candidatos-swiper', {
    slidesPerView : 'auto',
    spaceBetween  : 24,
    freeMode      : true,
    grabCursor    : true,
    pagination    : {
      el        : '.swiper-pagination',
      clickable : true,
    },
    breakpoints: {
      992: { spaceBetween: 32 }
    }
  });
});
