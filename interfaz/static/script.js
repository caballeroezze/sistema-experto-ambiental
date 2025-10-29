let hechos = {};
let preguntas = [];
let indice = 0;
let diagnosticoActualId = null;

// Funciones
async function cargarPreguntas() {
  try {
    const res = await fetch('/hechos'); // usa ruta relativa al mismo server
    if (!res.ok) throw new Error('Error al cargar preguntas: ' + res.status);
    const datos = await res.json();

    // Normalizar distintos formatos que pueda devolver el backend
    preguntas = datos.map(hecho => {
      if (typeof hecho === 'string') {
        return { id: hecho, pregunta: hecho };
      }
      // si es objeto, intentar obtener campos comunes
      const id = hecho.id ?? hecho.key ?? hecho.codigo ?? hecho.name ?? JSON.stringify(hecho);
      const pregunta = hecho.pregunta ?? hecho.texto ?? hecho.label ?? hecho.nombre ?? hecho.descripcion ?? JSON.stringify(hecho);
      return { id, pregunta };
    });

    if (preguntas.length === 0) {
      console.warn('No hay preguntas devueltas por /hechos');
    }
  } catch (error) {
    console.error('Error al cargar preguntas:', error);
    alert('No se pudo conectar con el servidor. Asegúrate de que FastAPI esté corriendo.');
  }
}

async function empezarDiagnostico() {
  await cargarPreguntas();
  hechos = {};
  indice = 0;
  mostrarPregunta();
  document.getElementById('inicio').classList.add('hidden');
  document.getElementById('cuestionario').classList.remove('hidden');
}

function mostrarPregunta() {
  if (preguntas.length === 0) {
    document.getElementById('pregunta-texto').textContent = 'No hay preguntas disponibles.';
    document.getElementById('progreso').style.width = '0%';
    return;
  }

  if (indice < preguntas.length) {
    const pregunta = preguntas[indice];
    document.getElementById('pregunta-texto').textContent = pregunta.pregunta;
    const progreso = ((indice + 1) / preguntas.length) * 100;
    document.getElementById('progreso').style.width = progreso + '%';
  }
  // Mostrar u ocultar el botón "Anterior" según el índice (visible desde la segunda pregunta)
  const btnAnterior = document.getElementById('btn-anterior');
  if (btnAnterior) {
    if (indice > 0 && indice <= preguntas.length - 1) {
      btnAnterior.style.display = 'inline-block';
    } else {
      btnAnterior.style.display = 'none';
    }
  }
}

async function responder(respuesta) {
  if (indice >= preguntas.length) return;

  const id = preguntas[indice].id;
  hechos[id] = respuesta;
  indice++;
if (indice < preguntas.length) {
    mostrarPregunta();
  } else {
    try {
      const res = await fetch('/diagnosticar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ hechos })
      });

      if (!res.ok) throw new Error('Error en diagnóstico: ' + res.status);
      const data = await res.json();
      // esperar que el response_model devuelva { diagnostico: ... }
      const diagnostico = data.diagnostico ?? null;
      // Guardar el ID del diagnóstico para poder descargarlo
      if (diagnostico && diagnostico.diagnostico_id) {
        diagnosticoActualId = diagnostico.diagnostico_id;
      }
      mostrarResultados(diagnostico);
    } catch (error) {
      console.error('Error al enviar diagnóstico:', error);
      alert('Hubo un error al procesar el diagnóstico.');
    }
  }
}


