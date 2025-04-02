from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "seu_segredo_super_secreto"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

ph = PasswordHasher()


def create_access_token(data: dict):
    """Cria um token JWT com tempo de expiração"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_password_hash(password: str) -> str:
    """Gera um hash seguro para a senha usando Argon2"""
    hashed_password = ph.hash(password)
    if not hashed_password:
        raise ValueError("Falha ao gerar o hash da senha.")
    return hashed_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha digitada corresponde ao hash armazenado"""
    try:
        resultado = ph.verify(hashed_password, plain_password)  # Ordem corrigida!
        print(f"✅ Senha correta! ({plain_password})")
        return resultado
    except VerifyMismatchError:
        print("❌ Senha incorreta!")
        return False
    except Exception as e:
        print(f"⚠️ Erro ao verificar senha: {e}")
        return False



