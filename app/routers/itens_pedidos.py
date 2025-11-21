from fastapi import APIRouter, HTTPException, status
from typing import List
import pandas as pd

# Importações locais
from app.schemas.itens_pedidos import ItemPedidoRaw
from app.services.itens_pedidos_services import limpar_itens_pedidos
from app.config import *

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

    df_validos, df_orfaos = verificar_integridade(df_limpo)

    if not df_orfaos.empty:
        # Se houver órfãos, falhar o fluxo com HTTP 400 (Bad Request)
        # O n8n deve capturar este erro e disparar o alerta.
        orfaos_json = df_orfaos.to_dict(orient="records")
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Falha na Integridade Referencial. Dados órfãos detectados.",
                "data": orfaos_json
            }
        )

    return df_limpo.to_dict(orient="records")
