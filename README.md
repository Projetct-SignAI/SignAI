# 🧠 SignAI – Backend com FastAPI

<div align="center">
   <img src="https://img.shields.io/badge/FastAPI-0.110.0-green?logo=fastapi" alt="FastAPI" />
   <img src="https://img.shields.io/badge/PostgreSQL-17-blue?logo=postgresql" alt="PostgreSQL" />
   <img src="https://img.shields.io/badge/CI/CD-ready-brightgreen?logo=githubactions" alt="CI/CD" />
</div>

**SignAI** é uma solução inovadora que utiliza **Inteligência Artificial** e **Visão Computacional** para traduzir sinais da Língua Brasileira de Sinais (Libras) em **texto e áudio em tempo real**. Este repositório contém o back-end da aplicação, construído com **FastAPI**, **PostgreSQL**, e preparado para **CI/CD** e **deploy em nuvem**.

> ⚠️ **Atenção:** A aplicação ainda **não está publicada online**. Este repositório refere-se à versão local do sistema em desenvolvimento.

---

## 📽️ Demonstração

> 🔗 Em breve será disponibilizado aqui um vídeo demonstrando o sistema em funcionamento.

<!-- Exemplo:
[🎬 Clique para assistir à demo](https://www.youtube.com/watch?v=video-demo)
-->

---

## 📂 Índice

1. [Clonando o repositório](#-1-clonando-o-repositório)
2. [Instalando as dependências](#-2-instalação-das-dependências)
3. [Configuração do banco de dados](#-3-configuração-do-banco-de-dados-postgresql)
4. [Estrutura do projeto](#-4-estrutura-do-projeto)
5. [Executando o servidor](#-5-executando-o-servidor)
6. [Problemas comuns e soluções](#-6-problemas-comuns-e-soluções)
7. [Atualizações](#-7-o-que-foi-atualizado)
8. [Observações finais](#-observações)

---

## 📌 1. Clonando o Repositório

> 🔐 Caso não consiga dar `git clone`, use seu **token** como senha. O GitHub aceita apenas tokens.

```bash
git clone https://<SEU_TOKEN_CLASSIC_COM_OPÇÕES_HABILITADAS_DE_REPO>@github.com/Projetct-SignAI/SignAI.git
```

**Comando para Push:**

```bash
git push https://<SEU_TOKEN_DA_CONTA>@github.com/UsuarioGit/SignAI.git
```

---

## 📌 2. Instalação das Dependências

Instale todos os pacotes necessários com:

```bash
pip install -r requirements.txt
```

---

## 📌 3. Configuração do Banco de Dados (PostgreSQL)

**Criar o banco:**
```sql
CREATE DATABASE SignAI;
```

**Criar a tabela:**
```sql
CREATE TABLE users (
      id SERIAL PRIMARY KEY,
      nome VARCHAR(100) NOT NULL,
      email VARCHAR(100) UNIQUE NOT NULL,
      senha TEXT NOT NULL
);
```

**Verificar se o PostgreSQL está rodando:**
```bash
pg_ctl status
```

**Caso não esteja rodando:**
```bash
pg_ctl start -D "C:\Program Files\PostgreSQL\17\data"
```

**Verifique a conexão:**
```bash
psql -U postgres -d SignAI -h localhost -p 5432
```

---

## 📌 4. Estrutura do Projeto

```plaintext
SignAI/
├── src/
│   ├── main.py                # Arquivo principal da API
│   ├── routes/
│   │   └── rotas.py           # Rotas definidas
│   ├── models/
│   │   └── user.py            # Modelo de dados (ORM)
│   └── utils/
│       └── bancoPostgres.py   # Conexão com PostgreSQL
│
├── static/                    # Arquivos estáticos (CSS, JS, imagens)
│   └── css/
│       └── login.css
│
├── templates/                 # Páginas HTML (renderizadas)
│   ├── base.html
│   ├── login.html
│   ├── cadastro.html
│   └── home.html
│
├── requirements.txt           # Dependências do projeto
├── .gitignore                 # Arquivos ignorados pelo Git
└── README.md                  # Documentação
```

---

## 📌 5. Executando o Servidor

Rode o servidor localmente com Uvicorn:

```bash
uvicorn src.main:app --reload
```

Acesse no navegador:

- App: [`http://127.0.0.1:8000`](http://127.0.0.1:8000)
- Docs interativas: [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)

---

## 📌 6. Problemas Comuns e Soluções

### ❗ PostgreSQL não está rodando

- Verifique o status:
   ```bash
   pg_ctl status
   ```
- Inicie o servidor se necessário:
   ```bash
   pg_ctl start -D "C:\Program Files\PostgreSQL\17\data"
   ```
- Confirme a string de conexão:
   ```python
   DATABASE_URL = "postgresql://postgres:senha@localhost:5432/SignAI"
   ```

---

### ❗ Arquivos estáticos não carregam

1. Certifique-se que está montando a pasta `static` no FastAPI:
    ```python
    from fastapi.staticfiles import StaticFiles
    app.mount("/static", StaticFiles(directory="static"), name="static")
    ```
2. No HTML, use:
    ```html
    <link rel="stylesheet" href="/static/css/login.css">
    ```

---

## 📌 7. O que foi atualizado

### 🚀 SignAI - Versão 0.4

- Implementações de IA e automações
- Preparação para CI/CD
- Autenticação JWT
- Tradução de Libras via webcam com TensorFlow + OpenCV + MediaPipe

---

## 📌 Observações

- Este README será atualizado com instruções de deploy e mais detalhes técnicos ao longo do desenvolvimento.
- Certifique-se de ter permissões adequadas para clonar e enviar alterações ao repositório.

---

<div align="center">

Feito com ❤️ por <b>Equipe SignAI</b> — Promovendo acessibilidade com tecnologia.

</div>
