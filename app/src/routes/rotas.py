# src/routes/rotas.py

import mimetypes
mimetypes.add_type("application/javascript", ".js", strict=True)

import logging
from fastapi import FastAPI, Depends, Request, HTTPException, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import joblib
import numpy as np

from src.utils.bancoPostgres import SessionLocal
from src.models.user import User
from src.utils.auth import create_access_token, verify_password, get_password_hash
from src.routes.rotaFunc import router as rotaFunc

logging.basicConfig(level=logging.INFO)

# Configuração do FastAPI
app = FastAPI()
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Montagem dos arquivos estáticos (se ainda não estiver feito em main.py)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuração de hashing com Argon2
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Configuração do JWT
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"

templates = Jinja2Templates(directory="templates")


# Dependência para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# —————————————————————————————
# ROTAS DE AUTENTICAÇÃO / PÁGINAS
# —————————————————————————————

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/home", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("home1.html", {"request": request})

@app.get("/cadastro", response_class=HTMLResponse)
async def cadastro_page(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request})


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


@app.post("/cadastro/info")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    new_user = User(name=user.name, email=user.email, password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Usuário cadastrado com sucesso!"}


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    access_token = create_access_token(data={"sub": user.email})
    return JSONResponse({"access_token": access_token, "token_type": "bearer"})


@app.get("/user-info")
async def get_user_info(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    return {"email": user.email, "name": user.name}


# —————————————————————————————
# ROTA DE RECONHECIMENTO DE GESTOS
# —————————————————————————————

# Carrega uma vez o modelo KNN treinado
_model = joblib.load("modelo_knn_oi.pkl")


class LandmarksPayload(BaseModel):
    landmarks: list[float]


reconhecer_router = APIRouter(prefix="/reconhecer", tags=["reconhecimento"])


@reconhecer_router.post("/", summary="Recebe vetor de landmarks e retorna nome do gesto")
async def reconhecer_gesto(payload: LandmarksPayload):
    try:
        vetor = np.array(payload.landmarks, dtype=float).reshape(1, -1)
        pred = _model.predict(vetor)
        return {"gesture": pred[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na predição: {e}")


# —————————————————————————————
# ROTA DE CONVERSÃO DE TEXTO PARA SINAIS
# —————————————————————————————

@app.get("/texto-para-sinais", response_class=HTMLResponse)
async def texto_para_sinais_page(request: Request):
    return templates.TemplateResponse("texto_para_sinais.html", {"request": request})


# —————————————————————————————
# INCLUSÃO DE TODOS OS ROTEADORES
# —————————————————————————————

app.include_router(rotaFunc)
app.include_router(router)
