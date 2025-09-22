# collect_seq.py
"""
Coleta vídeos curtos por gesto.
- Pressione 'Q' para iniciar a gravação (igual ao collect_imgs.py).
- Durante a gravação, 'Q' também permite encerrar antecipadamente.
- Salva em machineL/data_seq_videos/<GESTURE>/
"""

import cv2
import os
import time
import uuid

# ---------- CONFIGURAÇÃO (ajuste conforme necessário) ----------
BASE_DIR = os.path.dirname(__file__)
OUTPUT_DIR = os.path.join(BASE_DIR, "data_seq_videos")
NUM_VIDEOS = 5        # quantos vídeos por gesto por execução
DURATION = 5          # duração de cada vídeo em segundos
FPS = 25              # frames por segundo
RESOLUTION = (640, 480)  # largura x altura
FOURCC = "XVID"       # codec para VideoWriter
# --------------------------------------------------------------

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def record_one_video(cap, filename, duration=DURATION, fps=FPS, resolution=RESOLUTION):
    fourcc = cv2.VideoWriter_fourcc(*FOURCC)
    out = cv2.VideoWriter(filename, fourcc, fps, resolution)
    start_time = time.time()
    while (time.time() - start_time) < duration:
        ret, frame = cap.read()
        if not ret:
            print("Falha ao ler frame da câmera. Interrompendo gravação.")
            break
        frame = cv2.flip(frame, 1)
        out.write(frame)
        cv2.imshow("Coleta de Sequência (gravando) - Pressione 'Q' para parar", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # permite parar antes do tempo
            print("Gravação interrompida antecipadamente pelo usuário.")
            break
    out.release()

def main():
    ensure_dir(OUTPUT_DIR)
    gesture = input("Digite o nome/label do gesto: ").strip()
    if not gesture:
        print("Label vazio. Abortando.")
        return

    gesture_path = os.path.join(OUTPUT_DIR, gesture)
    ensure_dir(gesture_path)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Não foi possível abrir a câmera.")
        return

    print(f"Pronto para gravar vídeos para o gesto: '{gesture}'")
    print("Para cada vídeo: pressione 'Q' para iniciar a gravação (ou sair do programa).")

    for vid_idx in range(NUM_VIDEOS):
        print(f"\nPreparando vídeo {vid_idx+1}/{NUM_VIDEOS}. Fique pronto.")
        # Mostra preview até o usuário apertar 'q' para iniciar
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Erro ao capturar frame da câmera.")
                break
            frame = cv2.flip(frame, 1)
            cv2.putText(frame, f"Ready? Press 'Q' to start ({vid_idx+1}/{NUM_VIDEOS})",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
            cv2.imshow("Coleta de Sequências (preview)", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            if key == 27:  # ESC para sair completamente
                print("Usuário solicitou saída.")
                cap.release()
                cv2.destroyAllWindows()
                return

        # grava
        filename = os.path.join(gesture_path, f"{gesture}_{int(time.time())}_{uuid.uuid4().hex}.avi")
        print("Gravação iniciada...")
        record_one_video(cap, filename, DURATION, FPS, RESOLUTION)
        print(f"Vídeo salvo em: {filename}")

    cap.release()
    cv2.destroyAllWindows()
    print("Coleta finalizada.")

if __name__ == "__main__":
    main()
