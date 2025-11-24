from fastapi import APIRouter, HTTPException, status
from typing import List
import pandas as pd
from app.schemas import PedidoInput
from app.services import limpar_pedidos
from ..config import *


router = APIRouter()

CAMPOS_VALIDOS = [
    "order_id",
    "customer_id",
    "order_status",
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]


@router.post("/limpar", description="Limpa e transforma dados de pedidos recebidos como JSON.")
async def limpar_pedidos_endpoint(pedidos: List[PedidoInput]):
    """
    Endpoint para processar pedidos.
    """

    #  Converte lista de objetos Pydantic para dicionários
    lista_dict = [p.model_dump() for p in pedidos]

    #  Remove campos inválidos do JSON antes de montar o DataFrame
    lista_limpa = [
        {k: v for k, v in registro.items() if k in CAMPOS_VALIDOS}
        for registro in lista_dict
    ]

    #  Converte para DataFrame
    df = pd.DataFrame(lista_limpa)

    #  Aplica a função de limpeza
    df_limpo = limpar_pedidos(df)

    # Atualiza IDs referenciais
    atualizar_ids_referencia(df_limpo, 'pedidos')

    #Converte NaN → None para JSON
    resultado = df_limpo.where(pd.notnull(df_limpo), None).to_dict(orient='records')

    return {
        "message": "Pedidos processados com sucesso!",
        "total_registros": len(pedidos),
        "dados": resultado
    }