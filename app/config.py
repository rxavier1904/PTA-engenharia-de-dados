VALID_ORDERS = set()
VALID_PRODUCTS = set()
VALID_SELLERS = set()


def atualizar_ids_referencia(df, tipo):
    if tipo == 'pedidos':
        VALID_ORDERS.update(df['order_id'].astype(str))
    elif tipo == 'produtos':
        VALID_PRODUCTS.update(df['product_id'].astype(str))
    elif tipo == 'vendedores':
        VALID_SELLERS.update(df['seller_id'].astype(str))

    print(f"[CONFIG] {tipo} carregado. Total atual: "
          f"{len(VALID_ORDERS)} pedidos, "
          f"{len(VALID_PRODUCTS)} produtos, "
          f"{len(VALID_SELLERS)} vendedores.")
