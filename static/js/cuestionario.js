/**
 * IDEOMATCH – Cuestionario (wizard simple)
 * Script principal para la navegación y animación del cuestionario tipo wizard.
 * Gestiona el avance, retroceso, validación y animaciones de los bloques de preguntas.
 */
document.addEventListener("DOMContentLoaded", () => {

  /* ------------- Referencias a elementos del DOM ---------------- */
  const blocks = [...document.querySelectorAll(".pregunta-block")]; // Bloques de preguntas
  const prev   = document.getElementById("btn-prev");               // Botón anterior
  const next   = document.getElementById("btn-next");               // Botón siguiente
  const submit = document.getElementById("btn-submit");             // Botón enviar
  const bar    = document.getElementById("progress-bar");           // Barra de progreso

  /* ------------- Estado del cuestionario ------------------------ */
  let idx   = 0;                        // Índice actual del bloque mostrado
  const total = blocks.length;          // Total de bloques/preguntas

  /**
   * Animación de entrada/salida para los bloques de preguntas.
   * Utiliza keyframes gentleIn/gentleOut definidos en CSS o inyectados abajo.
   * @param {HTMLElement} el - Elemento a animar
   * @param {string} dir - Dirección: "In" para mostrar, "Out" para ocultar
   */
  const animate = (el, dir) => {
    el.style.animation = `gentle${dir} .45s ease both`;
    // both: aplica forwards y backwards para preservar opacidad
  };

  /**
   * Muestra el bloque de pregunta correspondiente al índice dado.
   * Actualiza controles, barra de progreso y aplica animaciones.
   * @param {number} i - Índice del bloque a mostrar
   */
  function show(i) {
    animate(blocks[idx], "Out");           // Oculta el bloque actual
    idx = i;                               // Actualiza el índice
    animate(blocks[idx], "In");            // Muestra el nuevo bloque

    // Oculta todos los bloques excepto el actual
    blocks.forEach((b, k) => b.classList.toggle("d-none", k !== idx));

    // Control de botones
    prev.disabled = idx === 0;
    next.classList.toggle("d-none", idx === total - 1);
    submit.classList.toggle("d-none", idx !== total - 1);

    // Actualiza barra de progreso
    bar.style.width = `${(idx / total) * 100}%`;

    // Desplaza la ventana hacia arriba para mejor experiencia
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  /* ------------- Navegación: Botón Anterior --------------------- */
  prev.onclick = () => {
    if (idx > 0) show(idx - 1);
  };

  /* ------------- Navegación: Botón Siguiente -------------------- */
  next.onclick = () => {
    // Valida que alguna alternativa esté seleccionada antes de avanzar
    const radios = blocks[idx].querySelectorAll("input[type=radio]");
    if (![...radios].some(r => r.checked)) {
      blocks[idx].classList.add("border-danger"); // Marca error visual
      return;
    }
    blocks[idx].classList.remove("border-danger");
    if (idx < total - 1) show(idx + 1);
  };

  /* ------------- Keyframes inyectados (fallback CSS) ------------ */
  // Si la hoja CSS no está cargada, se inyectan los keyframes necesarios
  const style = document.createElement("style");
  style.innerHTML = `
    @keyframes gentleIn  {
      from { opacity:0; transform:translateY(30px); }
      to   { opacity:1; transform:none; }
    }
    @keyframes gentleOut {
      from { opacity:1; transform:none; }
      to   { opacity:0; transform:translateY(-30px); }
    }
  `;
  document.head.appendChild(style);

  /* ------------- Inicialización del wizard ---------------------- */
  show(0); // Muestra el primer bloque al cargar
});
