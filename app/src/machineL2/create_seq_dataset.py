# create_seq_dataset.py
"""
Cria o dataset sequencial a partir dos vídeos em data_seq_videos/.
- Extrai landmarks por frame (MediaPipe Hands).
- Normaliza cada frame de forma similar ao create_dataset.py (x - min(x), y - min(y)).
- Para cada vídeo: amostra/recorta/pad para SEQUENCE_LENGTH frames.
- Salva em machineL/data_seq.pickle -> {'data': [np.array(seq)], 'labels': [label]}
"""

import os
import pickle
import numpy as np
import cv2
import mediapipe as mp

# ---------- CONFIGURAÇÃO ----------
BASE_DIR = os.path.dirname(__file__)
INPUT_VIDEOS_DIR = os.path.join(BASE_DIR, "data_seq_videos")
OUTPUT_PICKLE = os.path.join(BASE_DIR, "data_seq.pickle")
SEQUENCE_LENGTH = 30   # frames por sequência (ajustar conforme coletado)
MAX_HANDS = 1
MIN_DETECTION_CONFIDENCE = 0.3
# -----------------------------------

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def extract_landmarks_from_frame(frame, hands_processor):
    """
    Retorna vetor de 42 floats (21*2) ou None se mão não detectada.
    Normalização por subtração do mínimo x e y (mesma lógica do create_dataset.py).
    """
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands_processor.process(frame_rgb)
    if not results.multi_hand_landmarks:
        return None

    # usa apenas a primeira mão detectada (compatível com pipeline atual)
    hand_landmarks = results.multi_hand_landmarks[0]
    x_coords = [lm.x for lm in hand_landmarks.landmark]
    y_coords = [lm.y for lm in hand_landmarks.landmark]

    data_aux = []
    min_x = min(x_coords)
    min_y = min(y_coords)

    for lm in hand_landmarks.landmark:
        data_aux.append(lm.x - min_x)
        data_aux.append(lm.y - min_y)

    if len(data_aux) != 42:  # sanity check
        return None
    return np.array(data_aux, dtype=np.float32)

def load_videos_and_extract_sequences(input_dir=INPUT_VIDEOS_DIR, seq_len=SEQUENCE_LENGTH):
    data = []
    labels = []

    hands = mp_hands.Hands(static_image_mode=False,
                           max_num_hands=MAX_HANDS,
                           min_detection_confidence=MIN_DETECTION_CONFIDENCE)

    if not os.path.exists(input_dir):
        print(f"Nenhuma pasta de vídeos encontrada em {input_dir}. Abortando.")
        return data, labels

    # itera pelos subdiretórios (cada subdir é um label)
    for label in sorted(os.listdir(input_dir)):
        label_dir = os.path.join(input_dir, label)
        if not os.path.isdir(label_dir):
            continue

        print(f"Processando label: {label}")
        for fname in sorted(os.listdir(label_dir)):
            if not fname.lower().endswith((".avi", ".mp4", ".mov", ".mkv")):
                continue
            fpath = os.path.join(label_dir, fname)
            cap = cv2.VideoCapture(fpath)
            frames_vectors = []
            frame_idx = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                # opcional: redimensionar para consistência se vídeos foram salvos em resoluções diferentes
                # frame = cv2.resize(frame, (640, 480))
                lm_vec = extract_landmarks_from_frame(frame, hands)
                if lm_vec is not None:
                    frames_vectors.append(lm_vec)
                frame_idx += 1
            cap.release()

            if len(frames_vectors) == 0:
                print(f"  -> Nenhuma mão detectada no vídeo {fname}. Pulando.")
                continue

            # amostragem / recorte / padding para ter exatamente seq_len frames
            seq = np.asarray(frames_vectors)  # shape (n_frames, 42)
            n = seq.shape[0]
            if n >= seq_len:
                # amostra uniformemente seq_len frames
                indices = np.linspace(0, n - 1, seq_len, dtype=int)
                seq_fixed = seq[indices]
            else:
                # se fewer frames: pad repetindo o último frame válido
                pad_count = seq_len - n
                last = seq[-1]
                padding = np.vstack([last for _ in range(pad_count)])
                seq_fixed = np.vstack([seq, padding])

            # seq_fixed shape: (seq_len, 42)
            data.append(seq_fixed)
            labels.append(label)
            print(f"  -> {fname} -> frames_detected: {n} -> seq_saved")

    hands.close()
    return data, labels

def save_dataset(data, labels, out_path=OUTPUT_PICKLE):
    with open(out_path, "wb") as f:
        pickle.dump({"data": data, "labels": labels}, f)
    print(f"Dataset salvo em: {out_path} | samples: {len(data)}")

def main():
    data, labels = load_videos_and_extract_sequences()
    if len(data) == 0:
        print("Nenhuma sequência válida processada. Verifique os vídeos em data_seq_videos/.")
        return
    save_dataset(data, labels)

if __name__ == "__main__":
    main()
