#Rota Dedicada para as funções do SignAI: Captar Sinais, Traduzir Sinais e Historico
from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.machineL.sinalModel import traduzir_video

router = APIRouter()

# Templates
templates = Jinja2Templates(directory="templates")

# Rota para a Captura de Sinais
@router.get("/captarSinais", response_class=HTMLResponse)
async def sinais_Page(request: Request):
    return templates.TemplateResponse("captarSinais.html", {"request": request})

# Rota para enviar o vídeo
@router.post("/upload_video/")
async def upload_video(video: UploadFile = File(...)):
    conteudo = await video.read()
    resultado = traduzir_video(conteudo)
    return {"traducao": resultado}
