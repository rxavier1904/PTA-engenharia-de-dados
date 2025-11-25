import pandas as pd

def limpar_pedidos(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()


    colunas_indesejadas = [
        "message", "dados", "total_registros",
        "tempo_entrega_dias", "tempo_entrega_estimado_dias", 
        "entrega_no_prazo"
    ]
    df = df.drop(columns=[c for c in colunas_indesejadas if c in df.columns], errors="ignore")


    df = df.replace("", pd.NA)


    if "order_status" in df.columns:
        df["order_status"] = df["order_status"].astype(str)
        df["order_status"] = df["order_status"].replace("nan", pd.NA)

  
    colunas_data = [
        'order_purchase_timestamp',
        'order_approved_at',
        'order_delivered_carrier_date',
        'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ]

    for coluna in colunas_data:
        if coluna in df.columns:
            df[coluna] = pd.to_datetime(df[coluna].astype(str), errors='coerce', utc=True)
            df[coluna] = df[coluna].dt.tz_convert(None)   

 
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

    if "order_status" in df.columns:
        df["order_status"] = df["order_status"].astype(str)
        df["order_status"] = df["order_status"].replace("nan", pd.NA)
        df["order_status"] = df["order_status"].str.strip().str.lower()
        df["order_status"] = df["order_status"].map(mapa_status).fillna(df["order_status"])

   
    if "order_delivered_customer_date" in df.columns and "order_purchase_timestamp" in df.columns:
        df["tempo_entrega_dias"] = (
            df["order_delivered_customer_date"] - df["order_purchase_timestamp"]
        ).dt.days


    if "order_estimated_delivery_date" in df.columns and "order_purchase_timestamp" in df.columns:
        df["tempo_entrega_estimado_dias"] = (
            df["order_estimated_delivery_date"] - df["order_purchase_timestamp"]
        ).dt.days

 
    if "order_delivered_customer_date" in df.columns and "order_estimated_delivery_date" in df.columns:
        def entrega_no_prazo(row):
            if pd.isna(row["order_delivered_customer_date"]):
                return "Não Entregue"
            return "Sim" if row["order_delivered_customer_date"] <= row["order_estimated_delivery_date"] else "Não"

        df["entrega_no_prazo"] = df.apply(entrega_no_prazo, axis=1)

    return df
