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

**Nota:** Ao importar esses fluxos, lembre-se de atualizar as URLs nos nós "HTTP Request" para o endereço da sua API em produção.

### Arquitetura Técnica
A solução utiliza uma arquitetura orientada a eventos para processamento de dados, integrando **n8n**, **FastAPI** e **Google Sheets**:

1. **Google Sheets (Fonte de Dados):** Atua como o repositório inicial onde os dados brutos são inseridos.
2. **n8n (Orquestrador):**
   - **Trigger:** Monitora as planilhas em busca de novas linhas (eventos `rowAdded`).
   - **Comunicação:** Envia os dados capturados para a API via requisições HTTP (POST).
   - **Persistência:** Recebe os dados limpos da API e atualiza a planilha ou insere em um banco de dados final.
3. **API FastAPI (Processamento):**
   - Recebe o payload JSON do n8n.
   - **Validação:** Utiliza Pydantic para garantir tipos corretos e tratar valores nulos (ex: converter `""` para `None`).
   - **Transformação:** Aplica regras de negócio e limpeza de dados utilizando Pandas.
   - **Resposta:** Retorna o objeto JSON estruturado e pronto para uso.

Esta abordagem desacopla a lógica de transformação (API) da automação de fluxo (n8n), facilitando a manutenção e permitindo que a API seja consumida por outros serviços se necessário.

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

## Configurando o n8n

Para utilizar os fluxos de automação presentes na pasta `n8n/`, você precisará de uma instância do n8n em execução.

### 1. Rodando o n8n
Você pode rodar o n8n facilmente se tiver o Node.js instalado (via npx) ou usando Docker.

**Via npx:**
```bash
npx n8n
```

**Via Docker:**
```bash
docker run -it --rm --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n
```

Após iniciar, acesse o painel em: `http://localhost:5678`

### 2. Importando os Fluxos
1. No menu lateral do n8n, clique em **Workflows**.
2. Selecione **Import from File**.
3. Navegue até a pasta `n8n/` deste repositório e selecione os arquivos JSON (`produtos (2).json`, `Vendedores.json`, etc.).

### 3. Ajustes Finais
- **Credenciais:** Você precisará configurar as credenciais do Google Sheets (OAuth2 ou Service Account) dentro do n8n para que os nós "Google Sheets Trigger" funcionem.
- **Conexão com a API:**
  - Abra os nós **HTTP Request** nos fluxos importados.
  - Atualize a URL para apontar para sua API.
  - **Dica:** Se o n8n estiver rodando em Docker e a API na sua máquina local, use `http://host.docker.internal:8000` em vez de `localhost`.

<br/>


## Contato
<br/>

- [CITi UFPE](https://github.com/CITi-UFPE) - contato@citi.org.br
- [João Pedro Bezerra](https://github.com/jpbezera), Líder de Dados em 2025.2 - jpbmtl@cin.ufpe.br