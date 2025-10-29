import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from contextlib import contextmanager

DATABASE_NAME = "diagnosticos_ambientales.db"

@contextmanager
def get_db_connection():
    """Context manager para manejar conexiones a la base de datos"""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def init_database():
    """Inicializa la base de datos con las tablas necesarias"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS diagnosticos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                hechos_json TEXT NOT NULL,
                regla_id TEXT,
                titulo TEXT,
                categoria TEXT,
                riesgo TEXT,
                descripcion TEXT,
                justificacion TEXT,
                acciones_json TEXT
            )
        ''')
        conn.commit()

def guardar_diagnostico(hechos: Dict[str, bool], resultado: Optional[Dict[str, Any]]) -> int:
    """
    Guarda un diagnóstico en la base de datos
    
    Args:
        hechos: Diccionario con los hechos observados
        resultado: Resultado del motor de inferencia (puede ser None)
    
    Returns:
        ID del diagnóstico guardado
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        hechos_json = json.dumps(hechos, ensure_ascii=False)
        
        if resultado:
            cursor.execute('''
                INSERT INTO diagnosticos 
                (hechos_json, regla_id, titulo, categoria, riesgo, descripcion, justificacion, acciones_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                hechos_json,
                resultado.get('id'),
                resultado.get('titulo'),
                resultado.get('categoria'),
                resultado.get('riesgo'),
                resultado.get('descripcion'),
                resultado.get('justificacion'),
                json.dumps(resultado.get('acciones', []), ensure_ascii=False)
            ))
        else:
            # Diagnóstico sin resultado (condiciones normales)
            cursor.execute('''
                INSERT INTO diagnosticos 
                (hechos_json, regla_id, titulo, categoria, riesgo, descripcion, justificacion, acciones_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                hechos_json,
                None,
                "Sin diagnóstico aplicable",
                "Monitoreo Preventivo",
                "BAJO",
                "No se encontraron condiciones críticas",
                "La ausencia de indicadores críticos sugiere buena gestión ambiental",
                json.dumps(["Mantener monitoreo periódico", "Continuar con buenas prácticas ambientales"], ensure_ascii=False)
            ))
        
        return cursor.lastrowid

def obtener_historial(limite: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
    """
    Obtiene el historial de diagnósticos
    
    Args:
        limite: Número máximo de registros a devolver
        offset: Número de registros a saltar
    
    Returns:
        Lista de diagnósticos con toda la información
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                id,
                fecha,
                hechos_json,
                regla_id,
                titulo,
                categoria,
                riesgo,
                descripcion,
                justificacion,
                acciones_json
            FROM diagnosticos
            ORDER BY fecha DESC
            LIMIT ? OFFSET ?
        ''', (limite, offset))
        
        rows = cursor.fetchall()
        
        diagnosticos = []
        for row in rows:
            diagnostico = {
                'id': row['id'],
                'fecha': row['fecha'],
                'hechos': json.loads(row['hechos_json']),
                'regla_id': row['regla_id'],
                'titulo': row['titulo'],
                'categoria': row['categoria'],
                'riesgo': row['riesgo'],
                'descripcion': row['descripcion'],
                'justificacion': row['justificacion'],
                'acciones': json.loads(row['acciones_json']) if row['acciones_json'] else []
            }
            diagnosticos.append(diagnostico)
        
        return diagnosticos

def obtener_diagnostico_por_id(diagnostico_id: int) -> Optional[Dict[str, Any]]:
    """
    Obtiene un diagnóstico específico por su ID
    
    Args:
        diagnostico_id: ID del diagnóstico
    
    Returns:
        Diagnóstico completo o None si no existe
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                id,
                fecha,
                hechos_json,
                regla_id,
                titulo,
                categoria,
                riesgo,
                descripcion,
                justificacion,
                acciones_json
            FROM diagnosticos
            WHERE id = ?
        ''', (diagnostico_id,))
        
        row = cursor.fetchone()
        
        if row:
            return {
                'id': row['id'],
                'fecha': row['fecha'],
                'hechos': json.loads(row['hechos_json']),
                'regla_id': row['regla_id'],
                'titulo': row['titulo'],
                'categoria': row['categoria'],
                'riesgo': row['riesgo'],
                'descripcion': row['descripcion'],
                'justificacion': row['justificacion'],
                'acciones': json.loads(row['acciones_json']) if row['acciones_json'] else []
            }
        
        return None

def obtener_estadisticas() -> Dict[str, Any]:
    """
    Obtiene estadísticas generales de los diagnósticos
    
    Returns:
        Diccionario con estadísticas
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Total de diagnósticos
        cursor.execute('SELECT COUNT(*) as total FROM diagnosticos')
        total = cursor.fetchone()['total']
        
        # Diagnósticos por nivel de riesgo
        cursor.execute('''
            SELECT riesgo, COUNT(*) as cantidad
            FROM diagnosticos
            GROUP BY riesgo
        ''')
        por_riesgo = {row['riesgo']: row['cantidad'] for row in cursor.fetchall()}
        
        # Diagnósticos por categoría
        cursor.execute('''
            SELECT categoria, COUNT(*) as cantidad
            FROM diagnosticos
            GROUP BY categoria
            ORDER BY cantidad DESC
            LIMIT 5
        ''')
        por_categoria = {row['categoria']: row['cantidad'] for row in cursor.fetchall()}
        
        return {
            'total': total,
            'por_riesgo': por_riesgo,
            'por_categoria': por_categoria
        }

# Inicializar base de datos al importar el módulo
init_database()

