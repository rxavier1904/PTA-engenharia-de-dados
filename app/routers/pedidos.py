from fastapi import APIRouter
from typing import List
import pandas as pd
from app.schemas import PedidoInput
from app.services import limpar_pedidos

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
    
    # Converte para JSON tratando NaN como None
    resultado = df_limpo.where(pd.notnull(df_limpo), None).to_dict(orient='records')
    
    return {
        "message": "Pedidos processados com sucesso!",
        "total_registros": len(pedidos),
        "dados": resultado
    }
