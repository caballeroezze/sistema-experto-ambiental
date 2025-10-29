"""
Tests unitarios para el motor de inferencia del Sistema Experto Ambiental

Ejecutar con: pytest test_motor_inferencia.py -v
O con: python -m pytest test_motor_inferencia.py -v
"""

import pytest
from reglas import motor_inferencia, motor_inferencia_multiple, REGLAS_AMBIENTALES, HECHOS_OBSERVABLES


class TestMotorInferencia:
    """Tests para el motor de inferencia principal"""
    
    def test_motor_inferencia_con_hechos_vacios(self):
        """Debe devolver una regla cuando no hay indicadores positivos"""
        hechos = {
            "olor_fuerte": False,
            "vegetacion_deteriorada": False,
            "residuos_acumulados": False,
            "humedad_excesiva": False,
            "ruido_elevado": False,
            "aire_contaminado": False,
            "agua_turbia": False
        }
        resultado = motor_inferencia(hechos)
        
        assert resultado is not None
        assert resultado['riesgo'] == 'BAJO'
        assert resultado['titulo'] == "Zona con Condiciones Aceptables"
    
    def test_motor_inferencia_contaminacion_agua(self):
        """Debe detectar contaminación crítica del agua"""
        hechos = {
            "olor_fuerte": True,
            "vegetacion_deteriorada": False,
            "residuos_acumulados": False,
            "humedad_excesiva": True,
            "ruido_elevado": False,
            "aire_contaminado": False,
            "agua_turbia": True
        }
        resultado = motor_inferencia(hechos)
        
        assert resultado is not None
        assert resultado['riesgo'] == 'ALTO'
        assert resultado['categoria'] == 'Contaminación del Agua'
        assert 'acciones' in resultado
        assert len(resultado['acciones']) > 0
    
    def test_motor_inferencia_residuos_peligrosos(self):
        """Debe detectar zona de acumulación de residuos peligrosos"""
        hechos = {
            "olor_fuerte": True,
            "vegetacion_deteriorada": True,
            "residuos_acumulados": True,
            "humedad_excesiva": False,
            "ruido_elevado": False,
            "aire_contaminado": False,
            "agua_turbia": False
        }
        resultado = motor_inferencia(hechos)
        
        assert resultado is not None
        assert resultado['riesgo'] == 'ALTO'
        assert resultado['categoria'] == 'Gestión de Residuos'
        assert 'justificacion' in resultado
    
    def test_motor_inferencia_contaminacion_atmosferica(self):
        """Debe detectar contaminación atmosférica significativa"""
        hechos = {
            "olor_fuerte": False,
            "vegetacion_deteriorada": False,
            "residuos_acumulados": False,
            "humedad_excesiva": False,
            "ruido_elevado": True,
            "aire_contaminado": True,
            "agua_turbia": False
        }
        resultado = motor_inferencia(hechos)
        
        assert resultado is not None
        assert resultado['riesgo'] == 'ALTO'
        assert resultado['categoria'] == 'Contaminación Atmosférica'
    
    def test_motor_inferencia_deterioro_ecosistema(self):
        """Debe detectar deterioro moderado del ecosistema"""
        hechos = {
            "olor_fuerte": False,
            "vegetacion_deteriorada": True,
            "residuos_acumulados": True,
            "humedad_excesiva": False,
            "ruido_elevado": False,
            "aire_contaminado": False,
            "agua_turbia": False
        }
        resultado = motor_inferencia(hechos)
        
        assert resultado is not None
        assert resultado['riesgo'] == 'MEDIO'
        assert resultado['categoria'] == 'Ecosistema'
    
    def test_motor_inferencia_ruido_aislado(self):
        """Debe detectar contaminación acústica sin contaminación del aire"""
        hechos = {
            "olor_fuerte": False,
            "vegetacion_deteriorada": False,
            "residuos_acumulados": False,
            "humedad_excesiva": False,
            "ruido_elevado": True,
            "aire_contaminado": False,
            "agua_turbia": False
        }
        resultado = motor_inferencia(hechos)
        
        assert resultado is not None
        assert resultado['riesgo'] == 'MEDIO'
        assert resultado['categoria'] == 'Contaminación Acústica'
    
    def test_motor_inferencia_no_devuelve_lambda(self):
        """El resultado no debe contener la función lambda 'condicion'"""
        hechos = {
            "olor_fuerte": True,
            "vegetacion_deteriorada": True,
            "residuos_acumulados": True,
            "humedad_excesiva": True,
            "ruido_elevado": True,
            "aire_contaminado": True,
            "agua_turbia": True
        }
        resultado = motor_inferencia(hechos)
        
        assert resultado is not None
        assert 'condicion' not in resultado
    
    def test_motor_inferencia_tiene_campos_requeridos(self):
        """El resultado debe tener todos los campos esenciales"""
        hechos = {
            "olor_fuerte": True,
            "vegetacion_deteriorada": False,
            "residuos_acumulados": False,
            "humedad_excesiva": True,
            "ruido_elevado": False,
            "aire_contaminado": False,
            "agua_turbia": True
        }
        resultado = motor_inferencia(hechos)
        
        assert resultado is not None
        assert 'id' in resultado
        assert 'titulo' in resultado
        assert 'riesgo' in resultado
        assert 'categoria' in resultado
        assert 'descripcion' in resultado
        assert 'acciones' in resultado
        assert 'justificacion' in resultado


