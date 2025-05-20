// landmark.js
// Versão completa corrigida das importações
import * as tf from "https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.5.0/+esm";
import "https://cdn.jsdelivr.net/npm/@tensorflow/tfjs-backend-webgl@4.5.0/+esm";
import * as handpose from "https://cdn.jsdelivr.net/npm/@tensorflow-models/handpose@0.7.0/+esm";

const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const gestureSpan = document.getElementById("gestureName");
const ctx = canvas.getContext("2d");

const btnArquivo = document.getElementById("btnArquivo");
const filePicker = document.getElementById("filePicker");
const status = document.getElementById("status");

const API_URL = "/reconhecer/";

let hpModel = null;

async function init() {
  await tf.setBackend("webgl");
  hpModel = await handpose.load();
  status.textContent = "Modelo carregado. Escolha um vídeo.";
  loop();
}

// Laço principal
async function loop() {
  if (video.readyState >= 2) {
    const preds = await hpModel.estimateHands(video);
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (preds.length > 0) {
      const landmarks = preds[0].landmarks;
      desenhaPontos(landmarks);

      const flat = landmarks.flat();
      const gesto = await reconhecerBackend(flat);
      gestureSpan.textContent = gesto;
    } else {
      gestureSpan.textContent = "—";
    }
  }

  requestAnimationFrame(loop);
}

// Desenha pontos vermelhos nas articulações da mão
function desenhaPontos(landmarks) {
  landmarks.forEach(([x, y]) => {
    ctx.beginPath();
    ctx.arc(x, y, 4, 0, 2 * Math.PI);
    ctx.fillStyle = "red";
    ctx.fill();
  });
}

// Envia os landmarks para o backend e retorna a resposta
let ultimaChamada = 0;
async function reconhecerBackend(vetor) {
  const agora = Date.now();
  if (agora - ultimaChamada < 200) return gestureSpan.textContent || "—";
  ultimaChamada = agora;

  try {
    const resp = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ landmarks: vetor })
    });

    if (!resp.ok) throw new Error("Erro no reconhecimento");

    const data = await resp.json();
    return data.gesture || "—";
  } catch (e) {
    console.error("Erro ao reconhecer gesto:", e);
    return "erro";
  }
}

// Botão: abre seletor de vídeo
btnArquivo.addEventListener("click", () => {
  filePicker.click();
});

// Ao selecionar o vídeo, inicia a reprodução
filePicker.addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (!file) return;

  const url = URL.createObjectURL(file);
  video.src = url;
  status.textContent = `Tocando: ${file.name}`;

  video.onloadeddata = () => {
    canvas.width = video.clientWidth;
    canvas.height = video.clientHeight;
  };
});

// Inicia tudo
init();
