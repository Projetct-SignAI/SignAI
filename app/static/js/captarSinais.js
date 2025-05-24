// —————————————————————————————
// INICIALIZAÇÃO DOS ELEMENTOS E VARIÁVEIS
// —————————————————————————————
window.addEventListener("DOMContentLoaded", () => {
    const video   = document.getElementById("video");
    const canvas  = document.createElement("canvas"); 
    const gesture = document.getElementById("gestureName");
    const status  = document.getElementById("status");
    const btnCam  = document.getElementById("btnWebcam");

    let sending = false, stream = null, loopId = null;

    // —————————————————————————————
    // EVENTO DE CLIQUE NO BOTÃO DA WEBCAM
    // —————————————————————————————
    btnCam.onclick = async () => {
        if (stream) { 
            cancelAnimationFrame(loopId);
            stream.getTracks().forEach(t => t.stop());
            stream = null;
            status.textContent = "Webcam desligada";
            return;
        }
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video:true });
            video.srcObject = stream;
            status.textContent = "Webcam ativa";
            loop();
        } catch(err) {
            status.textContent = "Erro na webcam";
        }
    };

    // —————————————————————————————
    // LOOP PRINCIPAL PARA CAPTURA DE FRAMES
    // —————————————————————————————
    async function loop() {
        if (!stream) return;

        if (video.videoWidth === 0 || video.videoHeight === 0) {
            requestAnimationFrame(loop);
            return;
        }

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        canvas.toBlob(blob => {
            if (blob) {
                enviarFrame(blob);
            }
            loopId = requestAnimationFrame(loop); 
        }, "image/jpeg", 0.7);
    }

    // —————————————————————————————
    // ENVIO DO FRAME PARA O BACKEND
    // —————————————————————————————
    let ultima = 0;
    async function enviarFrame(blob){
        const agora = Date.now();
        if (agora - ultima < 250) return; // máx 4 fps p/ backend
        ultima = agora;
        const form = new FormData();
        form.append("file", blob, "frame.jpg");
        try{
            const r = await fetch("/reconhecer/", {method:"POST", body:form});
            const {gesture: g} = await r.json();
            gesture.textContent = g;
        }catch(e){
            gesture.textContent = "erro";
        }
    }
});
