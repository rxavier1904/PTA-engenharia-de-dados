from fastapi import APIRouter, HTTPException, status
from typing import List
import pandas as pd
from app.schemas import PedidoInput
from app.services import limpar_pedidos
from ..config import *


router = APIRouter()


@router.post("/limpar", description="Limpa e transforma dados de pedidos recebidos como JSON.")
async def limpar_pedidos_endpoint(pedidos: List[PedidoInput]):
    """
    Endpoint para processar pedidos.
    
    Recebe uma lista de pedidos em formato JSON, aplica a limpeza e retorna:
    - Status traduzidos para português
    - Datas convertidas para datetime
    - Novas colunas calculadas
    
    Args:
        pedidos: Lista de objetos PedidoInput (JSON)
        
    Returns:
        JSON com dados limpos e transformados
    """
    # Converte lista de objetos Pydantic para DataFrame
    lista_dict = [p.model_dump() for p in pedidos]
    df = pd.DataFrame(lista_dict)
    
    # Aplica a função de limpeza
    df_limpo = limpar_pedidos(df)

    atualizar_ids_referencia(df_limpo, 'pedidos')

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
    
    # Converte para JSON tratando NaN como None
    resultado = df_limpo.where(pd.notnull(df_limpo), None).to_dict(orient='records')
    
    return {
        "message": "Pedidos processados com sucesso!",
        "total_registros": len(pedidos),
        "dados": resultado
    }
