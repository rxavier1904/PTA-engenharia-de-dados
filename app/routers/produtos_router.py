from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List
import pandas as pd
from ..schemas.produtos import *
from ..services.produtos_services import *
from ..config import *

router = APIRouter(prefix="/products", tags=["Produtos"])


@router.post("/processar_produtos")
def processar_produtos(dados: List[ProdutoRaw]):
    # Converte JSON para DataFrame
    df = pd.DataFrame([d.dict() for d in dados])

    df_limpo = limpar_produtos(df)

    atualizar_ids_referencia(df_limpo, 'produtos')

    # df_validos, df_orfaos = verificar_integridade(df_limpo)
    
    # # 4. DECISÃO DE FLUXO E RETORNO HTTP
    
    # if not df_orfaos.empty:
    #     # ATENÇÃO: Se houver registros órfãos, devemos falhar o fluxo no n8n.
        
    #     # Converte a lista de órfãos para JSON para que o n8n possa alertar
    #     orfaos_json = df_orfaos.to_dict(orient="records")
        
    #     # Levanta um erro HTTP 400 (Bad Request) que o n8n pode capturar.
    #     # Isso atende à necessidade de desviar o fluxo para um alerta.
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail={
    #             "message": "Falha na Integridade Referencial. Dados órfãos detectados.",
    #             "data": orfaos_json
    #         }
    #     )

    # Retorna como JSON (orient='records')
    return df_limpo.to_dict(orient="records")
