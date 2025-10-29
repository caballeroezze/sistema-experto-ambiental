from typing import Optional, Dict, Any

HECHOS_OBSERVABLES = [
    {"id": "olor_fuerte", "pregunta": "¿Detecta olor fuerte o desagradable en el área?"},
    {"id": "vegetacion_deteriorada", "pregunta": "¿La vegetación está deteriorada o sin vida?"},
    {"id": "residuos_acumulados", "pregunta": "¿Hay acumulación visible de residuos o basura?"},
    {"id": "humedad_excesiva", "pregunta": "¿Observa humedad excesiva o estancamiento de agua?"},
    {"id": "ruido_elevado", "pregunta": "¿El nivel de ruido es elevado constantemente?"},
    {"id": "aire_contaminado", "pregunta": "¿Percibe contaminación en el aire (humo, polvo)?"},
    {"id": "agua_turbia", "pregunta": "¿El agua cercana está turbia o con coloración anormal?"},
]

REGLAS_AMBIENTALES = [
    {
        "id": "R-AMB-01",
        "titulo": "Contaminación Crítica del Agua",
        "condicion": lambda h: h.get("agua_turbia") and h.get("olor_fuerte") and h.get("humedad_excesiva"),
        "riesgo": "ALTO",
        "categoria": "Contaminación del Agua",
        "descripcion": "Indicadores de contaminación severa del agua que requiere atención inmediata.",
        "acciones": [
            "Reportar inmediatamente a autoridades ambientales",
            "Evitar contacto directo con el agua",
            "No consumir agua de la zona",
            "Evacuar si hay población cercana expuesta",
            "Solicitar análisis químico urgente del agua"
        ],
        "justificacion": "La combinación de agua turbia, olor fuerte y humedad excesiva indica posible contaminación con desechos tóxicos o aguas residuales sin tratar."
    },
    {
        "id": "R-AMB-02",
        "titulo": "Zona de Acumulación de Residuos Peligrosos",
        "condicion": lambda h: h.get("residuos_acumulados") and h.get("olor_fuerte") and h.get("vegetacion_deteriorada"),
        "riesgo": "ALTO",
        "categoria": "Gestión de Residuos",
        "descripcion": "Acumulación de residuos que está afectando el ecosistema local.",
        "acciones": [
            "Contactar servicios de recolección inmediatamente",
            "Delimitar zona afectada",
            "Prohibir acceso a niños y mascotas",
            "Evaluar presencia de residuos peligrosos",
            "Implementar limpieza profunda del área"
        ],
        "justificacion": "Los residuos acumulados generan olores y toxinas que deterioran la vegetación, indicando un problema de gestión de residuos grave."
    },
    {
        "id": "R-AMB-03",
        "titulo": "Contaminación Atmosférica Significativa",
        "condicion": lambda h: h.get("aire_contaminado") and h.get("ruido_elevado"),
        "riesgo": "ALTO",
        "categoria": "Contaminación Atmosférica",
        "descripcion": "Niveles elevados de contaminación del aire combinados con contaminación acústica.",
        "acciones": [
            "Usar mascarillas en la zona",
            "Limitar actividades al aire libre",
            "Monitorear calidad del aire",
            "Identificar fuentes de emisión",
            "Solicitar medidas de control de emisiones"
        ],
        "justificacion": "La presencia de contaminación del aire junto con ruido elevado sugiere zona industrial o tráfico intenso, poniendo en riesgo la salud respiratoria."
    },
    {
        "id": "R-AMB-04",
        "titulo": "Deterioro Moderado del Ecosistema",
        "condicion": lambda h: h.get("vegetacion_deteriorada") and (h.get("humedad_excesiva") or h.get("residuos_acumulados")),
        "riesgo": "MEDIO",
        "categoria": "Ecosistema",
        "descripcion": "El ecosistema muestra signos de deterioro que requieren intervención preventiva.",
        "acciones": [
            "Realizar estudio de suelo",
            "Implementar plan de recuperación vegetal",
            "Mejorar drenaje si hay exceso de humedad",
            "Limpiar residuos del área",
            "Monitorear evolución mensualmente"
        ],
        "justificacion": "La vegetación deteriorada indica desequilibrio ambiental que puede agravarse sin intervención oportuna."
    },
    {
        "id": "R-AMB-05",
        "titulo": "Contaminación Acústica",
        "condicion": lambda h: h.get("ruido_elevado") and not h.get("aire_contaminado"),
        "riesgo": "MEDIO",
        "categoria": "Contaminación Acústica",
        "descripcion": "Niveles de ruido que pueden afectar la calidad de vida.",
        "acciones": [
            "Medir niveles de decibeles",
            "Identificar fuentes de ruido",
            "Implementar barreras acústicas",
            "Regular horarios de actividades ruidosas",
            "Informar a residentes sobre protección auditiva"
        ],
        "justificacion": "El ruido elevado constante puede causar estrés, problemas de sueño y daños auditivos en la población expuesta."
    },
    {
        "id": "R-AMB-06",
        "titulo": "Gestión de Residuos Mejorable",
        "condicion": lambda h: h.get("residuos_acumulados") and not h.get("olor_fuerte"),
        "riesgo": "MEDIO",
        "categoria": "Gestión de Residuos",
        "descripcion": "Acumulación de residuos que requiere mejora en la gestión.",
        "acciones": [
            "Aumentar frecuencia de recolección",
            "Instalar más contenedores",
            "Campaña de educación ambiental",
            "Implementar sistema de separación de residuos",
            "Monitorear puntos críticos semanalmente"
        ],
        "justificacion": "La acumulación de residuos sin olor intenso indica problema de gestión antes que de descomposición avanzada."
    },
    {
        "id": "R-AMB-07",
        "titulo": "Problema de Drenaje",
        "condicion": lambda h: h.get("humedad_excesiva") and not h.get("agua_turbia") and not h.get("olor_fuerte"),
        "riesgo": "BAJO",
        "categoria": "Infraestructura",
        "descripcion": "Problemas de drenaje que pueden derivar en situaciones más graves.",
        "acciones": [
            "Inspeccionar sistema de drenaje",
            "Limpiar alcantarillas y desagües",
            "Evaluar pendientes del terreno",
            "Implementar mejoras de drenaje",
            "Prevenir formación de criaderos de mosquitos"
        ],
        "justificacion": "La humedad excesiva sin otros contaminantes indica deficiencia en infraestructura de drenaje."
    },
    {
        "id": "R-AMB-08",
        "titulo": "Deterioro Ambiental con Afectación de Vegetación",
        "condicion": lambda h: h.get("vegetacion_deteriorada") and h.get("olor_fuerte") and not h.get("residuos_acumulados"),
        "riesgo": "MEDIO",
        "categoria": "Contaminación Ambiental",
        "descripcion": "Deterioro de la vegetación asociado a contaminación ambiental sin evidencia de residuos sólidos.",
        "acciones": [
            "Identificar fuentes de contaminación atmosférica",
            "Realizar análisis de calidad del aire",
            "Evaluar el estado del suelo",
            "Implementar barreras vegetales de protección",
            "Monitorear la salud de la vegetación existente",
            "Investigar posibles fuentes industriales cercanas"
        ],
        "justificacion": "La combinación de vegetación deteriorada y olores indica posible contaminación atmosférica o del suelo que requiere identificación y control de la fuente."
    },
    {
        "id": "R-AMB-09",
        "titulo": "Zona con Condiciones Aceptables",
        "condicion": lambda h: not h.get("olor_fuerte") and not h.get("residuos_acumulados") and not h.get("aire_contaminado") and not h.get("agua_turbia"),
        "riesgo": "BAJO",
        "categoria": "Monitoreo Preventivo",
        "descripcion": "La zona presenta condiciones ambientales aceptables.",
        "acciones": [
            "Mantener programa de monitoreo regular",
            "Continuar con limpieza periódica",
            "Reforzar campañas de educación ambiental",
            "Preservar áreas verdes existentes",
            "Documentar estado actual como línea base"
        ],
        "justificacion": "La ausencia de indicadores críticos sugiere buena gestión ambiental, pero se requiere mantenimiento preventivo."
    }
]

