# src/routes/rotas.py
"""
Rotas de páginas, autenticação e utilidades do SignAI.

❗  Este módulo **NÃO** cria objeto FastAPI().  
    Ele apenas define um ou mais APIRouters que devem ser incluídos
    no app principal (src/main.py) com `app.include_router(...)`.
"""

# ---------------------------------------------------------------------
# Ajuste de MIME para servir JS como application/javascript
# ---------------------------------------------------------------------
import mimetypes
mimetypes.add_type("application/javascript", ".js", strict=True)

# ---------------------------------------------------------------------
# Imports padrão FastAPI / utilitários
# ---------------------------------------------------------------------
import logging
from datetime import timedelta
from fastapi import (
    APIRouter, Depends, HTTPException, Request,
    Response
)
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field, EmailStr, field_validator
from sqlalchemy.orm import Session
import joblib
import numpy as np

# ---------------------------------------------------------------------
# Imports de camadas internas
# ---------------------------------------------------------------------
from src.utils.bancoPostgres import SessionLocal
from src.models.user import User
from src.utils.auth import (
    create_access_token, verify_password, get_password_hash,
    SECRET_KEY, ALGORITHM
)

# (APIRouter com rotas de negócios/funcionalidades)
from src.routes.rotaFunc import router as rotaFunc   # será incluído no main.py

# ---------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)

router = APIRouter()                      # ← router principal deste módulo
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
templates = Jinja2Templates(directory="templates")
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# ---------------------------------------------------------------------
# Dependência: sessão de banco
# ---------------------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------------------------------------------
# ————————————————————   PÁGINAS PÚBLICAS   ————————————————————
# ---------------------------------------------------------------------
@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/home", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("home1.html", {"request": request})

@router.get("/cadastro", response_class=HTMLResponse)
async def cadastro_page(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request})

@router.get("/sobre", response_class=HTMLResponse)
async def sobre_page(request: Request):
    return templates.TemplateResponse("sobre.html", {"request": request})

@router.get("/texto-para-sinais", response_class=HTMLResponse)
async def texto_para_sinais_page(request: Request):
    return templates.TemplateResponse("texto_para_sinais.html", {"request": request})

@router.get("/perfil", response_class=HTMLResponse)
async def perfil_page(request: Request):
    return templates.TemplateResponse("perfil.html", {"request": request})

# ---------------------------------------------------------------------
# ————————————————————   AUTENTICAÇÃO   ————————————————————
# ---------------------------------------------------------------------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(...)

    @field_validator("password")
    @classmethod
    def senha_muito_curta(cls, v):
        if len(v) < 6:
            raise ValueError("Senha muito curta. Use pelo menos 6 caracteres.")
        return v

@router.post("/cadastro/info")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # validações de unicidade
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(400, "E-mail já cadastrado")
    if db.query(User).filter(User.name == user.name).first():
        raise HTTPException(400, "Nome de usuário já cadastrado")

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Usuário cadastrado com sucesso!"}

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(401, "Credenciais inválidas")

    token = create_access_token(data={"email": user.email, "name": user.name})
    return JSONResponse({"access_token": token, "token_type": "bearer"})

# ---------------------------------------------------------------------
# ————————————————————   PERFIL   ————————————————————
# ---------------------------------------------------------------------
class ProfileUpdate(BaseModel):
    name: str
    email: EmailStr
    password: str | None = None

@router.put("/update-profile")
async def update_profile(
    payload: ProfileUpdate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = decoded.get("email") or decoded.get("sub")
        if not user_email:
            raise HTTPException(401, "Token inválido")

        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            raise HTTPException(404, "Usuário não encontrado")

        # unicidade
        if (db.query(User)
                .filter(User.email == payload.email, User.id != user.id)
                .first()):
            raise HTTPException(400, "E-mail já cadastrado")
        if (db.query(User)
                .filter(User.name == payload.name, User.id != user.id)
                .first()):
            raise HTTPException(400, "Nome de usuário já cadastrado")

        if payload.password and len(payload.password) < 6:
            raise HTTPException(400, "Senha muito curta. Use pelo menos 6 caracteres.")

        user.name = payload.name
        user.email = payload.email
        if payload.password:
            user.password = get_password_hash(payload.password)
        db.commit()

        new_token = create_access_token(data={"email": user.email, "name": user.name})
        return {"message": "Perfil atualizado com sucesso",
                "access_token": new_token, "token_type": "bearer"}

    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expirado")
    except JWTError:
        raise HTTPException(401, "Token inválido")

@router.get("/user-info")
async def get_user_info(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        if not email:
            raise HTTPException(401, "Token inválido")
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(401, "Usuário não encontrado")
    except JWTError:
        raise HTTPException(401, "Token inválido")

    return {"email": user.email, "name": user.name}

# ---------------------------------------------------------------------
# ————————————————————   RECONHECIMENTO DE GESTOS   ————————————————————
# ---------------------------------------------------------------------
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
        raise HTTPException(500, f"Erro na predição: {e}")

# ---------------------------------------------------------------------
# Exporta routers para inclusão no app principal
# ---------------------------------------------------------------------
__all__ = ["router", "reconhecer_router", "rotaFunc"]
