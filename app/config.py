import pandas as pd
import os

# Definindo SETs globais para armazenar IDs válidos
VALID_ORDERS = set()
VALID_PRODUCTS = set()
VALID_SELLERS = set()

def atualizar_ids_referencia(df: pd.DataFrame, tipo_tabela: str):
    """Atualiza o SET global de IDs válidos com base no DataFrame recebido."""

    if tipo_tabela == 'produtos':
        # Assumindo que a coluna de chave primária é 'product_id'
        novos_ids = set(df['product_id']) 
        VALID_PRODUCTS.update(novos_ids)
        print(f"IDs de Produtos atualizados. Total: {len(VALID_PRODUCTS)}")
        
    elif tipo_tabela == 'pedidos':
        novos_ids = set(df['order_id'])
        VALID_ORDERS.update(novos_ids)
        print(f"IDs de Pedidos atualizados. Total: {len(VALID_ORDERS)}")
    
    elif tipo_tabela == 'vendedores':
        novos_ids = set(df['sellers_id'])
        VALID_SELLERS.update(novos_ids)
        print(f"IDs de Pedidos atualizados. Total: {len(VALID_SELLERS)}")

def verificar_integridade(df_itens: pd.DataFrame):
    """
    Função para checar se as chaves existem nos SETs globais.
    Use apenas para validar itens_pedidos que têm product_id e seller_id.
    """
    global VALID_ORDERS, VALID_PRODUCTS, VALID_SELLERS

    # 1. Checagem de Chaves
    df_itens['order_id_ok'] = df_itens['order_id'].isin(VALID_ORDERS)
    df_itens['product_id_ok'] = df_itens['product_id'].isin(VALID_PRODUCTS)
    df_itens['seller_id_ok'] = df_itens['seller_id'].isin(VALID_SELLERS)
    
    # 2. Determinação do Status
    df_itens['is_valid'] = (
        df_itens['order_id_ok'] & 
        df_itens['product_id_ok'] & 
        df_itens['seller_id_ok']
    )
    
    # 3. Divisão dos DataFrames
    df_validos = df_itens[df_itens['is_valid']].copy()
    df_orfaos = df_itens[~df_itens['is_valid']].copy()
    
    # 4. Limpeza
    cols_to_drop = ['order_id_ok', 'product_id_ok', 'seller_id_ok', 'is_valid']
    df_validos = df_validos.drop(columns=cols_to_drop)
    
    return df_validos, df_orfaos
    pass