class TestMotorInferenciaMultiple:
    """Tests para el motor de inferencia múltiple"""
    
    def test_motor_multiple_con_hechos_vacios(self):
        """Debe devolver solo la regla de condiciones aceptables"""
        hechos = {
            "olor_fuerte": False,
            "vegetacion_deteriorada": False,
            "residuos_acumulados": False,
            "humedad_excesiva": False,
            "ruido_elevado": False,
            "aire_contaminado": False,
            "agua_turbia": False
        }
        resultados = motor_inferencia_multiple(hechos)
        
        assert isinstance(resultados, list)
        assert len(resultados) >= 1
        # Debe incluir la regla de condiciones aceptables
        assert any(r['riesgo'] == 'BAJO' for r in resultados)
    
    def test_motor_multiple_devuelve_lista(self):
        """Debe devolver una lista incluso si no hay reglas cumplidas"""
        hechos = {}
        resultados = motor_inferencia_multiple(hechos)
        
        assert isinstance(resultados, list)
    
    def test_motor_multiple_ordena_por_prioridad(self):
        """Las reglas deben estar ordenadas por nivel de riesgo (ALTO > MEDIO > BAJO)"""
        hechos = {
            "olor_fuerte": True,
            "vegetacion_deteriorada": True,
            "residuos_acumulados": True,
            "humedad_excesiva": True,
            "ruido_elevado": True,
            "aire_contaminado": True,
            "agua_turbia": True
        }
        resultados = motor_inferencia_multiple(hechos)
        
        assert len(resultados) > 0
        
        # Verificar que están ordenados
        riesgos = [r['riesgo'] for r in resultados]
        orden = {'ALTO': 0, 'MEDIO': 1, 'BAJO': 2}
        numeros = [orden.get(r, 3) for r in riesgos]
        
        assert numeros == sorted(numeros), "Las reglas no están ordenadas por prioridad"
    
    def test_motor_multiple_multiples_reglas(self):
        """Debe devolver múltiples reglas cuando varias se cumplen"""
        hechos = {
            "olor_fuerte": True,
            "vegetacion_deteriorada": True,
            "residuos_acumulados": True,
            "humedad_excesiva": True,
            "ruido_elevado": True,
            "aire_contaminado": True,
            "agua_turbia": True
        }
        resultados = motor_inferencia_multiple(hechos)
        
        # Con todos los indicadores en True, deberían cumplirse varias reglas
        assert len(resultados) > 1
    
    def test_motor_multiple_sin_lambda_en_resultados(self):
        """Ninguna regla devuelta debe contener la función lambda"""
        hechos = {
            "olor_fuerte": True,
            "vegetacion_deteriorada": True,
            "residuos_acumulados": True,
            "humedad_excesiva": False,
            "ruido_elevado": False,
            "aire_contaminado": False,
            "agua_turbia": False
        }
        resultados = motor_inferencia_multiple(hechos)
        
        for regla in resultados:
            assert 'condicion' not in regla
    
    def test_motor_multiple_todas_reglas_validas(self):
        """Todas las reglas devueltas deben tener la estructura correcta"""
        hechos = {
            "olor_fuerte": True,
            "vegetacion_deteriorada": True,
            "residuos_acumulados": True,
            "humedad_excesiva": True,
            "ruido_elevado": False,
            "aire_contaminado": False,
            "agua_turbia": False
        }
        resultados = motor_inferencia_multiple(hechos)
        
        for regla in resultados:
            assert 'id' in regla
            assert 'titulo' in regla
            assert 'riesgo' in regla
            assert 'categoria' in regla
            assert 'descripcion' in regla
            assert 'acciones' in regla
            assert 'justificacion' in regla


