/* ────────────────────────────────────────────────
   IdeoMatch · Radar individual de afinidad (Chart.js)
   ──────────────────────────────────────────────── */

document.addEventListener('DOMContentLoaded', () => {
  /* ① lee el JSON inyectado por la view ------------------------- */
  const dataNode = document.getElementById('radar-data');
  if (!dataNode) return;                       

  let raw;
  try { raw = JSON.parse(dataNode.textContent); }
  catch { console.warn('⚠️ Radar – datos inválidos'); return; }

  if (!Array.isArray(raw) || !raw.length) return;  

  /* ② ejes y valores ------------------------------------------- */
  const labels  = raw.map(d => d.nombre);
  const valores = raw.map(d => d.pct);

  /* ③ canvas & gráfico ----------------------------------------- */
  const canvas = document.getElementById('radarChart');
  if (!canvas) return;

  // Si ya hay un gráfico, lo destruye para evitar duplicados
  if (canvas._chartInstance) canvas._chartInstance.destroy();

  const cfg = {
    type : 'radar',
    data : {
      labels,
      datasets : [{
        label               : 'Afinidad %',
        data                : valores,
        borderColor         : '#d90429',
        backgroundColor     : 'rgba(217,4,41,.25)',
        pointBackgroundColor: '#d90429',
        pointRadius         : 4,
        borderWidth         : 2
      }]
    },
    options : {
      responsive: true,
      maintainAspectRatio: false,   
      scales: {
        r: {
          suggestedMin : 0,
          suggestedMax : 100,
          ticks : {
            stepSize : 20,
            callback : v => v + '%',
            color    : '#374151'
          },
          grid      : { color:'#e3e3e3' },
          angleLines: { color:'#e3e3e3' }
        }
      },
      plugins: {
        legend : { display:false },
        tooltip: {
          callbacks:{
            label: ctx => `${ctx.label}: ${ctx.parsed.r}%`
          }
        }
      }
    }
  };

  canvas._chartInstance = new Chart(canvas, cfg);
});
