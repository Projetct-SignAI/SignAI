# src/machineL/sinalModel.py

import cv2
import numpy as np
import mediapipe as mp
import tempfile

# Carregue seu modelo treinado (ex: um modelo .pkl salvo com joblib)
# from joblib import load
# model = load("modelo_sinais.pkl")

mp_hands = mp.solutions.hands

def traduzir_video(video_bytes: bytes) -> str:
    # 1. Salvar temporariamente o vídeo
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(video_bytes)
        temp_video_path = temp_video.name

    # 2. Abrir vídeo com OpenCV
    cap = cv2.VideoCapture(temp_video_path)

    hands = mp_hands.Hands(static_image_mode=False,
                           max_num_hands=1,
                           min_detection_confidence=0.5)

    gestos_detectados = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Extrair os 21 pontos (x, y, z)
                pontos = []
                for lm in hand_landmarks.landmark:
                    pontos.extend([lm.x, lm.y, lm.z])
                
                pontos_np = np.array(pontos).reshape(1, -1)

                # 3. Aqui seria a inferência com o modelo:
                # pred = model.predict(pontos_np)
                # gestos_detectados.append(pred[0])

                # Como exemplo, vamos simular:
                gestos_detectados.append("sinal_ficticio")

    cap.release()

    # 4. Retornar a sequência de sinais detectados (únicos, mais comuns, etc)
    if not gestos_detectados:
        return "Nenhum gesto detectado"
    
    # Retorna os sinais únicos detectados (ou o mais frequente, ou todos em ordem)
    sinais_final = ", ".join(set(gestos_detectados))
    return sinais_final