def motor_inferencia(hechos: Dict[str, bool]) -> Optional[Dict[str, Any]]:
    """
    Motor de inferencia que evalúa todas las reglas y devuelve la de mayor prioridad
    
    Args:
        hechos: Diccionario con los hechos observados
    
    Returns:
        Regla con mayor prioridad que se cumple, o None si ninguna se cumple
    """
    for regla in REGLAS_AMBIENTALES:
        try:
            if regla["condicion"](hechos):
                # Eliminar función lambda antes de devolver
                return {k: v for k, v in regla.items() if k != "condicion"}
        except Exception as e:
            print(f"Error evaluando regla {regla['id']}: {e}")
    return None

def motor_inferencia_multiple(hechos: Dict[str, bool]) -> list:
    """
    Motor de inferencia que devuelve TODAS las reglas que se cumplen, ordenadas por prioridad
    
    Args:
        hechos: Diccionario con los hechos observados
    
    Returns:
        Lista de reglas que se cumplen, ordenadas por nivel de riesgo (ALTO > MEDIO > BAJO)
    """
    reglas_cumplidas = []
    
    for regla in REGLAS_AMBIENTALES:
        try:
            if regla["condicion"](hechos):
                # Eliminar función lambda antes de agregar
                regla_limpia = {k: v for k, v in regla.items() if k != "condicion"}
                reglas_cumplidas.append(regla_limpia)
        except Exception as e:
            print(f"Error evaluando regla {regla['id']}: {e}")
    
    # Ordenar por prioridad de riesgo
    orden_riesgo = {'ALTO': 0, 'MEDIO': 1, 'BAJO': 2}
    reglas_cumplidas.sort(key=lambda r: orden_riesgo.get(r.get('riesgo', 'BAJO'), 3))
    
    return reglas_cumplidas