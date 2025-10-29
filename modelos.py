from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class HechosRequest(BaseModel):
    hechos: Dict[str, bool]

class DiagnosticoResponse(BaseModel):
    diagnostico: Optional[Dict[str, Any]] = None

class DiagnosticoMultipleRequest(BaseModel):
    hechos: Dict[str, bool]

class DiagnosticoMultipleResponse(BaseModel):
    diagnosticos: List[Dict[str, Any]]
    total: int