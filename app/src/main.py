import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# 🔗 importa os routers
from src.routes.rotas import router as paginas_router
from src.routes.rotas import reconhecer_router
from src.routes.rotaFunc import router as rotaFunc_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# registra tudo
app.include_router(paginas_router)      # /, /home, /cadastro, /sobre, etc.
app.include_router(rotaFunc_router)     # suas rotas de funcionalidades
app.include_router(reconhecer_router)   # /reconhecer/...

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
