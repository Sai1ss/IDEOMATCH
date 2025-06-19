// miperfil.js - Funcionalidades para la página de perfil con UX mejorado

document.addEventListener('DOMContentLoaded', function () {
  const form = document.querySelector('form');
  const nombreInput = document.getElementById('id_nombre');
  const edadInput = document.getElementById('id_edad');

  const showToast = (message) => {
    const toastContainer = document.createElement('div');
    toastContainer.className = 'toast align-items-center text-bg-success border-0 position-fixed bottom-0 end-0 m-4 show';
    toastContainer.style.zIndex = '1055';
    toastContainer.role = 'alert';
    toastContainer.innerHTML = `
      <div class="d-flex">
        <div class="toast-body">
          ✅ ${message}
        </div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Cerrar"></button>
      </div>
    `;
    document.body.appendChild(toastContainer);

    setTimeout(() => {
      toastContainer.classList.remove('show');
      toastContainer.addEventListener('transitionend', () => toastContainer.remove());
    }, 4000);
  };

  // Añadir animación a los inputs al hacer focus
  const inputs = document.querySelectorAll('input, select');
  inputs.forEach(input => {
    input.addEventListener('focus', () => input.classList.add('animate__animated', 'animate__pulse'));
    input.addEventListener('blur', () => input.classList.remove('animate__animated', 'animate__pulse'));
  });

  form.addEventListener('submit', function (e) {
    let valid = true;

    if (!nombreInput.value.trim()) {
      valid = false;
      nombreInput.classList.add('is-invalid');
    } else {
      nombreInput.classList.remove('is-invalid');
    }

    if (!edadInput.value.trim() || isNaN(edadInput.value) || parseInt(edadInput.value) <= 0) {
      valid = false;
      edadInput.classList.add('is-invalid');
    } else {
      edadInput.classList.remove('is-invalid');
    }

    if (!valid) {
      e.preventDefault();
    } else {
      showToast("¡Datos actualizados correctamente!");
    }
  });
});
