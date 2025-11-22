import os
import json
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials


def _get_credentials():
    """
    Carrega credenciais do Google.
    - LOCAL: usa o arquivo service_account.json
    - RENDER: usa GOOGLE_SERVICE_ACCOUNT_KEY
    """

    creds_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_KEY")

    if creds_json:
        #render: variável de ambiente
        creds_dict = json.loads(creds_json)
    else:
        # local: arquivo físico
        local_path = "app/credentials/service_account.json"

        if not os.path.exists(local_path):
            raise Exception(
                "Nenhuma credencial encontrada. "
                "Defina GOOGLE_SERVICE_ACCOUNT_KEY ou coloque o arquivo local."
            )

        with open(local_path, "r") as f:
            creds_dict = json.load(f)

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    credentials = Credentials.from_service_account_info(
        creds_dict,
        scopes=scopes
    )

    return credentials



def load_sheet(document_name: str, sheet_name: str):
    creds = _get_credentials()
    client = gspread.authorize(creds)

    try:
        sheet = client.open(document_name).worksheet(sheet_name)
    except Exception as e:
        raise Exception(
            f"Erro ao acessar aba '{sheet_name}' do documento '{document_name}': {e}"
        )

    df = pd.DataFrame(sheet.get_all_records())
    return df


#so utilizado para inicializacao(parte de tratar a tabela completa)
def write_sheet(document_name: str, sheet_name: str, df: pd.DataFrame):
    creds = _get_credentials()
    client = gspread.authorize(creds)

    sheet = client.open(document_name).worksheet(sheet_name)

    # limpa tudo
    sheet.clear()

    # reescreve
    valores = [df.columns.tolist()] + df.astype(str).values.tolist()
    sheet.update(valores)
