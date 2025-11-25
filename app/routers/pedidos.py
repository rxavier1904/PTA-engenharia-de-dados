from fastapi import APIRouter
from typing import List
import pandas as pd
from app.schemas import PedidoInput
from app.services import limpar_pedidos
from ..config import atualizar_ids_referencia   # IMPORTA DIRETO
import math

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
    
    # Converte objetos Pydantic em dicionários
    lista_dict = [p.model_dump() for p in pedidos]

    # Remove campos inválidos
    lista_limpa = [
        {k: v for k, v in registro.items() if k in CAMPOS_VALIDOS}
        for registro in lista_dict
    ]

    # Converte para DataFrame
    df = pd.DataFrame(lista_limpa)

    # Limpa e transforma
    df_limpo = limpar_pedidos(df)

    # NÃO USAMOS O RETORNO (igual vendedores)
    atualizar_ids_referencia(df_limpo, 'pedidos')

    # Converte NaN → None para JSON
    df_json = df_limpo.where(pd.notnull(df_limpo), None)

    # Última limpeza (garante JSON válido)
    import math
    def clean_json(o):
        if isinstance(o, list):
            return [clean_json(x) for x in o]
        if isinstance(o, dict):
            return {k: clean_json(v) for k, v in o.items()}
        if isinstance(o, float) and math.isnan(o):
            return None
        return o

    retorno = clean_json(df_json.to_dict(orient="records"))

    return retorno
