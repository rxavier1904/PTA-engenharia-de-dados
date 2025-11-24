from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List
import pandas as pd
from ..schemas.produtos import ProdutoRaw

router = APIRouter(prefix="/products", tags=["Produtos"])


@router.post("/processar_produtos")
def processar_produtos(dados: List[ProdutoRaw]):
    """
    Endpoint para processar produtos.
    Recebe dados brutos e retorna os mesmos dados validados.
    """
    # Converte JSON para DataFrame usando model_dump() (Pydantic v2)
    df = pd.DataFrame([d.model_dump() for d in dados])
    
    # Converte NaN para None para JSON válido
    resultado = df.where(pd.notnull(df), None).to_dict(orient='records')
    
    return resultado