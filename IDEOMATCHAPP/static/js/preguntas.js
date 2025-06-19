document.addEventListener('DOMContentLoaded', () => {
  const tabla = document.getElementById('tabla-preguntas');
  const formContainer = document.getElementById('form-pregunta-container');
  const form = document.getElementById('form-pregunta');
  const btnNueva = document.getElementById('btn-nueva');
  const btnCancelar = document.getElementById('btn-cancelar');
  const btnGuardar = document.getElementById('btn-guardar');
  const tituloForm = document.getElementById('form-titulo');
  const inpPk = document.getElementById('inp-pk');
  const inpOrden = document.getElementById('inp-orden');
  const inpTexto = document.getElementById('inp-texto');
  const errOrden = document.getElementById('err-orden');
  const errTexto = document.getElementById('err-texto');

  // Abrir formulario en modo "nueva"
  btnNueva.addEventListener('click', () => {
    tituloForm.textContent = 'Crear Pregunta';
    btnGuardar.textContent = 'Crear';
    inpPk.value = '';
    inpOrden.value = '';
    inpTexto.value = '';
    clearErrors();
    formContainer.classList.remove('hidden');
    inpOrden.focus();
  });

  // Cancelar edición/creación
  btnCancelar.addEventListener('click', () => {
    formContainer.classList.add('hidden');
  });

  // Delegación de botones "Editar" y "Borrar"
  tabla.addEventListener('click', e => {
    const tr = e.target.closest('tr[data-id]');
    if (!tr) return;
    const pk = tr.dataset.id;

    // Editar
    if (e.target.matches('.btn-editar')) {
      tituloForm.textContent = 'Editar Pregunta';
      btnGuardar.textContent = 'Guardar cambios';
      inpPk.value = pk;
      inpOrden.value = tr.querySelector('.td-orden').textContent.trim();
      inpTexto.value = tr.querySelector('.td-texto').textContent.trim();
      clearErrors();
      formContainer.classList.remove('hidden');
      inpOrden.focus();
    }

    // Borrar
    if (e.target.matches('.btn-borrar')) {
      if (!confirm('¿Seguro que quieres eliminar esta pregunta?')) return;
      // Llamada AJAX al endpoint de borrado
      fetch(`/preguntas/${pk}/eliminar/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
      }).then(resp => {
        if (resp.ok) location.reload();
        else alert('Error al eliminar');
      });
    }
  });

  // Enviar formulario (crear o actualizar) vía AJAX
  form.addEventListener('submit', e => {
    e.preventDefault();
    clearErrors();
    const pk = inpPk.value;
    const url = pk
      ? `/preguntas/${pk}/editar/`
      : `/preguntas/nueva/`;
    const data = new FormData(form);

    fetch(url, {
      method: 'POST',
      body: data,
      headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
      }
    }).then(async resp => {
      if (resp.ok) {
        location.reload();
      } else if (resp.status === 400) {
        const errors = await resp.json(); 
        if (errors.orden) {
          inpOrden.classList.add('is-invalid');
          errOrden.textContent = errors.orden[0];
        }
        if (errors.texto) {
          inpTexto.classList.add('is-invalid');
          errTexto.textContent = errors.texto[0];
        }
      } else {
        alert('Error en el servidor');
      }
    });
  });

  function clearErrors() {
    [inpOrden, inpTexto].forEach(i => {
      i.classList.remove('is-invalid');
    });
    errOrden.textContent = '';
    errTexto.textContent = '';
  }
});
