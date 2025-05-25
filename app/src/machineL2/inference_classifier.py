# src/machineL2/inference_utils.py

import os, pickle
import numpy as np
import cv2
import mediapipe as mp

BASE_DIR = os.path.dirname(__file__)
MODEL = pickle.load(open(os.path.join(BASE_DIR, 'model.p'), 'rb'))["model"]
LABELS_DICT = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'I', 8: 'L',9: 'M', 10: 'N', 11: 'O', 12: 'P', 13: 'Q', 14: 'R', 15: 'S', 16: 'T', 17: 'U', 18: 'V', 19: 'W', 20: 'Y'}  # ajuste conforme seu treino

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)


def predict_from_frame_bgr(frame_bgr):
    H, W, _ = frame_bgr.shape
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if not results.multi_hand_landmarks:
        return "—"

    data_aux, x_, y_ = [], [], []

    for hand_landmarks in results.multi_hand_landmarks:
        for lm in hand_landmarks.landmark:
            x_.append(lm.x)
            y_.append(lm.y)

        for lm in hand_landmarks.landmark:
            data_aux.append(lm.x - min(x_))
            data_aux.append(lm.y - min(y_))

    prediction = MODEL.predict([np.asarray(data_aux)])[0]
    return LABELS_DICT.get(int(prediction), "?")
