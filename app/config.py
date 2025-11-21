import pandas as pd
import os

VALID_ORDERS = set()
VALID_PRODUCTS = set()
VALID_SELLERS = set()

def atualizar_ids_referencia(df: pd.DataFrame, tipo_tabela: str):

    if tipo_tabela == 'produtos':
        novos_ids = set(df['product_id']) 
        VALID_PRODUCTS.update(novos_ids)
        print(f"IDs de Produtos atualizados. Total: {len(VALID_PRODUCTS)}")
        
    elif tipo_tabela == 'pedidos':
        novos_ids = set(df['order_id'])
        VALID_ORDERS.update(novos_ids)
        print(f"IDs de Pedidos atualizados. Total: {len(VALID_ORDERS)}")
    
    elif tipo_tabela == 'vendedores':
        novos_ids = set(df['seller_id'])
        VALID_SELLERS.update(novos_ids)
        print(f"IDs de Pedidos atualizados. Total: {len(VALID_SELLERS)}")

def verificar_integridade(df_itens: pd.DataFrame, df_dimensoes: dict):

    VALID_ORDERS = set()
    VALID_PRODUCTS = set()
    VALID_SELLERS = set()

    # 1. Checagem de Chaves
    
    df_itens['order_id_ok'] = df_itens['order_id'].isin(VALID_ORDERS)
    df_itens['product_id_ok'] = df_itens['product_id'].isin(VALID_PRODUCTS)
    df_itens['seller_id_ok'] = df_itens['seller_id'].isin(VALID_SELLERS)
    
    # 2. Determinação do Status (Válido vs. Órfão)
    
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
