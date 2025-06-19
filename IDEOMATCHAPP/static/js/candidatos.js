
 
document.addEventListener('DOMContentLoaded', () => {
  /* refs */
  const track     = document.querySelector('.carousel-track');
  const container = document.querySelector('.carousel-track-container');
  const cards     = Array.from(track.children);
  const btnNext   = document.getElementById('nextBtn');
  const btnPrev   = document.getElementById('prevBtn');

  /* state */
  let index = 0;

  /* layout */
  const setLayout = () => {
    const viewport = container.clientWidth;
    cards.forEach(c => {
      c.style.minWidth = c.style.maxWidth = `${viewport}px`;
    });
  };

  const updatePos = () => {
    /* Animación de la card */
    cards.forEach(c => c.classList.remove('card-animate'));
    void cards[index].offsetWidth;              // reflow
    cards[index].classList.add('card-animate');

    const offset = cards[index].offsetLeft;
    track.style.transform = `translateX(-${offset}px)`;
  };

  /* nav */
  btnNext.addEventListener('click', () => {
    index = (index + 1) % cards.length;
    updatePos();
  });
  btnPrev.addEventListener('click', () => {
    index = (index - 1 + cards.length) % cards.length;
    updatePos();
  });

  /* responsive */
  window.addEventListener('resize', () => { setLayout(); updatePos(); });

  /* init */
  setLayout();
  updatePos();

  /* -------- Modal -------- */
  const modal    = document.getElementById('candidateModal');
  const closeBtn = modal.querySelector('.close-btn');
  const [mImg,mName,mParty,mTray,mProp,mLider] =
        ['modalImage','modalName','modalPartido',
         'modalTrayectoria','modalPropuesta','modalLiderazgo']
        .map(id => document.getElementById(id));

  cards.forEach(card => card.addEventListener('click', () => {
    mName.textContent  = card.dataset.name;
    mParty.textContent = card.dataset.partido;
    mTray.textContent  = card.dataset.trayectoria;
    mProp.textContent  = card.dataset.propuesta;
    mLider.textContent = card.dataset.liderazgo;
    mImg.src           = card.dataset.img;
    modal.style.display = 'flex';
  }));

  closeBtn.addEventListener('click', () => modal.style.display = 'none');
  window.addEventListener('click', e => { if (e.target === modal) modal.style.display = 'none'; });
});

/* ——— ② ROTADOR DE DATOS CURIOSOS ——— */
document.addEventListener('DOMContentLoaded', () => {
  const facts = [
    'El 62 % de los votantes se decide la última semana de campaña.',
    'Sólo 3 de cada 10 personas recuerda el programa completo de su candidato.',
    'La participación juvenil subió 12 puntos en la elección pasada.',
    'Un debate televisivo puede mover hasta 5 puntos porcentuales en intención de voto.',
    'Más del 70 % de los electores quiere ver propuestas sobre seguridad y salud.'
  ];
  const box = document.getElementById('factBox');
  let idx = 0;
  const showFact = () => {
    box.style.opacity = 0;
    setTimeout(() => {
      box.textContent = facts[idx];
      box.style.opacity = 1;
      idx = (idx + 1) % facts.length;
    }, 400);
  };
  showFact();
  setInterval(showFact, 6000);
});

/**
 * Carrusel 
 */
