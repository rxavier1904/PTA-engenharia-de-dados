from fastapi import APIRouter
from app.core.initializer import inicializar_dimensoes

router = APIRouter()

@router.post("/rodar_carga_inicial")
def rodar_carga():
    inicializar_dimensoes()
    return {"status": "Carga inicial concluída!"}
