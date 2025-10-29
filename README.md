# Sistema Experto Ambiental

*Sistema experto basado en reglas para evaluar riesgos ambientales en zonas urbanas mediante análisis de indicadores observables y recomendación de acciones inmediatas.*

## 1) Descripción
Este sistema experto permite realizar diagnósticos ambientales a través de un cuestionario interactivo que evalúa 7 indicadores observables y aplica 8 reglas de inferencia para determinar el nivel de riesgo ambiental y proporcionar recomendaciones específicas.

### Características principales:

**Core del Sistema:**
* ✅ Base de conocimiento con 8 reglas ambientales
* ✅ Motor de inferencia con encadenamiento hacia adelante
* ✅ Motor de inferencia múltiple (detecta todos los problemas simultáneamente)
* ✅ Explicaciones detalladas con justificaciones
* ✅ Clasificación de riesgos (ALTO, MEDIO, BAJO)
* ✅ Recomendaciones de acciones inmediatas

**Interfaz y Experiencia:**
* ✅ Interfaz web moderna y responsive
* ✅ Cuestionario interactivo paso a paso
* ✅ Barra de progreso visual
* ✅ Botón "Anterior" para revisar respuestas
* ✅ Vista de todos los problemas detectados

**Persistencia y Reportes:**
* ✅ Base de datos SQLite para historial
* ✅ Estadísticas generales de diagnósticos
* ✅ Exportación a PDF de diagnósticos individuales
* ✅ Exportación a PDF del historial completo
* ✅ Consulta de diagnósticos previos

**Calidad y Testing:**
* ✅ 23 tests unitarios con cobertura completa
* ✅ Tests del motor de inferencia
* ✅ Tests de la base de conocimiento
* ✅ Validación de integridad de reglas

## 2) Instalación
### Requisitos previos

Python 3.8 o superior
pip (gestor de paquetes de Python)

Pasos de instalación

* *Descargar el proyecto*
- Si tienes el proyecto en una carpeta
cd PROYECTO FINAL-Diagnotico Ambiental

* *Crear entorno virtual (opcional pero recomendado)*

python -m venv venv

- Activar entorno virtual
En Windows:
venv\Scripts\activate

En Linux/Mac:
source venv/bin/activate

* *Instalar dependencias*
pip install -r requirements.txt

## 3) Ejecución del Sistema
* Iniciar el servidor FastAPI
uvicorn main:app --reload
* Abrir el navegador

Ir a: http://localhost:8000
O: http://127.0.0.1:8000

## 4) Uso del Sistema
### Flujo de trabajo

#### 🏠 **Pantalla de Inicio**
* Lee la descripción del sistema
* Haz clic en "Comenzar Diagnóstico →"
* O haz clic en "Ver Historial de Diagnósticos" para revisar diagnósticos previos

#### 📋 **Cuestionario Interactivo**
* Responde 7 preguntas sobre indicadores ambientales
* Opciones: SÍ o NO
* Usa el botón "← Anterior" si necesitas revisar una respuesta
* La barra de progreso muestra tu avance
* Puedes usar "Volver al Inicio" para cancelar

#### 📊 **Resultados del Diagnóstico**
* **Nivel de Riesgo:** ALTO / MEDIO / BAJO (con código de color)
* **Título del Problema:** Identificación clara del problema
* **Categoría:** Tipo de problema ambiental
* **Descripción:** Explicación del problema detectado
* **Justificación:** Por qué el sistema llegó a esta conclusión
* **Acciones Recomendadas:** Lista de acciones a tomar
* **Resumen de Respuestas:** Todas tus respuestas del cuestionario

**Opciones disponibles:**
* 🔄 "Nuevo Diagnóstico" - Evaluar otra zona
* 📄 "Descargar PDF" - Exportar el diagnóstico actual
* 🔍 "Ver Todos los Problemas" - Ver todas las reglas que se cumplen
* 📚 "Ver Historial" - Acceder al historial completo

#### 🔍 **Vista de Múltiples Problemas**
* Muestra TODAS las reglas ambientales que se cumplen con los indicadores detectados
* Ordenadas por prioridad (ALTO → MEDIO → BAJO)
* Cada problema con sus propias acciones recomendadas
* Útil para tener una visión completa de la situación

#### 📚 **Historial de Diagnósticos**
* **Estadísticas generales:** Total de diagnósticos, distribución por riesgo y categorías
* **Lista de diagnósticos previos** con fecha, riesgo y detalles
* **Detalles expandibles** para cada diagnóstico
* **Descarga del historial en PDF** 

## 5) Estructura del Proyecto

