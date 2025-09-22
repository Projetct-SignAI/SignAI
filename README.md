# 🧠 SignAI – Backend com FastAPI

<div align="center">
   <img src="https://img.shields.io/badge/FastAPI-0.110.0-green?logo=fastapi" alt="FastAPI" />
   <img src="https://img.shields.io/badge/PostgreSQL-17-blue?logo=postgresql" alt="PostgreSQL" />
   <img src="https://img.shields.io/badge/CI/CD-ready-brightgreen?logo=githubactions" alt="CI/CD" />
   <img src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow" alt="Status" />
</div>

---

## 🚀 Sobre o SignAI

**SignAI** é uma **startup** focada em **acessibilidade** e **inclusão social**, usando **Inteligência Artificial** e **Visão Computacional** para traduzir, em tempo real, sinais da Língua Brasileira de Sinais (Libras) em **texto** e **áudio**. Nosso objetivo é:

- **Democratizar** o acesso à comunicação para pessoas surdas.
- Reduzir a **dependência** de intérpretes humanos.
- Oferecer uma **solução escalável**, de **baixo custo** e fácil manutenção.
- Ampliar oportunidades **educacionais**, **profissionais** e **governamentais**.

> ⚠️ **Atenção:** A aplicação ainda **não está publicada online**. Este repositório refere-se à versão local em desenvolvimento.

---

## 🎯 Visão & Missão

**Visão:** Ser a principal plataforma de tradução automática de Línguas de Sinais no Brasil até 2026.  
**Missão:** Construir tecnologia que elimine barreiras de comunicação, promovendo empatia e inclusão por meio de inovação contínua.

---

## 👥 Equipe Fundadora

<div align="center">
    <table>
         <tr>
             <td align="center">
                  <img src="app/static/images/eurico.png" alt="Fundador 1" style="width:120px; height:120px; object-fit:cover;" /><br>
                  <strong>Eduardo Eurico</strong><br>
                  Co-Founder
             </td>
             <td align="center">
                  <img src="app/static/images/vini.png" alt="Fundador 2" style="width:100px; height:120px; object-fit:cover;" /><br>
                  <strong>Vinícius Rodrigues</strong><br>
                  Co-Founder
             </td>
             <td align="center">
                  <img src="app/static/images/roger.png" alt="Fundador 3" style="width:120px; height:120px; object-fit:cover;" /><br>
                  <strong>Roger Arraz</strong><br>
                  Co-Founder
             </td>
         </tr>
    </table>
</div>

---

<div align="center">

🎬 <strong>Assista à demonstração:</strong><br>
<a href="https://youtu.be/HUchOBB0NRg" target="_blank">
   <img src="https://img.icons8.com/ios-filled/100/000000/play-button-circled.png" alt="Play Video" width="80" /><br>
   <b>Clique aqui para ver o vídeo da aplicação em ação</b>
</a>

</div>

---

## 📂 Índice

1. [Clonando o repositório](#-1-clonando-o-repositório)  
2. [Instalação das Dependências](#-2-instalação-das-dependências)  
3. [Configuração do Banco de Dados](#-3-configuração-do-banco-de-dados-postgresql)  
4. [Estrutura do Projeto](#-4-estrutura-do-projeto)  
5. [Executando o Servidor](#-5-executando-o-servidor)  
6. [Problemas Comuns & Soluções](#-6-problemas-comuns--soluções)  
7. [Roadmap & Atualizações](#-7-roadmap--atualizações)  
8. [Observações Finais](#-8-observações-finais)  

---

## 📌 1. Clonando o Repositório

> 🔐 Use seu **token** caso o `git clone` solicite autenticação.

```bash
git clone https://<SEU_TOKEN>@github.com/Projetct-SignAI/SignAI.git
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

### 🚀 SignAI - Versão 0.5

## 🚀 O que foi atualizado

- **Implementações de IA e automações**
  - Pipeline completo de coleta → criação de dataset → treinamento → inferência.
  - Padronização das features: **2 mãos × 21 pontos × 3 coordenadas = 126 features por frame**. //A fazer
  - Normalização por mão (mínimo de x, y, z). Em Desenvolvimento
  - Ordenação das mãos (esquerda → direita) para consistência.
  - Padding automático com zeros quando apenas 1 mão é detectada.

- **Preparação para CI/CD**
  - Estrutura de diretórios organizada para versionamento.
  - Arquivos de dataset salvos em formato **NumPy `.npz`**.
  - Modelo de rede neural salvo em **Pickle `.pkl`**.

- **Autenticação JWT**
  - Mantida da versão anterior, já integrada no backend.

- **Tradução de Libras para modelo de video via webcam com TensorFlow + OpenCV + MediaPipe**
  - Captura de vídeo em tempo real.
  - Extração de landmarks em 3D (x, y).
  - Inferência de sequências com modelo baseado em LSTM/GRU.
  - Visualização do gesto reconhecido diretamente sobre o frame da webcam.

---

## 📌 8. Observações Finais

- Este README será atualizado com instruções de deploy e mais detalhes técnicos ao longo do desenvolvimento.
- Certifique-se de ter permissões adequadas para clonar e enviar alterações ao repositório.

---

<div align="center">

Feito com ❤️ por <b>Equipe SignAI</b> — Promovendo acessibilidade com tecnologia.

</div>
