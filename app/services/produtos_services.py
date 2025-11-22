import pandas as pd


def limpar_produtos(df: pd.DataFrame) -> pd.DataFrame:
    
    # Substituir valores nulos por 'indefinido'
    df["product_category_name"] = df["product_category_name"].fillna("indefinido")
    
    # Converter para string, minúsculo e substituir espaços por _
    df["product_category_name"] = (
        df["product_category_name"]
        .astype(str)
        .str.lower()
        .str.replace(" ", "_")
    )
    
    colunas_numericas = [
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ]

    for coluna in colunas_numericas:

        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")
        mediana = df[coluna].median()
        df[coluna] = df[coluna].fillna(mediana)


    return df
