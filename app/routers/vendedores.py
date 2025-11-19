from fastapi import APIRouter
from typing import List
import pandas as pd

from app.schemas.vendedores import VendedorRaw
from app.services.vendedores_services import limpar_vendedores

router = APIRouter(prefix="/vendedores", tags=["Vendedores"])

@router.post("/processar_vendedores")
def processar_vendedores_endpoint(dados: List[VendedorRaw]):
    
    #recebe lista de vendedores e padroniza cidades e estados.
    # Converte Pydantic para DataFrame
    lista_dados = [vendedor.model_dump() for vendedor in dados]
    df = pd.DataFrame(lista_dados)
  
    df_limpo = limpar_vendedores(df)

    return df_limpo.to_dict(orient="records")
