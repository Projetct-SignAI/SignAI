// landmark.js — usa os globals tf, handpose e tfjsConverter

window.addEventListener("DOMContentLoaded", async () => {
  const video        = document.getElementById("video");
  const canvas       = document.getElementById("canvas");
  const ctx          = canvas.getContext("2d");
  const gestureSpan  = document.getElementById("gestureName");
  const btnWebcam    = document.getElementById("btnWebcam");
  //const btnArquivo   = document.getElementById("btnArquivo");
  const filePicker   = document.getElementById("filePicker");
  const statusLabel  = document.getElementById("status");

  // 1) Inicializa TensorFlow.js + WebGL
  await tf.setBackend("webgl");
  statusLabel.textContent = "Carregando modelo…";

  // 2) Carrega o modelo handpose (global handpose)
  const hpModel = await handpose.load();
  statusLabel.textContent = "Modelo carregado. Escolha webcam ou vídeo.";

  let ultimaChamada = 0;

  // Desenha os pontos
  function drawLandmarks(landmarks) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    landmarks.forEach(([x, y]) => {
      ctx.beginPath();
      ctx.arc(x, y, 4, 0, 2 * Math.PI);
      ctx.fillStyle = "red";
      ctx.fill();
    });
  }

  // Chama o FastAPI
  async function reconhecerBackend(vetor) {
    const agora = Date.now();
    if (agora - ultimaChamada < 200) return gestureSpan.textContent || "—";
    ultimaChamada = agora;
    try {
      const resp = await fetch("/reconhecer/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ landmarks: vetor })
      });
      if (!resp.ok) throw new Error(resp.status);
      const data = await resp.json();
      return data.gesture || "—";
    } catch (e) {
      console.error("Erro no backend:", e);
      return "erro";
    }
  }

  // Loop de inferência
  async function loop() {
    if (video.readyState >= 2) {
      const preds = await hpModel.estimateHands(video);
      if (preds.length > 0) {
        const landmarks = preds[0].landmarks;
        drawLandmarks(landmarks);
        const flat = landmarks.flat();
        gestureSpan.textContent = await reconhecerBackend(flat);
      } else {
        gestureSpan.textContent = "—";
        ctx.clearRect(0, 0, canvas.width, canvas.height);
      }
    }
    requestAnimationFrame(loop);
  }

  // Eventos de UI
  btnWebcam.addEventListener("click", async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      video.srcObject = stream;
      statusLabel.textContent = "Webcam ativa";
    } catch {
      statusLabel.textContent = "Falha ao acessar webcam";
    }
  });

  btnArquivo.addEventListener("click", () => filePicker.click());
  filePicker.addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (!file) return;
    video.srcObject = null;
    video.src = URL.createObjectURL(file);
    statusLabel.textContent = `Tocando: ${file.name}`;
    video.onloadeddata = () => {
      canvas.width  = video.clientWidth;
      canvas.height = video.clientHeight;
    };
  });

  // Inicia o loop
  loop();
});
