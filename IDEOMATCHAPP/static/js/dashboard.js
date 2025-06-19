// static/js/dashboard.js

document.addEventListener('DOMContentLoaded', () => {
  // ─── 0. Parse JSON scripts ───────────────────────────────────
  const total = JSON.parse(document.getElementById('total').textContent || '0');
  document.getElementById('bigTotal').textContent = Number(total).toLocaleString('es-CL');

  // ─── 1. Cargar datasets generales desde JSON scripts ───────────
  const datasets = {
    general: {
      bar: JSON.parse(document.getElementById('bar-general').textContent),
      pie: JSON.parse(document.getElementById('pie-general').textContent),
    },
    sexo: {
      bar: JSON.parse(document.getElementById('bar-sexo').textContent),
      pie: JSON.parse(document.getElementById('pie-sexo').textContent),
    },
    edad: {
      bar: JSON.parse(document.getElementById('bar-edad').textContent),
      pie: JSON.parse(document.getElementById('pie-edad').textContent),
    },
    region: {
      bar: JSON.parse(document.getElementById('bar-region').textContent),
      pie: JSON.parse(document.getElementById('pie-region').textContent),
    },
  };

  // ─── 2. Funciones de dibujo de gráficos ────────────────────────
  function drawBar(rawData, targetDiv = 'barChart') {
    // Agrupar por label y sumar valores
    const summary = {};
    rawData.forEach(({ label, value }) => {
      summary[label] = (summary[label] || 0) + value;
    });
    const labels  = Object.keys(summary);
    const counts  = Object.values(summary);
    const tooltip = counts.map(c => `${c} encuesta${c === 1 ? '' : 's'}`);

    Plotly.react(targetDiv, [{
      type : 'bar',
      x    : labels,
      y    : counts,
      marker: { color: '#d90429' },
      text         : tooltip,
      hovertemplate: '%{x}<br><b>%{text}</b><extra></extra>',
      textposition : 'none'
    }], {
      margin: { l: 40, r: 20, t: 30, b: 90 },
      yaxis : {
        title     : 'Encuestados',
        tick0     : 0,
        dtick     : 1,
        rangemode : 'tozero',
        tickformat: ',d'
      },
      xaxis : { tickangle: -35 },
      responsive: true
    });
  }

  function drawPie(data, targetDiv = 'pieChart') {
    const totalVotes = data.reduce((sum, d) => sum + d.value, 0);
    Plotly.react(targetDiv, [{
      type : 'pie',
      hole : 0.45,
      labels: data.map(d => d.label),
      values: data.map(d => d.value),
      textinfo   : 'percent',
      hovertemplate: '%{label}<br><b>%{value}</b>%<extra></extra>'
    }], {
      margin: { t: 20, b: 20, l: 20, r: 20 },
      annotations: [{
        text     : `${totalVotes}<br><span style="font-size:0.7em">encuestas</span>`,
        showarrow: false
      }],
      responsive: true
    });
  }

  // ─── 3. Render inicial (General) ───────────────────────────────
  drawBar(datasets.general.bar, 'barChart');
  drawPie(datasets.general.pie, 'pieChart');

  // ─── 4. Botones Filtros “General/Sexo/Edad/Región” ─────────────
  document.querySelectorAll('.btn-filter').forEach(button => {
    button.addEventListener('click', () => {
      document.querySelectorAll('.btn-filter').forEach(b => b.classList.remove('active'));
      button.classList.add('active');

      const key = button.dataset.key;
      if (datasets[key]) {
        drawBar(datasets[key].bar, 'barChart');
        drawPie(datasets[key].pie, 'pieChart');
      }
    });
  });

  // ─── 5. Filtrado combinado: Sexo, Edad y Región ────────────────
  const prefData     = JSON.parse(document.getElementById('pref-data').textContent);
  const selSexo      = document.getElementById('filterSexo');
  const selEdad      = document.getElementById('filterEdad');
  const selRegion    = document.getElementById('filterRegion');
  const barFilterDiv = 'barFilterChart';

  // 5a) Rellenar rangos de edad (18+)
  (function fillAgeRanges() {
    const ages = prefData.map(r => r.edad).filter(e => e >= 18);
    const minA = Math.min(...ages), maxA = Math.max(...ages);
    let opts = '<option value="">Edad: Todos</option>';
    for (let start = minA; start <= maxA; start += 10) {
      const end = Math.min(start + 9, maxA);
      opts += `<option value="${start}-${end}">${start}-${end}</option>`;
    }
    selEdad.innerHTML = opts;
  })();

  // 5b) Rellenar regiones
  (function fillRegions() {
    const regions = [...new Set(prefData.map(r => r.region))].sort();
    let opts = '<option value="">Región: Todas</option>';
    regions.forEach(r => opts += `<option value="${r}">${r}</option>`);
    selRegion.innerHTML = opts;
  })();

  // 5c) Dibujar gráfico filtrado
  function drawFilteredBar() {
    let data = prefData.slice();
    if (selSexo.value)   data = data.filter(r => r.sexo   === selSexo.value);
    if (selEdad.value) {
      const [lo, hi] = selEdad.value.split('-').map(Number);
      data = data.filter(r => r.edad >= lo && r.edad <= hi);
    }
    if (selRegion.value) data = data.filter(r => r.region === selRegion.value);

    // Agrupar por candidate_nombre
    const summary = {};
    data.forEach(r => {
      const key = r.candidato_nombre;       
      summary[key] = (summary[key] || 0) + 1;
    });

    const labels = Object.keys(summary);
    const counts = Object.values(summary);
    const tooltip = counts.map(c => `${c} usuarios`);

    Plotly.react('barFilterChart', [{
      type : 'bar',
      x    : Object.keys(summary),
      y    : Object.values(summary),
      marker: { color: '#d90429' },
      hovertemplate: '%{x}<br><b>%{y} usuarios</b><extra></extra>'
    }], {
      margin: { l:40, r:20, t:30, b:90 },
      yaxis : { title:'Cantidad de usuarios', dtick:1, rangemode:'tozero', tickformat:',d' },
      xaxis : { tickangle:-35 },
      responsive: true
    });
  }

  // 5d) Listeners & dibujo inicial combinado
  [selSexo, selEdad, selRegion].forEach(el => el.addEventListener('change', drawFilteredBar));
  drawFilteredBar();
});
