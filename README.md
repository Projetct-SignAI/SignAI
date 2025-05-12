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

# SignAI - Atualização 0.2 - Autenticação 

## 🔒 Autenticação JWT e Hash de Senhas com Argon2

Esta atualização implementa a autenticação de usuários utilizando JWT para gerenciamento de sessões seguras e Argon2 para hashing de senhas.

### 🛠 Tecnologias Utilizadas
- **PyJWT** para geração e validação do token JWT.
- **argon2-cffi** para hashing seguro de senhas.

---

## 📌 Instalação e Configuração

### 1️⃣ Atualizar Dependências
Certifique-se de instalar as novas bibliotecas adicionadas ao projeto:
```bash
pip install -r requirements.txt
```

Se precisar atualizar o arquivo `requirements.txt`, execute:
```bash
pip freeze > requirements.txt
```

### 2️⃣ Configurar a Autenticação
A autenticação foi implementada na rota `/login`, onde o sistema:
1. Verifica as credenciais do usuário.
2. Compara a senha informada com o hash armazenado usando Argon2.
3. Retorna um token JWT em caso de sucesso.

### 3️⃣ Cadastro de Usuários com Hash Seguro
Ao criar um novo usuário, a senha é automaticamente criptografada com Argon2 antes de ser armazenada no banco de dados.


---

## 🚀 Uso do JWT
Após o login bem-sucedido, o sistema retorna um token JWT que deve ser incluído nas requisições autenticadas.

#### Exemplo de Requisição Autenticada:
```bash
curl -H "Authorization: Bearer <SEU_TOKEN_AQUI>" http://localhost:8000/protected-route
```

---

## 🛠 Possíveis Melhorias
- Implementar refresh tokens para sessões persistentes.
- Criar um sistema de recuperação de senha.

Essa atualização melhora a segurança do sistema e a gestão de autenticação dos usuários. Se tiver dúvidas ou sugestões, contribua! 🎯




---

## Observações

- Este README será atualizado e complementado com mais informações ao longo do desenvolvimento.
- Certifique-se de ter as permissões adequadas para clonar e realizar push no repositório.