function mostrarResultados(regla) {
  const cont = document.getElementById('resultado-contenido');
  if (!regla) {
    cont.innerHTML = `
      <div class="resultado-card">
        <div class="riesgo-tag riesgo-bajo">RIESGO BAJO</div>
        <div class="resultado-title">Sin diagnóstico aplicable</div>
        <p class="resultado-descripcion">No se encontraron condiciones críticas. La zona parece estar en buen estado.</p>
        <div class="acciones-title">Recomendaciones generales:</div>
        <ul class="acciones-list">
          <li>Mantener monitoreo periódico</li>
          <li>Continuar con buenas prácticas ambientales</li>
          <li>Reportar cualquier cambio significativo</li>
        </ul>
        <div class="info-adicional">
          <div class="ministerio-link">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="16" x2="12" y2="12"></line>
              <line x1="12" y1="8" x2="12.01" y2="8"></line>
            </svg>
            <span>Para más información sobre gestión ambiental en Tierra del Fuego, visita:</span>
          </div>
          <a href="https://prodyambiente.tierradelfuego.gob.ar/informacion-geografica" target="_blank" rel="noopener noreferrer" class="link-ministerio">
            🌿 Ministerio de Producción y Ambiente - Información Geográfica
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
              <polyline points="15 3 21 3 21 9"></polyline>
              <line x1="10" y1="14" x2="21" y2="3"></line>
            </svg>
          </a>
        </div>
      </div>
    `;
  } else {
    let claseRiesgo = 'riesgo-bajo';
    if (regla.riesgo === 'ALTO') claseRiesgo = 'riesgo-alto';
    else if (regla.riesgo === 'MEDIO') claseRiesgo = 'riesgo-medio';

    const acciones = Array.isArray(regla.acciones) ? regla.acciones : [];

    const resumenHtml = preguntas.map(p => {
      const resp = hechos[p.id] ? 'SÍ' : 'NO';
      const cls = hechos[p.id] ? 'respuesta-si' : 'respuesta-no';
      return `<div class="resumen-item"><span>${p.pregunta}</span><span class="${cls}">${resp}</span></div>`;
    }).join('');

    const accionesHtml = acciones.map(a => `<li>${a}</li>`).join('');

    const html = `
      <div class="resultado-card">
        <div class="riesgo-tag ${claseRiesgo}">RIESGO ${regla.riesgo}</div>
        <div class="resultado-title">${regla.titulo}</div>
        <div class="resultado-categoria">${regla.categoria ?? ''}</div>
        <p class="resultado-descripcion">${regla.descripcion ?? ''}</p>
        <div class="justificacion"><strong>Justificación:</strong> ${regla.justificacion ?? ''}</div>
        <div class="acciones-title">Acciones Inmediatas Recomendadas:</div>
        <ul class="acciones-list">
          ${accionesHtml}
        </ul>
        <div class="resumen">
          <strong>Resumen de respuestas:</strong>
          ${resumenHtml}
        </div>
        <div class="info-adicional">
          <div class="ministerio-link">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="16" x2="12" y2="12"></line>
              <line x1="12" y1="8" x2="12.01" y2="8"></line>
            </svg>
            <span>Para más información sobre gestión ambiental en Tierra del Fuego, visita:</span>
          </div>
          <a href="https://prodyambiente.tierradelfuego.gob.ar/informacion-geografica" target="_blank" rel="noopener noreferrer" class="link-ministerio">
            🌿 Ministerio de Producción y Ambiente - Información Geográfica
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
              <polyline points="15 3 21 3 21 9"></polyline>
              <line x1="10" y1="14" x2="21" y2="3"></line>
            </svg>
          </a>
        </div>
      </div>
    `;
    cont.innerHTML = html;

     

  }

  document.getElementById('cuestionario').classList.add('hidden');
  document.getElementById('resultados').classList.remove('hidden');
}

function nuevoDiagnostico() {
  document.getElementById('resultados').classList.add('hidden');
  empezarDiagnostico();
}

function volverInicio() {
  ocultarTodasPantallas();
  document.getElementById('inicio').classList.remove('hidden');
}

function anteriorPregunta() {
  // Solo retroceder si hay una pregunta anterior
  if (indice <= 0) return;
  // Reducir el índice para mostrar la pregunta anterior
  indice = Math.max(0, indice - 1);
  mostrarPregunta();
}

async function cargarHistorial() {
  try {
    const res = await fetch('/historial?limite=50');
    if (!res.ok) throw new Error('Error al cargar historial');
    const data = await res.json();
    mostrarHistorial(data.historial);
  } catch (error) {
    console.error('Error al cargar historial:', error);
    document.getElementById('historial-contenido').innerHTML = '<p class="error">Error al cargar el historial.</p>';
  }
}

async function cargarEstadisticas() {
  try {
    const res = await fetch('/estadisticas');
    if (!res.ok) throw new Error('Error al cargar estadísticas');
    const stats = await res.json();
    mostrarEstadisticas(stats);
  } catch (error) {
    console.error('Error al cargar estadísticas:', error);
    document.getElementById('estadisticas-contenido').innerHTML = '<p class="error">Error al cargar estadísticas.</p>';
  }
}

