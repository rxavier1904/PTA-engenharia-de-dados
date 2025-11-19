from fastapi import APIRouter, HTTPException
from typing import List
import pandas as pd

# Importações locais
from app.schemas.itens_pedidos import ItemPedidoRaw
from app.services.itens_pedidos_services import limpar_itens_pedidos
from app.config import VALID_ORDERS, VALID_PRODUCTS, VALID_SELLERS

router = APIRouter(prefix="/itens_pedidos", tags=["Itens Pedidos"])

@router.post("/processar_itens")
def processar_itens(dados: List[ItemPedidoRaw]):    
    # verifica se o config.py carregou os dados
    if not VALID_ORDERS:
        print("Dados de referência vazios.")
        raise HTTPException(status_code=500, detail="Dados de referência não carregados no servidor.")

    # Converte Pydantic pra DataFrame
    lista_dados = [item.model_dump() for item in dados]
    df = pd.DataFrame(lista_dados)

    # chama o serviço passando pela validação
    df_limpo = limpar_itens_pedidos(
        df, 
        valid_orders=VALID_ORDERS, 
        valid_products=VALID_PRODUCTS, 
        valid_sellers=VALID_SELLERS
    )

    return df_limpo.to_dict(orient="records")
