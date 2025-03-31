from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from src.utils.bancoPostgres import SessionLocal
from src.models.user import User
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Corrigindo o nome do diretório
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

# Cadastro
@app.get("/cadastro", response_class=HTMLResponse)
async def cadastro_page(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request})

@app.post("/cadastro/info")
async def cadastro(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    novo_usuario = User(name=name, email=email, password=password)
    db.add(novo_usuario)
    db.commit()
    return RedirectResponse(url="/", status_code=303)



# Login
@app.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter_by(email=email, password=password).first()

    if user:
        return RedirectResponse(url="/home", status_code=303)
    else:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Email ou senha incorretos"})

@app.get("/home", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("home1.html", {"request": request})