function mostrarEstadisticas(stats) {
  const { total, por_riesgo, por_categoria } = stats;
  
  const riesgoHtml = Object.entries(por_riesgo || {})
    .map(([riesgo, cantidad]) => {
      const clase = riesgo === 'ALTO' ? 'riesgo-alto' : riesgo === 'MEDIO' ? 'riesgo-medio' : 'riesgo-bajo';
      return `<div class="stat-item"><span class="riesgo-tag ${clase}">${riesgo}</span><span class="stat-numero">${cantidad}</span></div>`;
    })
    .join('');
  
  const categoriaHtml = Object.entries(por_categoria || {})
    .map(([categoria, cantidad]) => `<div class="stat-item"><span>${categoria}</span><span class="stat-numero">${cantidad}</span></div>`)
    .join('');
  
  const html = `
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-titulo">Total de Diagnósticos</div>
        <div class="stat-valor-grande">${total}</div>
      </div>
      <div class="stat-card">
        <div class="stat-titulo">Por Nivel de Riesgo</div>
        ${riesgoHtml}
      </div>
      <div class="stat-card">
        <div class="stat-titulo">Top Categorías</div>
        ${categoriaHtml}
      </div>
    </div>
  `;
  
  document.getElementById('estadisticas-contenido').innerHTML = html;
}

function mostrarHistorial(historial) {
  if (!historial || historial.length === 0) {
    document.getElementById('historial-contenido').innerHTML = '<p>No hay diagnósticos en el historial.</p>';
    return;
  }
  
  const html = historial.map(diag => {
    const claseRiesgo = diag.riesgo === 'ALTO' ? 'riesgo-alto' : diag.riesgo === 'MEDIO' ? 'riesgo-medio' : 'riesgo-bajo';
    const fecha = new Date(diag.fecha).toLocaleString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
    
    // Contar hechos positivos
    const hechosPositivos = Object.values(diag.hechos).filter(v => v === true).length;
    const totalHechos = Object.keys(diag.hechos).length;
    
    return `
      <div class="historial-item">
        <div class="historial-header">
          <div>
            <span class="riesgo-tag ${claseRiesgo}">${diag.riesgo}</span>
            <span class="historial-fecha">${fecha}</span>
          </div>
          <span class="historial-id">#${diag.id}</span>
        </div>
        <div class="historial-titulo">${diag.titulo}</div>
        <div class="historial-categoria">${diag.categoria}</div>
        <div class="historial-stats">
          <span>📊 Indicadores detectados: ${hechosPositivos}/${totalHechos}</span>
        </div>
        <details class="historial-detalles">
          <summary>Ver detalles completos</summary>
          <div class="historial-contenido-expandido">
            <p><strong>Descripción:</strong> ${diag.descripcion}</p>
            <p><strong>Justificación:</strong> ${diag.justificacion}</p>
            <div><strong>Acciones recomendadas:</strong></div>
            <ul>${diag.acciones.map(a => `<li>${a}</li>`).join('')}</ul>
          </div>
        </details>
      </div>
    `;
  }).join('');
  
  document.getElementById('historial-contenido').innerHTML = html;
}

async function verHistorial() {
  ocultarTodasPantallas();
  document.getElementById('historial').classList.remove('hidden');
  await cargarEstadisticas();
  await cargarHistorial();
}

function ocultarTodasPantallas() {
  document.getElementById('inicio').classList.add('hidden');
  document.getElementById('cuestionario').classList.add('hidden');
  document.getElementById('resultados').classList.add('hidden');
  document.getElementById('historial').classList.add('hidden');
  document.getElementById('diagnosticos-multiples')?.classList.add('hidden');
}

function descargarPDF() {
  if (!diagnosticoActualId) {
    alert('No hay diagnóstico disponible para descargar.');
    return;
  }
  
  // Abrir el PDF en una nueva pestaña o descargar
  window.open(`/descargar-pdf/${diagnosticoActualId}`, '_blank');
}

function descargarHistorialPDF() {
  window.open('/descargar-historial-pdf?limite=50', '_blank');
}

