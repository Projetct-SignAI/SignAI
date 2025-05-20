#Rota Dedicada para as funções do SignAI: Captar Sinais, Traduzir Sinais e Historico
from fastapi import APIRouter,HTTPException ,UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.machineL.sinalModel import traduzir_video
from pydantic import BaseModel
import numpy as np
import joblib
import os



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

# ---- carregamento do modelo KNN ------------------------------------------------
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "modelo_knn_oi.pkl")

try:
    knn_model = joblib.load(MODEL_PATH)
except FileNotFoundError as e:
    raise RuntimeError(f"❌ Modelo não encontrado em {MODEL_PATH}. Treine primeiro.") from e
# -------------------------------------------------------------------------------

# payload esperado do frontend
class LandmarkRequest(BaseModel):
    landmarks: list[float]  # vetor 63 números (21 pontos × 3)

@router.post("/reconhecer/")
async def reconhecer_gesto(req: LandmarkRequest):
    if len(req.landmarks) != 63:
        raise HTTPException(status_code=400, detail="Landmarks incompletos")

    vetor = np.array(req.landmarks).reshape(1, -1)
    
    # Calcule distância para validação
    distances, indices = knn_model.kneighbors(vetor)
    limiar_confianca = 0.15  # Ajuste conforme seus dados
    
    if distances[0][0] > limiar_confianca:
        return {"gesture": "desconhecido"}
    
    pred = knn_model.predict(vetor)[0]
    return {"gesture": pred}