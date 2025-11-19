import pandas as pd


def limpar_produtos(df: pd.DataFrame) -> pd.DataFrame:
    # substituir valores nulos por indefinido
    df["product_category_name"] = df["product_category_name"].fillna(
        "indefinido")
    # tudo em minuscula, considerando a existencia de valores nulos
    df["product_category_name"] = df["product_category_name"].astype(
        str).str.lower()
    # substituir espacos por _
    df["product_category_name"] = df["product_category_name"].str.replace(
        " ", "_")

    # substituindo nulos pela mediana
    nomes_colunas_numericas = ["product_name_lenght",
                               "product_description_lenght",
                               "product_photos_qty",
                               "product_weight_g",
                               "product_length_cm",
                               "product_height_cm",
                               "product_width_cm"]

    for n in nomes_colunas_numericas:
        mediana = df[n].median()
        df[n] = df[n].fillna(mediana)

    return df