```
PROYECTO FINAL - Diagnostico Ambiental/
│
├── .venv/                          # Entorno virtual
├── main.py                         # API FastAPI - Punto de entrada principal
├── reglas.py                       # Base de conocimiento + Motores de inferencia
├── modelos.py                      # Modelos Pydantic para validación de datos
├── database.py                     # ⭐ Gestión de base de datos SQLite
├── pdf_generator.py                # ⭐ Generación de reportes PDF
├── test_motor_inferencia.py       # ⭐ Tests unitarios (23 tests)
├── pytest.ini                      # ⭐ Configuración de pytest
├── diagnosticos_ambientales.db    # ⭐ Base de datos (generada automáticamente)
├── README.md                       # Documentación completa
├── requirements.txt                # Dependencias del proyecto
│
└── interfaz/
    ├── app_visual.py              # Script de apertura automática del navegador
    ├── templates/
    │   ├── index.html             # Interfaz principal (SPA)
    │   └── resultado.html         # Template alternativo
    │
    └── static/
        ├── script.js              # Lógica del frontend (con historial y PDF)
        └── style.css              # Estilos modernos y responsive
```

⭐ = Nuevas funcionalidades implementadas

## 6) Tecnologías Utilizadas

**Backend:**
* **FastAPI 0.100+** - Framework web moderno y rápido
* **Uvicorn** - Servidor ASGI de alto rendimiento
* **Pydantic 2.0+** - Validación de datos con type hints
* **Jinja2** - Motor de templates HTML
* **SQLite3** - Base de datos embebida para persistencia
* **ReportLab 4.0+** - Generación profesional de PDFs
* **Pytest 7.4+** - Framework de testing

**Frontend:**
* **HTML5** - Estructura semántica
* **CSS3** - Estilos modernos con gradientes y animaciones
* **JavaScript (Vanilla)** - Sin dependencias de frameworks
* **Fetch API** - Comunicación asíncrona con el backend

**APIs REST Implementadas:**
* `GET /` - Página principal
* `GET /hechos` - Obtener indicadores observables
* `POST /diagnosticar` - Realizar diagnóstico (guarda en BD)
* `POST /diagnosticar-multiple` - Obtener todas las reglas que se cumplen
* `GET /historial` - Obtener historial de diagnósticos
* `GET /diagnostico/{id}` - Obtener diagnóstico específico
* `GET /estadisticas` - Obtener estadísticas generales
* `GET /descargar-pdf/{id}` - Descargar PDF de diagnóstico
* `GET /descargar-historial-pdf` - Descargar PDF del historial

## 7) Licencia
Este proyecto es de código abierto y está disponible para uso educativo y profesional.

## 8) Testing

El proyecto incluye una suite completa de tests unitarios para garantizar la calidad del sistema.

### Ejecutar Tests

```bash
# Ejecutar todos los tests
pytest test_motor_inferencia.py -v

# Ejecutar con cobertura detallada
pytest test_motor_inferencia.py -v --tb=short

# Ejecutar tests específicos
pytest test_motor_inferencia.py::TestMotorInferencia -v
```

### Cobertura de Tests

El proyecto incluye **23 tests unitarios** organizados en 4 categorías:

1. **TestMotorInferencia** (8 tests)
   - Tests del motor de inferencia principal
   - Validación de reglas específicas
   - Verificación de estructura de resultados

2. **TestMotorInferenciaMultiple** (6 tests)
   - Tests del motor de inferencia múltiple
   - Validación de ordenamiento por prioridad
   - Verificación de detección de múltiples problemas

3. **TestBaseConocimiento** (6 tests)
   - Validación de integridad de reglas
   - Verificación de IDs únicos
   - Validación de estructura de hechos observables

4. **TestCasosEspecificos** (3 tests)
   - Tests de casos del dominio ambiental
   - Validación de prioridades
   - Verificación de combinaciones específicas

**Resultado:** ✅ 23/23 tests pasando

## 9) Checklist de Verificación
Antes de presentar o usar el sistema, verifica:

**Instalación:**
- [ ] Python 3.8+ instalado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Base de datos SQLite creada automáticamente

**Ejecución:**
- [ ] Servidor inicia correctamente (`uvicorn main:app --reload`)
- [ ] Navegador abre en http://localhost:8000
- [ ] Sin errores en la consola del servidor

**Funcionalidad Core:**
- [ ] Las 7 preguntas se cargan correctamente
- [ ] Botones SÍ/NO funcionan
- [ ] Barra de progreso avanza
- [ ] Botón "Anterior" funciona
- [ ] Resultados se muestran con colores correctos
- [ ] "Nuevo Diagnóstico" reinicia el cuestionario

**Nuevas Funcionalidades:**
- [ ] Botón "Ver Todos los Problemas" muestra múltiples diagnósticos
- [ ] Botón "Descargar PDF" genera PDF correctamente
- [ ] Botón "Ver Historial" muestra diagnósticos previos
- [ ] Estadísticas se muestran correctamente
- [ ] Historial se puede descargar en PDF
- [ ] Los diagnósticos se guardan en la base de datos

**Testing:**
- [ ] Todos los tests pasan: `pytest test_motor_inferencia.py -v`
- [ ] 23/23 tests en verde

