import pandas as pd
import unicodedata

def _remover_acentos(texto):

    #Remove acentos e coloca em maiusculo.
    if isinstance(texto, str):
        # Normalização
        texto_normalizado = unicodedata.normalize('NFKD', texto)
        # Converte pra ASCII
        texto_sem_acento = texto_normalizado.encode('ASCII', 'ignore').decode('ASCII')
        # Retorna em maiúsculo
        return texto_sem_acento.upper()
    return texto

def limpar_vendedores(df: pd.DataFrame) -> pd.DataFrame:
    print("[Service] Iniciando limpeza de Vendedores")
    
    # 1. Tratamento seller_city
    if "seller_city" in df.columns:
        # Aplica a funçao em cada linha
        df["seller_city"] = df["seller_city"].apply(_remover_acentos)

    # 2. Tratamento seller_state
    if "seller_state" in df.columns:
        # Converte pra string e maisuculo
        df["seller_state"] = df["seller_state"].astype(str).str.upper()
        
    return df
