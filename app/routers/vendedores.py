from fastapi import APIRouter, HTTPException, status
from typing import List
import pandas as pd

from app.schemas.vendedores import VendedorRaw
from app.services.vendedores_services import limpar_vendedores
from ..config import *

router = APIRouter(prefix="/vendedores", tags=["Vendedores"])

@router.post("/processar_vendedores")
def processar_vendedores_endpoint(dados: List[VendedorRaw]):
    
    #recebe lista de vendedores e padroniza cidades e estados.
    # Converte Pydantic para DataFrame
    lista_dados = [vendedor.model_dump() for vendedor in dados]
    df = pd.DataFrame(lista_dados)
  
    df_limpo = limpar_vendedores(df)

    atualizar_ids_referencia(df_limpo, 'vendedores')

    df_validos, df_orfaos = verificar_integridade(df_limpo)
    
    # 4. DECISÃO DE FLUXO E RETORNO HTTP
    
    if not df_orfaos.empty:
        # ATENÇÃO: Se houver registros órfãos, devemos falhar o fluxo no n8n.
        
        # Converte a lista de órfãos para JSON para que o n8n possa alertar
        orfaos_json = df_orfaos.to_dict(orient="records")
        
        # Levanta um erro HTTP 400 (Bad Request) que o n8n pode capturar.
        # Isso atende à necessidade de desviar o fluxo para um alerta.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Falha na Integridade Referencial. Dados órfãos detectados.",
                "data": orfaos_json
            }
        )

    return df_limpo.to_dict(orient="records")
