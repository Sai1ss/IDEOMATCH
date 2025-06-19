document.addEventListener('DOMContentLoaded', () => {
  // Animación de entrada
  const card = document.querySelector('.signin-card');
  if (card) {
    card.style.opacity = 0;
    card.style.transform = 'translateY(20px)';
    setTimeout(() => {
      card.style.transition = 'all 0.6s ease-out';
      card.style.opacity = 1;
      card.style.transform = 'translateY(0)';
    }, 100);
  }

  // Focus suave en input
  const emailInput = document.querySelector('input[name="email"]');
  if (emailInput) {
    emailInput.addEventListener('focus', () => {
      emailInput.parentElement.classList.add('focused');
    });
    emailInput.addEventListener('blur', () => {
      emailInput.parentElement.classList.remove('focused');
    });
  }
});
