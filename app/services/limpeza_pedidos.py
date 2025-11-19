import pandas as pd
import numpy as np

def limpar_pedidos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpa e transforma a tabela de pedidos seguindo as regras de negócio.
    
    Regras implementadas:
    - Converte 5 colunas de data para datetime
    - Traduz status de pedidos para português
    - Calcula tempo de entrega em dias
    - Calcula tempo estimado de entrega em dias
    - Cria flag de entrega no prazo
    
    Args:
        df: DataFrame com dados brutos de pedidos
        
    Returns:
        DataFrame limpo e transformado
    """
    df = df.copy()
    
    # CONVERSÃO DE DATAS
    colunas_data = [
        'order_purchase_timestamp',
        'order_approved_at',
        'order_delivered_carrier_date',
        'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ]
    
    for coluna in colunas_data:
        if coluna in df.columns:
            df[coluna] = pd.to_datetime(df[coluna], errors='coerce')
    
    # TRADUÇÃO DE STATUS
    mapa_status = {
        'delivered': 'entregue',
        'invoiced': 'faturado',
        'shipped': 'enviado',
        'processing': 'em processamento',
        'unavailable': 'indisponível',
        'canceled': 'cancelado',
        'created': 'criado',
        'approved': 'aprovado'
    }
    
    if 'order_status' in df.columns:
        df['order_status'] = df['order_status'].map(mapa_status).fillna(df['order_status'])
    
    # ENGENHARIA DE ATRIBUTOS - TEMPO DE ENTREGA
    if 'order_delivered_customer_date' in df.columns and 'order_purchase_timestamp' in df.columns:
        df['tempo_entrega_dias'] = (
            df['order_delivered_customer_date'] - df['order_purchase_timestamp']
        ).dt.days
    
    # ENGENHARIA DE ATRIBUTOS - TEMPO ESTIMADO
    if 'order_estimated_delivery_date' in df.columns and 'order_purchase_timestamp' in df.columns:
        df['tempo_entrega_estimado_dias'] = (
            df['order_estimated_delivery_date'] - df['order_purchase_timestamp']
        ).dt.days
    
    # ENGENHARIA DE ATRIBUTOS - ENTREGA NO PRAZO
    if all(col in df.columns for col in ['order_delivered_customer_date', 'order_estimated_delivery_date']):
        def calcular_entrega_no_prazo(row):
            if pd.isna(row['order_delivered_customer_date']):
                return 'Não Entregue'
            elif row['order_delivered_customer_date'] <= row['order_estimated_delivery_date']:
                return 'Sim'
            else:
                return 'Não'
        
        df['entrega_no_prazo'] = df.apply(calcular_entrega_no_prazo, axis=1)
    
    return df


def limpar_produtos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpa e padroniza a tabela de produtos.
    
    Regras implementadas:
    - Preenche valores nulos
    - Padroniza textos
    
    Args:
        df: DataFrame com dados brutos de produtos
        
    Returns:
        DataFrame limpo e transformado
    """
    df = df.copy()
    
    # Padronização de categoria
    if 'product_category_name' in df.columns:
        df['product_category_name'] = df['product_category_name'].fillna('Desconhecido')
    
    # Preenche valores nulos numéricos com 0
    colunas_numericas = [
        'product_name_lenght',
        'product_description_lenght',
        'product_photos_qty',
        'product_weight_g',
        'product_length_cm',
        'product_height_cm',
        'product_width_cm'
    ]
    
    for coluna in colunas_numericas:
        if coluna in df.columns:
            df[coluna] = df[coluna].fillna(0)
    
    return df
