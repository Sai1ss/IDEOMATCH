
document.addEventListener('DOMContentLoaded', () => {
  const animated = document.querySelectorAll('.section-title, .cf-card, .cf-flow .node, .cf-flow .arrow');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries, ob) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('fade-in-up');
          ob.unobserve(e.target);
        }
      });
    }, { threshold: .15 });
    animated.forEach(el => io.observe(el));
  } else {
    animated.forEach(el => el.classList.add('fade-in-up'));
  }
});

/* Simple CSS */
const style = document.createElement('style');
style.innerHTML = `
.fade-in-up{opacity:0;transform:translateY(20px);animation:fiu .6s forwards}
@keyframes fiu{to{opacity:1;transform:none}}
`;
document.head.appendChild(style);
