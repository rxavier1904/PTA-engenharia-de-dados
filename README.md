<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/CITi-UFPE/PTA-engenharia-de-dados">
    <img src="https://ci3.googleusercontent.com/mail-sig/AIorK4zWbC3U-G_vTTZE6rUQqJjzL8u7WNZjzhEaYi9z7slJn8vNhgnFVootxjm377GVCdPGY_F64WolHmGJ" alt="Logo" width="180px">
  </a>

  <h3 align="center">PTA Engenharia de Dados</h3>

  <p align="center">
  Este projeto foi criado em 2025.2 com a proposta de trazer a frente de engenharia de dados para o Processo de Treinamento de Área (PTA) do CITi. Ele foi desenvolvido com base em práticas modernas de engenharia de dados e tem como objetivo capacitar tecnicamente as pessoas aspirantes, alinhando-se às demandas atuais da empresa.
    <br />
    <a href="https://github.com/CITi-UFPE/PTA-engenharia-de-dados"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    ·
    <a href="https://github.com/CITi-UFPE/PTA-engenharia-de-dados/issues">Report Bug</a>
    ·
    <a href="https://github.com/CITi-UFPE/PTA-engenharia-de-dados/issues">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Tabela de Conteúdo</h2></summary>
  <ol>
    <li><a href="#sobre-o-projeto">Sobre o Projeto</a></li>
    <li><a href="#como-instalar">Como Instalar</a></li>
    <li><a href="#como-rodar">Como Rodar</a></li>
    <li><a href="#contato">Contato</a></li>
  </ol>
</details>

<br/>

## Sobre o Projeto
<br/>

Este projeto foi desenvolvido para o Processo de Treinamento de Área (PTA) do CITi, com foco em engenharia de dados. Ele inclui uma API construída com FastAPI, utilizando boas práticas de desenvolvimento e uma estrutura modular para facilitar a manutenção e a escalabilidade. O objetivo principal do projeto é construir uma pipeline completa que consiga ser acessada via uma API.

### Endpoints principais
- `/pedidos/limpar` : Limpa e valida dados de pedidos
- `/produtos/products/processar_produtos` : Limpa e valida dados de produtos
- `/vendedores/limpar` : Limpa e valida dados de vendedores
- `/itens_pedidos/limpar` : Limpa e valida dados de itens de pedidos
- `/dimensoes/*` : Endpoints para dimensões auxiliares
- `/admin_local/rodar_carga_inicial` : Recarrega as dimensões manualmente

### Estrutura de pastas
```
app/
  main.py                # Entrypoint FastAPI
  core/
    initializer.py       # Inicialização das dimensões
    google_client.py     # Integração com Google Sheets
  routers/               # Endpoints FastAPI
    pedidos.py
    produtos_router.py
    vendedores.py
    itens_pedidos.py
    dimensoes_router.py
    admin_router.py
  schemas/               # Schemas Pydantic (validação)
    pedido.py
    produtos.py
    vendedores.py
    itens_pedidos.py
  services/              # Lógica de limpeza/tratamento
    limpeza_pedidos.py
    produtos_services.py
    vendedores_services.py
    itens_pedidos_services.py
  config.py              # Configurações globais
  credentials/           # Credenciais Google
    service_account.json
```

### Fluxos n8n
A pasta `n8n/` contém os workflows exportados utilizados para orquestrar o pipeline de dados:
- **produtos (2).json**: Monitora a planilha de produtos e envia novos registros para limpeza na API.
- **Vendedores.json**: Processo similar para a tabela de vendedores.
- **itens_pedidos_final.json**: Pipeline completo que lê, limpa via API e atualiza os dados de itens de pedidos.
- **pedidos(1).json**: Fluxo para gerenciamento e atualização da tabela de pedidos.

<br/>

## Como Instalar
<br/>

1. Certifique-se de que o **Python** e o **Docker Desktop** estão instalados em sua máquina.

2. Clone o repositório:

   ```sh
   git clone https://github.com/CITi-UFPE/PTA-engenharia-de-dados.git
   ```

3. Entre na pasta do projeto:

   ```sh
   cd PTA-engenharia-de-dados
   ```

<br/>

## Como Rodar

### Usando Docker
<br/>

1. Certifique-se de que o Docker Desktop está em execução.

2. Suba os serviços com o Docker Compose:

   ```sh
   docker-compose up --build
   ```

3. Acesse a aplicação em seu navegador no endereço:

   ```
   http://localhost:8000
   ```

4. Para acessar a documentação interativa da API (Swagger UI), vá para:

   ```
   http://localhost:8000/docs
   ```

<br/>

### Localmente
<br/>

1. Certifique-se de que esteja no diretório principal

2. Instale as dependências: 
    ```
    pip install -r ./requirements.txt
    ```

3. Execute o projeto: 
    ```
    uvicorn app.main:app
    ```

4. Acesse a aplicação em seu navegador no endereço:

   ```
   http://localhost:8000
   ```

5. Para acessar a documentação interativa da API (Swagger UI), vá para:

   ```
   http://localhost:8000/docs
   ```

<br/>


## Contato
<br/>

- [CITi UFPE](https://github.com/CITi-UFPE) - contato@citi.org.br
- [João Pedro Bezerra](https://github.com/jpbezera), Líder de Dados em 2025.2 - jpbmtl@cin.ufpe.br