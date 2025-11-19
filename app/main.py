from fastapi import FastAPI
import uvicorn
import pandas as pd
from app.routers import example_router
from app.services.limpeza_pedidos import limpar_pedidos, limpar_produtos

app = FastAPI(
    title="API de Tratamento de Dados - Desafio 1",
    description="API que recebe dados brutos, os trata e os devolve limpos.",
    version="1.0.0"
)

@app.get("/", description="Mensagem de boas-vindas da API.")
async def read_root():
    return {"message": "Bem-vindo à API de Tratamento de Dados!"}

@app.get("/health", description="Verifica a saúde da API.")
async def health_check():
    return {"status": "ok"}

app.include_router(example_router, prefix="/example", tags=["Example"])

@app.get("/test-limpeza", description="Testa a limpeza de pedidos com dados de exemplo.")
async def test_limpeza():
    """
    Endpoint de demonstração que mostra a limpeza funcionando.
    Retorna JSON com status em português e novas colunas calculadas.
    """
    # Dados de exemplo (simulando um pedido)
    dados_exemplo = {
        'order_id': ['123', '456'],
        'order_status': ['delivered', 'processing'],
        'order_purchase_timestamp': ['2024-01-15 10:30:00', '2024-01-20 14:00:00'],
        'order_approved_at': ['2024-01-15 11:00:00', '2024-01-20 14:30:00'],
        'order_delivered_carrier_date': ['2024-01-16 09:00:00', None],
        'order_delivered_customer_date': ['2024-01-18 15:30:00', None],
        'order_estimated_delivery_date': ['2024-01-22 23:59:59', '2024-01-27 23:59:59']
    }
    
    df = pd.DataFrame(dados_exemplo)
    df_limpo = limpar_pedidos(df)
    
    # Converte para JSON
    resultado = df_limpo.to_dict(orient='records')
    
    return {
        "message": "Limpeza aplicada com sucesso!",
        "dados_limpos": resultado
    }