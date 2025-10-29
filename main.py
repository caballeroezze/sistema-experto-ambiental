from fastapi import FastAPI, Request, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from reglas import motor_inferencia, motor_inferencia_multiple, HECHOS_OBSERVABLES
from modelos import HechosRequest, DiagnosticoResponse, DiagnosticoMultipleRequest, DiagnosticoMultipleResponse
from database import guardar_diagnostico, obtener_historial, obtener_diagnostico_por_id, obtener_estadisticas
from pdf_generator import generar_pdf_diagnostico, generar_pdf_historial
from typing import Optional
from datetime import datetime

app = FastAPI(title="Sistema Experto Ambiental")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos y plantillas
templates = Jinja2Templates(directory="interfaz/templates")
app.mount("/static", StaticFiles(directory="interfaz/static"), name="static")

@app.get("/")
async def pagina_principal(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/hechos")
async def obtener_hechos():
    return list(HECHOS_OBSERVABLES)

@app.post("/diagnosticar", response_model=DiagnosticoResponse)
def diagnosticar(hechos_req: HechosRequest):
    resultado = motor_inferencia(hechos_req.hechos)
    
    # Guardar diagnóstico en la base de datos
    diagnostico_id = guardar_diagnostico(hechos_req.hechos, resultado)
    
    # Agregar el ID del diagnóstico al resultado
    response_data = {"diagnostico": resultado}
    if resultado:
        resultado["diagnostico_id"] = diagnostico_id
    else:
        response_data["diagnostico"] = {"diagnostico_id": diagnostico_id}
    
    return response_data

@app.get("/historial")
async def obtener_historial_diagnosticos(
    limite: int = Query(50, ge=1, le=100, description="Número de diagnósticos a obtener"),
    offset: int = Query(0, ge=0, description="Número de diagnósticos a saltar")
):
    """
    Obtiene el historial de diagnósticos realizados
    """
    historial = obtener_historial(limite=limite, offset=offset)
    return {"historial": historial, "total": len(historial)}

@app.get("/diagnostico/{diagnostico_id}")
async def obtener_diagnostico(diagnostico_id: int):
    """
    Obtiene un diagnóstico específico por su ID
    """
    diagnostico = obtener_diagnostico_por_id(diagnostico_id)
    if diagnostico:
        return diagnostico
    return {"error": "Diagnóstico no encontrado"}

@app.get("/estadisticas")
async def obtener_estadisticas_diagnosticos():
    """
    Obtiene estadísticas generales de los diagnósticos
    """
    stats = obtener_estadisticas()
    return stats

@app.get("/descargar-pdf/{diagnostico_id}")
async def descargar_pdf_diagnostico(diagnostico_id: int):
    """
    Genera y descarga un PDF con el diagnóstico específico
    """
    diagnostico = obtener_diagnostico_por_id(diagnostico_id)
    
    if not diagnostico:
        return {"error": "Diagnóstico no encontrado"}
    
    # Extraer hechos del diagnóstico
    hechos = diagnostico.pop('hechos', {})
    
    # Generar PDF
    pdf_bytes = generar_pdf_diagnostico(diagnostico, hechos)
    
    # Nombre del archivo
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"diagnostico_{diagnostico_id}_{fecha}.pdf"
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )

@app.get("/descargar-historial-pdf")
async def descargar_historial_pdf(
    limite: int = Query(50, ge=1, le=100, description="Número de diagnósticos a incluir")
):
    """
    Genera y descarga un PDF con el historial de diagnósticos
    """
    historial = obtener_historial(limite=limite, offset=0)
    
    if not historial:
        return {"error": "No hay diagnósticos en el historial"}
    
    # Generar PDF
    pdf_bytes = generar_pdf_historial(historial)
    
    # Nombre del archivo
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"historial_diagnosticos_{fecha}.pdf"
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )

@app.post("/diagnosticar-multiple", response_model=DiagnosticoMultipleResponse)
def diagnosticar_multiple(hechos_req: DiagnosticoMultipleRequest):
    """
    Realiza un diagnóstico devolviendo TODAS las reglas que se cumplen,
    ordenadas por nivel de riesgo (ALTO > MEDIO > BAJO)
    """
    resultados = motor_inferencia_multiple(hechos_req.hechos)
    
    # No guardamos en BD porque puede ser exploratorio
    # El usuario puede hacer diagnóstico normal si quiere guardar
    
    return {
        "diagnosticos": resultados,
        "total": len(resultados)
    }