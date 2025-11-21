from fastapi import APIRouter, HTTPException, status
from typing import List
import pandas as pd
from app.schemas import PedidoInput
from ..config import *

router = APIRouter()

@router.post("/carregar-dimensoes", tags=["Dimensões"])
async def carregar_dimensoes(
    produtos: List[dict],
    vendedores: List[dict],
    pedidos: List[dict]
):
    """Endpoint para carregar as dimensões de referência vindo do n8n."""
    
    df_produtos = pd.DataFrame(produtos)
    df_vendedores = pd.DataFrame(vendedores)
    df_pedidos = pd.DataFrame(pedidos)
    
    atualizar_ids_referencia(df_produtos, 'produtos')
    atualizar_ids_referencia(df_vendedores, 'vendedores')
    atualizar_ids_referencia(df_pedidos, 'pedidos')
    
    return {
        "message": "Dimensões carregadas com sucesso!",
        "produtos": len(VALID_PRODUCTS),
        "vendedores": len(VALID_SELLERS),
        "pedidos": len(VALID_ORDERS)
    }