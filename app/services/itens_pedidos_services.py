import pandas as pd
import numpy as np



def filtrar_orfaos(df_itens: pd.DataFrame, valid_orders: set, valid_products: set, valid_sellers: set) -> pd.DataFrame:
    
    quantidade_inicial = len(df_itens)
    
    # Filtrar apenas Order IDs validos
    mask_orders = df_itens['order_id'].isin(valid_orders)
    df_itens = df_itens[mask_orders]
    
    # Filtrar apenas Product IDs validos
    mask_products = df_itens['product_id'].isin(valid_products)
    df_itens = df_itens[mask_products]

    # Filtrar apenas Seller IDs validos
    mask_sellers = df_itens['seller_id'].isin(valid_sellers)
    df_itens = df_itens[mask_sellers]
    
    quantidade_final = len(df_itens)
    removidos = quantidade_inicial - quantidade_final
    
    if removidos > 0:
        print(f"{removidos} itens órfãos foram removidos antes do cálculo.")
    else:
        print("Integridade OK.")
        
    return df_itens

def limpar_itens_pedidos(df: pd.DataFrame, valid_orders, valid_products, valid_sellers) -> pd.DataFrame:

    # Remove a inconsistencia antes de fazer contas 
    if valid_orders is not None and valid_products is not None and valid_sellers is not None:
        df = filtrar_orfaos(df, valid_orders, valid_products, valid_sellers)

    # conversao das datas
    if "shipping_limit_date" in df.columns:
        df["shipping_limit_date"] = pd.to_datetime(df["shipping_limit_date"], errors="coerce")

    # mediana e preenchimento
    cols_numericas = ["price", "freight_value"]
    for col in cols_numericas:
        if col in df.columns:
            # Converte para numero
            df[col] = pd.to_numeric(df[col], errors="coerce")
            
            # Calcula a mediana
            mediana = df[col].median()
            
            valor_para_preencher = 0.0
            if not pd.isna(mediana):
                valor_para_preencher = mediana
            
            # Preenche nulos
            df[col] = df[col].fillna(valor_para_preencher)
    
    return df
