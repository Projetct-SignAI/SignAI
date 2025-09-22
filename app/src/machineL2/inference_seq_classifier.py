# inference_seq_classifier.py
"""
Inferência para gestos dinâmicos (sequências).
- Segue a mesma normalização do create_seq_dataset.py (x - min(x), y - min(y)).
- Carrega model_seq.h5 e label_encoder.pickle (gerados por train_seq_classifier.py).
- Modo de operação:
    1) mostra preview da câmera
    2) pressione 'Q' para iniciar a inferência em tempo real
    3) buffer deslizante de SEQ_LENGTH frames; quando cheio, faz predição
    4) pressione ESC para sair
"""

import os
import pickle
from collections import deque

import cv2
import numpy as np
import mediapipe as mp

# tensorflow import
try:
    from tensorflow.keras.models import load_model
except Exception as e:
    raise ImportError("TensorFlow/Keras não está disponível. Instale 'tensorflow'.\nErro: " + str(e))

# ---------------- CONFIGURAÇÃO ----------------
BASE_DIR = os.path.dirname(__file__)
MODEL_H5_PATH = os.path.join(BASE_DIR, "model_seq.h5")
LABEL_ENCODER_PATH = os.path.join(BASE_DIR, "label_encoder.pickle")

SEQ_LENGTH = 30           # deve bater com create_seq_dataset.py / train_seq_classifier.py
FEATURES_PER_FRAME = 42   # 21 pontos * 2 (x,y) - compatível com create_seq_dataset.py
CONF_THRESHOLD = 0.45     # limiar opcional para confiança mínima (ajuste conforme necessário)
# ------------------------------------------------

def load_trained_model(path_h5):
    if not os.path.exists(path_h5):
        raise FileNotFoundError(f"Modelo não encontrado em: {path_h5}. Rode train_seq_classifier.py primeiro.")
    print(f"Carregando modelo: {path_h5}")
    return load_model(path_h5)

def load_label_encoder(path_pickle):
    if not os.path.exists(path_pickle):
        raise FileNotFoundError(f"Label encoder não encontrado em: {path_pickle}. Rode train_seq_classifier.py primeiro.")
    with open(path_pickle, "rb") as f:
        le = pickle.load(f)
    return le

# ---------------- Mediapipe helper ----------------
mp_hands = mp.solutions.hands

def extract_landmarks_vector(frame, hands_processor):
    """
    Extrai vetor de 42 floats (21*2) do frame conforme create_seq_dataset.py.
    Retorna np.array(42,) ou None se mão não detectada.
    """
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands_processor.process(frame_rgb)
    if not results.multi_hand_landmarks:
        return None

    hand_landmarks = results.multi_hand_landmarks[0]  # primeira mão apenas
    x_coords = [lm.x for lm in hand_landmarks.landmark]
    y_coords = [lm.y for lm in hand_landmarks.landmark]

    min_x = min(x_coords)
    min_y = min(y_coords)

    data_aux = []
    for lm in hand_landmarks.landmark:
        data_aux.append(lm.x - min_x)
        data_aux.append(lm.y - min_y)

    if len(data_aux) != FEATURES_PER_FRAME:
        return None

    return np.asarray(data_aux, dtype=np.float32)

# ---------------- Inferência em tempo real ----------------
def main():
    # checagens inicial
    model = load_trained_model(MODEL_H5_PATH)
    label_encoder = load_label_encoder(LABEL_ENCODER_PATH)

    # mediapipe hands
    hands = mp_hands.Hands(static_image_mode=False,
                           max_num_hands=1,
                           min_detection_confidence=0.4,
                           min_tracking_confidence=0.4)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Não foi possível abrir a câmera.")
        hands.close()
        return

    print("Preview da câmera. Pressione 'Q' para iniciar a inferência, ESC para sair.")
    # Preview até o usuário apertar Q para iniciar
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao capturar frame da câmera.")
            break
        frame = cv2.flip(frame, 1)
        cv2.putText(frame, "Preview - Press 'Q' to start, ESC to exit", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.imshow("Inference - Preview", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("Inferência iniciada.")
            break
        if key == 27:  # ESC
            print("Saindo.")
            cap.release()
            cv2.destroyAllWindows()
            hands.close()
            return

    # buffer deslizante com padding por repetição do último frame válido
    buffer = deque(maxlen=SEQ_LENGTH)
    last_valid = None

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Erro ao capturar frame.")
                break
            frame = cv2.flip(frame, 1)

            lm_vec = extract_landmarks_vector(frame, hands)
            if lm_vec is not None:
                last_valid = lm_vec
                buffer.append(lm_vec)
                status_text = "Hand detected"
            else:
                # sem mão detectada -> repetir último válido (pad) se existir
                if last_valid is not None:
                    buffer.append(last_valid)
                status_text = "No hand"

            # quando buffer cheio, faz predição
            if len(buffer) == SEQ_LENGTH:
                input_arr = np.expand_dims(np.array(buffer, dtype=np.float32), axis=0)  # (1, seq_len, feat)
                preds = model.predict(input_arr, verbose=0)[0]
                pred_idx = int(np.argmax(preds))
                confidence = float(preds[pred_idx])

                # decodifica classe via label encoder
                try:
                    predicted_label = label_encoder.inverse_transform([pred_idx])[0]
                except Exception:
                    # caso str labels were encoded differently, try safe access
                    predicted_label = str(pred_idx)

                if confidence < CONF_THRESHOLD:
                    display_text = f"Unknown ({confidence:.2f})"
                else:
                    display_text = f"{predicted_label} ({confidence:.2f})"

                cv2.putText(frame, display_text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
            else:
                cv2.putText(frame, f"Warm-up {len(buffer)}/{SEQ_LENGTH}", (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 0), 2)

            cv2.putText(frame, status_text, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            cv2.imshow("Dynamic Gesture Inference", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                print("Saindo por ESC.")
                break
            if key == ord('q'):  # permite pausar/iniciar novamente: limpa buffer e retorna ao preview
                print("Pausa solicitada pelo usuário. Voltando ao preview (aperte 'Q' para re-iniciar).")
                buffer.clear()
                last_valid = None
                # preview loop until Q or ESC
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    frame = cv2.flip(frame, 1)
                    cv2.putText(frame, "Preview - Press 'Q' to resume, ESC to exit", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    cv2.imshow("Dynamic Gesture Inference", frame)
                    key2 = cv2.waitKey(1) & 0xFF
                    if key2 == ord('q'):
                        print("Retomando inferência.")
                        break
                    if key2 == 27:
                        print("Saindo por ESC.")
                        cap.release()
                        cv2.destroyAllWindows()
                        hands.close()
                        return

    finally:
        cap.release()
        cv2.destroyAllWindows()
        hands.close()
        print("Inferência finalizada.")

if __name__ == "__main__":
    main()