async function verTodosDiagnosticos() {
  if (Object.keys(hechos).length === 0) {
    alert('No hay hechos disponibles para analizar.');
    return;
  }
  
  try {
    const res = await fetch('/diagnosticar-multiple', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ hechos })
    });
    
    if (!res.ok) throw new Error('Error al obtener diagnósticos múltiples');
    const data = await res.json();
    
    mostrarDiagnosticosMultiples(data.diagnosticos, data.total);
  } catch (error) {
    console.error('Error al obtener diagnósticos múltiples:', error);
    alert('Error al obtener todos los diagnósticos.');
  }
}

function mostrarDiagnosticosMultiples(diagnosticos, total) {
  const cont = document.getElementById('diagnosticos-multiples-contenido');
  
  if (!diagnosticos || diagnosticos.length === 0) {
    cont.innerHTML = `
      <div class="resultado-card">
        <p class="resultado-descripcion">No se encontraron problemas específicos. La zona parece estar en condiciones aceptables.</p>
      </div>
    `;
  } else {
    const html = `
      <div class="multiple-summary">
        <p><strong>Se detectaron ${total} problema(s) ambiental(es)</strong></p>
        <p class="texto-info">Los problemas están ordenados por nivel de riesgo (ALTO → MEDIO → BAJO)</p>
      </div>
      ${diagnosticos.map((regla, index) => {
        const claseRiesgo = regla.riesgo === 'ALTO' ? 'riesgo-alto' : regla.riesgo === 'MEDIO' ? 'riesgo-medio' : 'riesgo-bajo';
        const acciones = Array.isArray(regla.acciones) ? regla.acciones : [];
        const accionesHtml = acciones.map(a => `<li>${a}</li>`).join('');
        
        return `
          <div class="diagnostico-multiple-card">
            <div class="multiple-header">
              <span class="multiple-numero">#${index + 1}</span>
              <span class="riesgo-tag ${claseRiesgo}">RIESGO ${regla.riesgo}</span>
            </div>
            <div class="resultado-title">${regla.titulo}</div>
            <div class="resultado-categoria">${regla.categoria ?? ''}</div>
            <p class="resultado-descripcion">${regla.descripcion ?? ''}</p>
            <div class="justificacion"><strong>Justificación:</strong> ${regla.justificacion ?? ''}</div>
            <details class="acciones-expandibles">
              <summary class="acciones-summary">Ver acciones recomendadas (${acciones.length})</summary>
              <ul class="acciones-list">
                ${accionesHtml}
              </ul>
            </details>
          </div>
        `;
      }).join('')}
    `;
    cont.innerHTML = html;
  }
  
  ocultarTodasPantallas();
  document.getElementById('diagnosticos-multiples').classList.remove('hidden');
}

function volverAlResultado() {
  ocultarTodasPantallas();
  document.getElementById('resultados').classList.remove('hidden');
}

// Asignar eventos
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('btn-comenzar')?.addEventListener('click', empezarDiagnostico);
  document.getElementById('btn-si')?.addEventListener('click', () => responder(true));
  document.getElementById('btn-no')?.addEventListener('click', () => responder(false));
  document.getElementById('btn-nuevo')?.addEventListener('click', nuevoDiagnostico);
  document.getElementById('btn-volver-inicio')?.addEventListener('click', volverInicio);
  document.getElementById('btn-anterior')?.addEventListener('click', anteriorPregunta);
  document.getElementById('btn-ver-historial')?.addEventListener('click', verHistorial);
  document.getElementById('btn-historial-inicio')?.addEventListener('click', verHistorial);
  document.getElementById('btn-volver-inicio-historial')?.addEventListener('click', volverInicio);
  document.getElementById('btn-descargar-pdf')?.addEventListener('click', descargarPDF);
  document.getElementById('btn-descargar-historial-pdf')?.addEventListener('click', descargarHistorialPDF);
  document.getElementById('btn-ver-todos-diagnosticos')?.addEventListener('click', verTodosDiagnosticos);
  document.getElementById('btn-volver-resultado')?.addEventListener('click', volverAlResultado);
  document.getElementById('btn-volver-inicio-multiple')?.addEventListener('click', volverInicio);
});