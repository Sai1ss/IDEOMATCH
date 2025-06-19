document.addEventListener('DOMContentLoaded', () => {
  // Auto-desvanecer cualquier alerta de Django a los 5s
  setTimeout(() => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(a => {
      a.classList.remove('show');
      a.classList.add('fade');
    });
  }, 5000);
});