class TestBaseConocimiento:
    """Tests para la base de conocimiento"""
    
    def test_todas_reglas_tienen_campos_requeridos(self):
        """Todas las reglas deben tener los campos esenciales"""
        campos_requeridos = ['id', 'titulo', 'condicion', 'riesgo', 'categoria', 
                            'descripcion', 'acciones', 'justificacion']
        
        for regla in REGLAS_AMBIENTALES:
            for campo in campos_requeridos:
                assert campo in regla, f"Regla {regla.get('id', 'sin ID')} no tiene el campo '{campo}'"
    
    def test_ids_unicos(self):
        """Todas las reglas deben tener IDs únicos"""
        ids = [regla['id'] for regla in REGLAS_AMBIENTALES]
        assert len(ids) == len(set(ids)), "Hay IDs duplicados en las reglas"
    
    def test_niveles_riesgo_validos(self):
        """Todos los niveles de riesgo deben ser válidos"""
        niveles_validos = {'ALTO', 'MEDIO', 'BAJO'}
        
        for regla in REGLAS_AMBIENTALES:
            assert regla['riesgo'] in niveles_validos, \
                f"Regla {regla['id']} tiene nivel de riesgo inválido: {regla['riesgo']}"
    
    def test_acciones_son_listas(self):
        """El campo 'acciones' debe ser una lista"""
        for regla in REGLAS_AMBIENTALES:
            assert isinstance(regla['acciones'], list), \
                f"Regla {regla['id']}: 'acciones' no es una lista"
            assert len(regla['acciones']) > 0, \
                f"Regla {regla['id']}: 'acciones' está vacía"
    
    def test_hechos_observables_estructura(self):
        """Los hechos observables deben tener la estructura correcta"""
        for hecho in HECHOS_OBSERVABLES:
            assert 'id' in hecho, "Falta campo 'id' en un hecho observable"
            assert 'pregunta' in hecho, "Falta campo 'pregunta' en un hecho observable"
            assert isinstance(hecho['id'], str), "El 'id' debe ser un string"
            assert isinstance(hecho['pregunta'], str), "La 'pregunta' debe ser un string"
    
    def test_numero_hechos_observables(self):
        """Debe haber exactamente 7 hechos observables"""
        assert len(HECHOS_OBSERVABLES) == 7, \
            f"Se esperaban 7 hechos observables, pero hay {len(HECHOS_OBSERVABLES)}"


class TestCasosEspecificos:
    """Tests de casos específicos del dominio ambiental"""
    
    def test_prioridad_contaminacion_agua(self):
        """La contaminación del agua debe tener prioridad ALTA"""
        hechos = {
            "olor_fuerte": True,
            "vegetacion_deteriorada": False,
            "residuos_acumulados": False,
            "humedad_excesiva": True,
            "ruido_elevado": False,
            "aire_contaminado": False,
            "agua_turbia": True
        }
        resultado = motor_inferencia(hechos)
        
        assert resultado['riesgo'] == 'ALTO'
        assert 'agua' in resultado['categoria'].lower() or 'agua' in resultado['titulo'].lower()
    
    def test_problema_drenaje_riesgo_bajo(self):
        """Problema de drenaje aislado debe ser riesgo BAJO"""
        hechos = {
            "olor_fuerte": False,
            "vegetacion_deteriorada": False,
            "residuos_acumulados": False,
            "humedad_excesiva": True,
            "ruido_elevado": False,
            "aire_contaminado": False,
            "agua_turbia": False
        }
        resultado = motor_inferencia(hechos)
        
        assert resultado is not None
        assert resultado['riesgo'] == 'BAJO'
    
    def test_combinacion_aire_ruido_es_alto(self):
        """Contaminación de aire + ruido debe ser riesgo ALTO"""
        hechos = {
            "olor_fuerte": False,
            "vegetacion_deteriorada": False,
            "residuos_acumulados": False,
            "humedad_excesiva": False,
            "ruido_elevado": True,
            "aire_contaminado": True,
            "agua_turbia": False
        }
        resultado = motor_inferencia(hechos)
        
        assert resultado['riesgo'] == 'ALTO'


# Función para ejecutar los tests manualmente
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

