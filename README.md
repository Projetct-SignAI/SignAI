<div align="center">

# 🧠 Projeto SignAI

<img src="https://img.shields.io/badge/FastAPI-0.110.0-green?logo=fastapi" alt="FastAPI" />
<img src="https://img.shields.io/badge/PostgreSQL-17-blue?logo=postgresql" alt="PostgreSQL" />
<img src="https://img.shields.io/badge/CI/CD-ready-brightgreen?logo=githubactions" alt="CI/CD" />
<img src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow" alt="Status" />

</div>

---

## 🎬 Apresentação do projeto (vídeo)

<div align="center">

<a href="https://drive.google.com/file/d/1HmkpBXraKy5qW87G8f7KKbOgdGh3V8La/view?usp=drive_link" target="_blank">
  <img src="https://img.icons8.com/ios-filled/100/000000/play-button-circled.png" width="70" alt="Play"/>
</a>

<b>▶️ Assistir à demonstração do SignAI</b>

</div>

No vídeo, apresentamos a proposta do **SignAI**, uma solução que une **Inteligência Artificial** e **Visão Computacional** para apoiar a **acessibilidade** na comunicação. Mostramos o conceito do projeto, o objetivo central de **reduzir barreiras entre pessoas surdas e ouvintes**, e uma visão prática de como a plataforma pretende traduzir sinais de **Libras** para **texto** (com evolução para **áudio**) em tempo real.

> ⚠️ **Atenção:** A aplicação ainda **não está publicada online**. Este repositório refere-se à versão local em desenvolvimento.

---

## 🎓 Contexto Acadêmico (Projeto Integrador)

Este projeto foi **desenvolvido no contexto da disciplina de Projeto Integrador** do **Centro Universitário de Brasília (UniCEUB)**, como parte de uma iniciativa acadêmica voltada à **inovação**, **impacto social** e **aplicação prática** de tecnologia em um cenário real.

📍 **Instituição:** UniCEUB — Brasília/DF  
🧑‍💻 **Ambiente:** Universitário / Acadêmico  
💡 **Foco:** Acessibilidade, inclusão e transformação social com IA

<div align="center">

<img src="app/static/images/instituição%20logo.png" alt="Logo UniCEUB" width="180" />

</div>

---

## 🚀 O que foi atualizado

### 🤖 IA & Automações
- Pipeline completo: **coleta → dataset → treino → inferência**
- Padronização de features: **2 mãos × 21 pontos × 3 coordenadas = 126 features por frame** *(a fazer)*
- Normalização por mão *(em desenvolvimento)*
- Ordenação das mãos (**esquerda → direita**) para consistência
- Padding automático com zeros quando apenas **1 mão** é detectada

### 🔁 Preparação para CI/CD
- Estrutura de diretórios organizada para versionamento
- Dataset salvo em **NumPy `.npz`**
- Modelo salvo em **Pickle `.pkl`**

### 🔐 Autenticação (JWT)
- Mantida da versão anterior, já integrada no backend

### 📹 Tradução Libras via Webcam (TensorFlow + OpenCV + MediaPipe)
- Captura de vídeo em tempo real
- Extração de landmarks (x, y, z)
- Inferência de sequências com modelo baseado em **LSTM/GRU**
- Exibição do gesto reconhecido diretamente no frame da webcam

---

## 🧩 Espaço reservado

<!-- 
✅ Use este espaço para futuras infos, prints, gif, roadmap, links, etc.
Sugestões:
- Roadmap
- Prints/GIFs da aplicação
- Diagrama da arquitetura
- Links de apresentação/paper
-->

---

<div align="center">

Feito com ❤️ por <b>Equipe SignAI</b> — Promovendo acessibilidade com tecnologia.

</div>