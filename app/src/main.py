import uvicorn
from src.routes.rotas import app
from fastapi.staticfiles import StaticFiles


app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
