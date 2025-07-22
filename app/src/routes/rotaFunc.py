# —————————————————————————————
# INCLUSÃO DE TODOS OS ROTEADORES
# —————————————————————————————

#Rota Dedicada para as funções do SignAI: Captar Sinais, Traduzir Sinais e Historico
from fastapi import APIRouter,HTTPException ,UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import numpy as np
import joblib
import os
from src.machineL2.inference_classifier import predict_from_frame_bgr
from fastapi.responses import JSONResponse
import cv2

router = APIRouter()

# —————————————————————————————
# TEMPLATES
# —————————————————————————————
templates = Jinja2Templates(directory="templates")

# —————————————————————————————
# ROTA PARA A PÁGINA DE CAPTAR SINAIS
# —————————————————————————————
@router.get("/captarSinais", response_class=HTMLResponse)
async def sinais_Page(request: Request):
    return templates.TemplateResponse("captarSinais.html", {"request": request})

# —————————————————————————————
# ROTA PARA A PÁGINA DE TRADUZIR SINAIS
# —————————————————————————————
@router.post("/upload_video/")
async def upload_video(video: UploadFile = File(...)):
    conteudo = await video.read()
    resultado = traduzir_video(conteudo)
    return {"traducao": resultado}

# —————————————————————————————
# ROTA PARA MANDAR OS SINAIS PARA O FRONTEND
# —————————————————————————————
@router.post("/reconhecer/")
async def reconhecer_frame(file: UploadFile = File(...)):
    contents = await file.read()
    npimg = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    if frame is None:
        raise HTTPException(400, detail="Imagem inválida")

    gesture = predict_from_frame_bgr(frame)
    return JSONResponse({"gesture": gesture})

# # ---- carregamento do modelo KNN ------------------------------------------------
# MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "modelo_knn_oi.pkl")

# try:
#     knn_model = joblib.load(MODEL_PATH)
# except FileNotFoundError as e:
#     raise RuntimeError(f"❌ Modelo não encontrado em {MODEL_PATH}. Treine primeiro.") from e
# # -------------------------------------------------------------------------------

# # payload esperado do frontend
# class LandmarkRequest(BaseModel):
#     landmarks: list[float]  # vetor 63 números (21 pontos × 3)

# @router.post("/reconhecer/")
# async def reconhecer_gesto(req: LandmarkRequest):
#     if len(req.landmarks) != 63:
#         raise HTTPException(status_code=400, detail="Landmarks incompletos")

#     vetor = np.array(req.landmarks).reshape(1, -1)
    
#     # Calcule distância para validação
#     distances, indices = knn_model.kneighbors(vetor)
#     limiar_confianca = 0.15  # Ajuste conforme seus dados
    
#     if distances[0][0] > limiar_confianca:
#         return {"gesture": "desconhecido"}
    
#     pred = knn_model.predict(vetor)[0]
#     return {"gesture": pred}

#class LandmarkInput(BaseModel):
#    landmarks: list[float]  # 63 floats

#@router.post("/reconhecer/")
#async def reconhecer_l2(body: LandmarkInput):
#    if len(body.landmarks) != 63:
#        raise HTTPException(status_code=400, detail="espera 63 valores")
#    gesto = predict_from_landmarks(body.landmarks)
#    return {"gesture": gesto}