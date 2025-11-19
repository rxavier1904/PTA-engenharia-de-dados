from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import pandas as pd
from ..schemas.produtos import *
from ..services.produtos_services import *

router = APIRouter(prefix="/products", tags=["Produtos"])


@router.post("/processar_produtos")
def processar_produtos(dados: List[ProdutoRaw]):
    # Converte JSON para DataFrame
    df = pd.DataFrame([d.dict() for d in dados])

    df_limpo = limpar_produtos(df)

    # Retorna como JSON (orient='records')
    return df_limpo.to_dict(orient="records")
