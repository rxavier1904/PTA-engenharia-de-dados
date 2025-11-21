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

def verificar_integridade(df_itens: pd.DataFrame, df_dimensoes: dict):
    """
    Função para checar se as chaves existem nos SETs globais. 
    Esta seria a lógica para validar itens_pedidos.
    """

    VALID_ORDERS = set()  # Deve ser populado pelo endpoint de pedidos
    VALID_PRODUCTS = set() # Deve ser populado pelo endpoint de produtos
    VALID_SELLERS = set()  # Deve ser populado pelo endpoint de vendedores

    # 1. Checagem de Chaves
    
    # Cria uma coluna booleana (True/False) para cada checagem
    df_itens['order_id_ok'] = df_itens['order_id'].isin(VALID_ORDERS)
    df_itens['product_id_ok'] = df_itens['product_id'].isin(VALID_PRODUCTS)
    df_itens['seller_id_ok'] = df_itens['seller_id'].isin(VALID_SELLERS)
    
    # 2. Determinação do Status (Válido vs. Órfão)
    
    # Um registro é válido se TODAS as chaves de referência existirem
    df_itens['is_valid'] = (
        df_itens['order_id_ok'] & 
        df_itens['product_id_ok'] & 
        df_itens['seller_id_ok']
    )
    
    # 3. Divisão dos DataFrames
    
    # Separa os registros que podem ser carregados no DW
    df_validos = df_itens[df_itens['is_valid']].copy()
    
    # Separa os registros que falharam e precisam ser alertados
    df_orfaos = df_itens[~df_itens['is_valid']].copy()
    
    # 4. Limpeza (Opcional, mas recomendado)
    
    # Remove colunas auxiliares de checagem dos DataFrames de saída
    cols_to_drop = ['order_id_ok', 'product_id_ok', 'seller_id_ok', 'is_valid']
    df_validos = df_validos.drop(columns=cols_to_drop)
    # Mantemos as colunas de checagem em df_orfaos para fins de debug/alerta
    
    return df_validos, df_orfaos
    pass