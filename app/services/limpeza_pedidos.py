import pandas as pd

def limpar_pedidos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpa e transforma a tabela de pedidos seguindo as regras de negócio.
    
    Args:
        df (pd.DataFrame): DataFrame com dados brutos de pedidos.
        
    Returns:
        pd.DataFrame: DataFrame com dados limpos e transformados.
    """
    df = df.copy()
    
    # Conversão de datas
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
    
    # Tradução de status
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
    
    # Engenharia de atributos - Tempo de entrega
    if 'order_delivered_customer_date' in df.columns and 'order_purchase_timestamp' in df.columns:
        df['tempo_entrega_dias'] = (
            df['order_delivered_customer_date'] - df['order_purchase_timestamp']
        ).dt.days
    
    # Engenharia de atributos - Tempo estimado
    if 'order_estimated_delivery_date' in df.columns and 'order_purchase_timestamp' in df.columns:
        df['tempo_entrega_estimado_dias'] = (
            df['order_estimated_delivery_date'] - df['order_purchase_timestamp']
        ).dt.days
    
    # Engenharia de atributos - Entrega no prazo
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