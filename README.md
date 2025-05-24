# **SignAI - Backend FastAPI**

Repositório do projeto **SignAI**, no qual será desenvolvido o sistema.

## **📌 1. Clonando o Repositório**

Caso não consiga dar `git clone`, tente usar seu token como senha. O Git não suporta mais senha do GitHub, apenas o token.

### **Comando para Clonar:**

```bash
git clone https://<SEU_TOKEN_CLASSIC_COM_OPÇÕES_HABILITADAS_DE_REPO>@github.com/Projetct-SignAI/SignAI.git
```

### **Comando para Push:**

Caso não consiga dar `git push`, utilize o seguinte comando:

```bash
git push https://<SEU_TOKEN_DA_CONTA>@github.com/UsuarioGit/SignAI.git
```

---

## **📌 2. Instalação das Dependências**

### **Instalar todas as dependências**

**Instala pelo requirements**

```sh
pip install -r requirements.txt
```

---

## **📌 3. Configuração do Banco de Dados (PostgreSQL)**

### **Criar o banco de dados**

Se o banco de dados ainda não existir, crie-o executando no **psql**:

```sql
CREATE DATABASE SignAI;
```

### **Criar a tabela **``

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha TEXT NOT NULL
);
```

### **Verificar se o PostgreSQL está rodando**

```sh
pg_ctl status
```

Caso não esteja rodando, inicie o servidor:

```sh
pg_ctl start -D "C:\Program Files\PostgreSQL\17\data"
```

Verifique a conexão com o banco:

```sh
psql -U postgres -d SignAI -h localhost -p 5432
```

---

## **📌 4. Estrutura do Projeto**

```plaintext
SignAI/
├── src/                     
│   ├── __init__.py
│   ├── main.py             # Arquivo principal
│   ├── routes/
│   │   ├── rotas.py        # Define as rotas
│   ├── models/
│   │   ├── user.py         # Define o modelo do banco
│   ├── utils/
│   │   ├── bancoPostgres.py # Conexão com PostgreSQL
│
├── static/                  # Arquivos estáticos (CSS, JS, imagens)
│   ├── css/
│   │   └── login.css
│
├── templates/              # Arquivos HTML (renderizados pelo FastAPI)
│   ├── login.html
│   ├── cadastro.html
│   ├── base.html            # Template base
│   └── home.html            # Página inicial
│
├── requirements.txt        # Lista de dependências
├── README.md               # Documentação do projeto
└── .gitignore              # Arquivos a serem ignorados no Git
```

---

## **📌 5. Executando o Servidor**

Para rodar a API FastAPI com Uvicorn, use:

```sh
uvicorn src.main:app --reload
```
NÃO ESQUECER DE RODAR EM APP

Acesse no navegador:

```
http://127.0.0.1:8000
```

A documentação interativa da API pode ser acessada em:

```
http://127.0.0.1:8000/docs
```

---

## **📌 6. Problemas Comuns e Soluções**

### **Erro: **``

Solução:

- Verifique se o PostgreSQL está rodando (`pg_ctl status`).
- Confirme que a string de conexão no código está correta:
  ```python
  DATABASE_URL = "postgresql://postgres:senha@localhost:5432/SignAI"
  ```

### **Erro: Arquivos estáticos não carregam (**``**)**

Solução:

1. Certifique-se de que o FastAPI está montando a pasta `static`:
   ```python
   from fastapi.staticfiles import StaticFiles
   app.mount("/static", StaticFiles(directory="static"), name="static")
   ```
2. No HTML, referencie os arquivos corretamente:
   ```html
   <link rel="stylesheet" href="/static/css/login.css">
   ```

---

## **📌 7. O que foi atualizado**

# SignAI - Atualização 0.4 - IA e automação 

#### 🤖 Reconhecimento de Gestos com Webcam + IA no Backend

Esta versão introduz um pipeline simplificado de inferência:  
o navegador captura frames da webcam, envia ao backend e recebe o gesto traduzido em tempo-real (sem treino online).

### 🛠 Tecnologias Utilizadas
- **MediaPipe Hands** para detecção de pontos da mão no backend.  
- **OpenCV** para captura e pré-processamento.  
- **Scikit-learn (RandomForest)** para classificar gestos a partir dos pontos.  
- **Fetch API + FormData** no frontend para upload contínuo de snapshots JPEG.

---

## 📌 Instalação e Configuração

### 1️⃣ Atualizar Dependências
```bash
pip install -r requirements.txt
---

## Observações

- Este README será atualizado e complementado com mais informações ao longo do desenvolvimento.
- Certifique-se de ter as permissões adequadas para clonar e realizar push no repositório.
