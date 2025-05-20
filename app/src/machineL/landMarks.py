import cv2
import mediapipe as mp
import json

# Inicializa MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# Abre o vídeo
video_path = "treinamento\oi\oi.mp4"
cap = cv2.VideoCapture(video_path)

landmarks_data = []

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Converte para RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(image)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Extrai os 21 pontos (x, y, z)
            pontos = []
            for lm in hand_landmarks.landmark:
                pontos.append([lm.x, lm.y, lm.z])
            landmarks_data.append({
                "label": "oi",
                "landmarks": pontos
            })

cap.release()

# Salva em JSON
with open("oi_landmarks.json", "w") as f:
    json.dump(landmarks_data, f, indent=2)

print("✅ Landmarks extraídos e salvos em 'oi_landmarks.json'")
