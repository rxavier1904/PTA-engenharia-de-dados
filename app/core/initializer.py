import pandas as pd
from app.core.google_client import load_sheet, write_sheet
from app.services.limpeza_pedidos import limpar_pedidos
from app.services.produtos_services import limpar_produtos
from app.services.vendedores_services import limpar_vendedores
from app.config import atualizar_ids_referencia


DOCUMENTO = "[Rafael] DataLake"


def inicializar_dimensoes():
    print("\nCARGA INICIAL DAS DIMENSÕES")

    ##1) Ler sheets originais
    df_pedidos = load_sheet(DOCUMENTO, "pedidos")
    df_produtos = load_sheet(DOCUMENTO, "produtos")
    df_vendedores = load_sheet(DOCUMENTO, "vendedores")
    df_itens = load_sheet(DOCUMENTO, "itens_pedidos")

    ##2) Tratar tudo
    df_pedidos = limpar_pedidos(df_pedidos)
    df_produtos = limpar_produtos(df_produtos)
    df_vendedores = limpar_vendedores(df_vendedores)

    ##3) Atualizar IDs válidos globais
    atualizar_ids_referencia(df_pedidos, "pedidos")
    atualizar_ids_referencia(df_produtos, "produtos")
    atualizar_ids_referencia(df_vendedores, "vendedores")

    print("Dimensões carregadas com sucesso!\n")

    write_sheet(DOCUMENTO, "produtos", df_produtos)
    write_sheet(DOCUMENTO, "pedidos", df_pedidos)
    write_sheet(DOCUMENTO, "vendedores", df_vendedores)
    write_sheet(DOCUMENTO, "itens_pedidos", df_itens)

    print(" Tabelas escritas com sucesso!\n")
