import pandas as pd
import os

# Configuração de Caminhos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Variáveis Globais 
VALID_ORDERS = set()
VALID_PRODUCTS = set()
VALID_SELLERS = set()

def carregar_dados_referencia():
    
    print(f"Buscando CSVs em: {DATA_DIR}")

    try:
        # Carrega pedidos 
        path_orders = os.path.join(DATA_DIR, "[Rafael] DataLake - pedidos.csv") 
        
        if os.path.exists(path_orders):
            df = pd.read_csv(path_orders, usecols=['order_id'])
            
            VALID_ORDERS.clear()                # Limpa sujeira antiga
            VALID_ORDERS.update(set(df['order_id'])) # Enche a caixa existente
            
            print(f"Pedidos carregados: {len(VALID_ORDERS)} IDs")
        else:
            print(f"Arquivo não encontrado: {path_orders}")

        #Carrega produtos
        path_products = os.path.join(DATA_DIR, "[Rafael] DataLake - produtos.csv")
        
        if os.path.exists(path_products):
            df = pd.read_csv(path_products, usecols=['product_id'])
            
            VALID_PRODUCTS.clear()
            VALID_PRODUCTS.update(set(df['product_id']))
            
            print(f"Produtos carregados: {len(VALID_PRODUCTS)} IDs")
        else:
             print(f"Arquivo não encontrado: {path_products}")

        # Carrega vendedores
        path_sellers = os.path.join(DATA_DIR, "[Rafael] DataLake - vendedores.csv")
        
        if os.path.exists(path_sellers):
            df = pd.read_csv(path_sellers, usecols=['seller_id'])
            
            VALID_SELLERS.clear()
            VALID_SELLERS.update(set(df['seller_id']))
            
            print(f"Vendedores carregados: {len(VALID_SELLERS)} IDs")
        else:
             print(f"Arquivo não encontrado: {path_sellers}")

    except Exception as e:
        print(f"Erro crítico ao ler CSVs: {e}")
