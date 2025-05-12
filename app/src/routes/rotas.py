#Rota dedicada para as funcionalidades de autenticação e cadastro e login de usuários
from fastapi import FastAPI, Depends, Request, Form, APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.utils.bancoPostgres import SessionLocal
from src.models.user import User
from src.utils.auth import create_access_token, verify_password, get_password_hash
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext
import logging
from src.routes.rotaFunc import router as rotaFunc


logging.basicConfig(level=logging.INFO)


# Configuração do FastAPI
app = FastAPI()
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Configuração de hashing com Argon2
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Configuração do JWT
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"

templates = Jinja2Templates(directory="templates")

# Montar arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependência para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/home", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("home1.html", {"request": request})

# Cadastro
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
    # Verifica se o usuário já existe
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    # Cria um novo usuário
    hashed_password = hash_password(user.password)
    new_user = User(name=user.name, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuário cadastrado com sucesso!"}


# Login
@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    access_token = create_access_token(data={"sub": user.email})
    return JSONResponse(content={"access_token": access_token, "token_type": "bearer"}, status_code=200)

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/user-info")
def get_user_info(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    return {"email": user.email, "name": user.name}


# Incluindo os módulos de rota
app.include_router(rotaFunc) 
app.include_router(router)