document.addEventListener('DOMContentLoaded', () => {
  /* refs carrusel */
  const track     = document.querySelector('.carousel-track');
  const container = document.querySelector('.carousel-track-container');
  const cards     = Array.from(track.children);
  const btnNext   = document.getElementById('nextBtn');
  const btnPrev   = document.getElementById('prevBtn');

  /* ---------- ① Datos de cada candidato ---------- */
  const candidateDetails = {
    /* … (igual que antes, no se modifica) … */
    "Carolina Tohá": {
      trayectoria: "Abogada (U. de Chile) y doctora en Cs. Políticas. Fue diputada, alcaldesa de Santiago y ministra del Interior, con 30 años de liderazgo público.",
      propuesta:   "Seguridad efectiva, crecimiento inclusivo y modernización digital del Estado (‘Chile Seguro y Sostenible’).",
      liderazgo:   "Gestora orientada a resultados, experta en acuerdos transversales y cercana a la ciudadanía."
    },
    "Evelyn Matthei": {
      trayectoria: "Economista, ex diputada, ex senadora y ex ministra del Trabajo. Alcaldesa de Providencia desde 2016.",
      propuesta:   "Plan ‘Chile Seguro y en Marcha’: seguridad integral, alivio tributario a pymes, listas de espera 0 y vivienda bien localizada.",
      liderazgo:   "Firme, pragmática y directa; alta valoración por gestión eficiente."
    },
    "Franco Parisi": {
      trayectoria: "Ingeniero comercial y PhD en Finanzas (U. Georgia). Académico, consultor del BM/BID y divulgador económico.",
      propuesta:   "Ahorro previsional vía consumo (APVC), impulso a startups regionales y Estado 100 % digital.",
      liderazgo:   "Disruptivo y participativo; comunica economía en lenguaje claro a través de plataformas digitales."
    },
    "José Antonio Kast": {
      trayectoria: "Abogado PUC, ex diputado (2002-2018), fundador del Partido Republicano y finalista presidencial 2017-2021.",
      propuesta:   "‘Chile Firme y Seguro’: fuerza antinarcóticos, megacárceles, rebaja de impuesto a empresas regionales y bono natalidad.",
      liderazgo:   "Discurso directo y doctrinario; moviliza bases ciudadanas con encuentros presenciales y digitales."
    },
    "Jeannette Jara": {
      trayectoria: "Administradora pública y abogada (Usach). Subsecretaria de Previsión Social y ministra del Trabajo 2022-25; impulsó Ley 40 Horas.",
      propuesta:   "‘Chile Justo, Seguro y Próspero’: crecimiento con distribución, derechos sociales garantizados y seguridad integral.",
      liderazgo:   "Pragmática y dialogante; experta en consensos entre sindicatos y sector privado."
    },
    "Jaime Mulet": {
      trayectoria: "Abogado, máster en Gestión Pública. Gobernador del Huasco y diputado cuatro periodos; líder regionalista.",
      propuesta:   "‘Chile Policéntrico’: descentralización profunda y transición ecológica con energía verde y soberanía regional.",
      liderazgo:   "Colaborativo y de terreno; promueve poder compartido con autoridades locales y comunidades."
    },
    "Gonzalo Winter": {
      trayectoria: "Abogado y dirigente estudiantil 2011. Diputado desde 2018 y presidente de la comisión de Constitución (2023-24).",
      propuesta:   "‘Chile que Confía’: gobierno digital, fondo verde de innovación y modernización del Servicio Civil.",
      liderazgo:   "Colaborativo y tecnocrático; combina participación ciudadana con evidencia técnica."
    },
    "Johannes Kaiser": {
      trayectoria: "Divulgador libertario y diputado (2022-26). Creador del canal ‘El Nacional-Libertario’.",
      propuesta:   "‘Chile Libre y Responsable’: flat tax 15 %, democracia directa y Estado base cero.",
      liderazgo:   "Oratoria directa y streaming semanal; vota propuestas con su comunidad online."
    }
  };

  /* state */
  let index = 0;

  /* ---------- ② Funciones de layout & scroll + animaciones ---------- */
  const setLayout = () => {
    const w = container.clientWidth;
    cards.forEach(c => c.style.minWidth = c.style.maxWidth = w + 'px');
  };

  const infoBox = document.getElementById('candidateInfo');

  const renderInfo = () => {
    const name = cards[index].dataset.name;
    const data = candidateDetails[name] || {trayectoria:"", propuesta:"", liderazgo:""};
    infoBox.innerHTML = `
      <h3 class="text-center fw-bold">${name}</h3>
      <h4>Trayectoria y formación</h4>
      <p>${data.trayectoria}</p>
      <h4>Propuesta de gobierno</h4>
      <p>${data.propuesta}</p>
      <h4>Estilo de liderazgo</h4>
      <p>${data.liderazgo}</p>
    `;
  };

  const updatePos = () => {
    /* animar card */
    cards.forEach(c => c.classList.remove('card-animate'));
    void cards[index].offsetWidth;
    cards[index].classList.add('card-animate');

    /* mover carrusel */
    track.style.transform = `translateX(-${cards[index].offsetLeft}px)`;

    /* animar info */
    infoBox.classList.remove('info-animate');
    renderInfo();
    void infoBox.offsetWidth;
    infoBox.classList.add('info-animate');
  };

  /* ---------- ④ Navegación ---------- */
  btnNext.addEventListener('click', () => { index = (index + 1) % cards.length; updatePos(); });
  btnPrev.addEventListener('click', () => { index = (index - 1 + cards.length) % cards.length; updatePos(); });
  window.addEventListener('resize', () => { setLayout(); updatePos(); });

  /* ---------- ⑤ Init ---------- */
  setLayout();
  updatePos();

  /* ---------- ⑥ Modal (igual) ---------- */
  const modal    = document.getElementById('candidateModal');
  const closeBtn = modal.querySelector('.close-btn');
  const [mImg,mName,mParty,mTray,mProp,mLider] =
        ['modalImage','modalName','modalPartido','modalTrayectoria','modalPropuesta','modalLiderazgo']
        .map(id => document.getElementById(id));

  cards.forEach(card => card.addEventListener('click', () => {
    mName.textContent  = card.dataset.name;
    mParty.textContent = card.dataset.partido;
    mTray.textContent  = card.dataset.trayectoria;
    mProp.textContent  = card.dataset.propuesta;
    mLider.textContent = card.dataset.liderazgo;
    mImg.src           = card.dataset.img;
    modal.style.display = 'flex';
  }));
  closeBtn.addEventListener('click', () => modal.style.display = 'none');
  window.addEventListener('click', e => { if (e.target === modal) modal.style.display = 'none'; });
});
