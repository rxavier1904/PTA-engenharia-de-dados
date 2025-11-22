from fastapi import FastAPI

# função que vai carregar as dimensões automaticamente na memória
from app.core.initializer import inicializar_dimensoes

# importa cada router corretamente separado
from app.routers.pedidos import router as pedidos_router
from app.routers.produtos_router import router as produtos_router
from app.routers.vendedores import router as vendedores_router
from app.routers.itens_pedidos import router as itens_pedidos_router
from app.routers.dimensoes_router import router as dimensoes_router

from app.routers.admin_router import router as admin_router

from fastapi import APIRouter


app = FastAPI(
    title="API de Tratamento de Dados - Desafio 1",
    description="API que recebe dados brutos, trata e devolve limpos.",
    version="2.0.0"
)

# Carrega dimensões automaticamente ao iniciar o servidor


#@app.on_event("startup")
#def startup_event():
    #print("[STARTUP] Inicializando dimensões (pedidos, produtos, vendedores)...")
    #inicializar_dimensoes()
   #print("[STARTUP] Dimensões carregadas com sucesso!")


@app.get("/", description="Mensagem de boas-vindas da API.")
async def read_root():
    return {"message": "API funcionando com inicialização automática de dimensões!"}


@app.get("/health", description="Verifica o status da API.")
async def health_check():
    return {"status": "ok"}


# Rotas agrupadas
app.include_router(dimensoes_router, prefix="/dimensoes", tags=["Dimensões"])
app.include_router(pedidos_router, prefix="/pedidos", tags=["Pedidos"])
app.include_router(produtos_router, prefix="/produtos", tags=["Produtos"])
app.include_router(vendedores_router, prefix="/vendedores",
                   tags=["Vendedores"])
app.include_router(itens_pedidos_router,
                   prefix="/itens_pedidos", tags=["Itens de Pedidos"])
app.include_router(admin_router)

admin_local_router = APIRouter()

@admin_local_router.post("/rodar_carga_inicial")
def rodar_carga():
    inicializar_dimensoes()
    return {"status": "Carga inicial concluída!"}

app.include_router(admin_local_router, prefix="/admin_local", tags=["Admin Local"])