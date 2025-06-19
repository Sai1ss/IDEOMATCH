document.addEventListener('DOMContentLoaded', function () {
  const form = document.querySelector('form');
  const emailInput = document.getElementById('id_email');
  const passwordInput = document.getElementById('id_password');

  form.addEventListener('submit', function (e) {
    let valid = true;

    if (emailInput && emailInput.value.trim() === '') {
      valid = false;
      emailInput.classList.add('is-invalid');
    } else if (emailInput) {
      emailInput.classList.remove('is-invalid');
    }

    if (passwordInput && passwordInput.value.trim() === '') {
      valid = false;
      passwordInput.classList.add('is-invalid');
    } else if (passwordInput) {
      passwordInput.classList.remove('is-invalid');
    }

    if (!valid) {
      e.preventDefault();
    } else {
      Swal.fire({
        icon: 'success',
        title: '¡Cambios guardados!',
        text: 'Tu configuración ha sido actualizada correctamente.',
        confirmButtonColor: '#d90429'
      });
    }
  });

  document.getElementById('exportDataBtn').addEventListener('click', function () {
    Swal.fire({
      icon: 'info',
      title: 'Exportación en curso',
      text: 'Tus datos están siendo empaquetados...',
      showConfirmButton: false,
      timer: 2500,
      background: '#fff',
      color: '#2c3e50',
      iconColor: '#d90429'
    });
  });

  document.getElementById('deleteAccountBtn').addEventListener('click', function () {
    Swal.fire({
      icon: 'warning',
      title: '¿Estás seguro?',
      text: 'Esta acción eliminará tu cuenta de forma permanente.',
      showCancelButton: true,
      confirmButtonColor: '#d90429',
      cancelButtonColor: '#6c757d',
      confirmButtonText: 'Sí, eliminar',
      cancelButtonText: 'Cancelar'
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.fire('Cuenta eliminada', 'Tu cuenta ha sido eliminada correctamente.', 'success');
      }
    });
  });

  document.getElementById('changePasswordBtn').addEventListener('click', function () {
    const newPass = document.getElementById('new_password').value;
    const confirmPass = document.getElementById('confirm_password').value;

    if (newPass === '' || confirmPass === '') {
      Swal.fire('Campos vacíos', 'Por favor completa ambos campos de contraseña.', 'warning');
    } else if (newPass !== confirmPass) {
      Swal.fire('No coinciden', 'Las contraseñas no coinciden.', 'error');
    } else {
      Swal.fire('¡Contraseña actualizada!', 'Tu contraseña ha sido cambiada exitosamente.', 'success');
    }
  });
});
