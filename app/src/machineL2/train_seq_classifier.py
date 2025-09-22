# train_seq_classifier.py
"""
Treina um classificador sequencial (LSTM/GRU) usando o data_seq.pickle gerado.
- Usa Keras (TensorFlow). Se não houver TF instalado, instrução de instalação será mostrada.
- Salva modelo em machineL/model_seq.h5
"""

import os
import pickle
import numpy as np

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# ---------- TF import com mensagem amigável ----------
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Masking, LSTM, GRU, Dense, Dropout, Bidirectional
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
except Exception as e:
    raise ImportError(
        "Falha ao importar TensorFlow. Instale com: pip install tensorflow\n"
        f"Erro original: {e}"
    )
# ----------------------------------------------------

# ---------- CONFIGURAÇÃO ----------
BASE_DIR = os.path.dirname(__file__)
DATA_SEQ_PKL = os.path.join(BASE_DIR, "data_seq.pickle")
MODEL_OUT_PATH = os.path.join(BASE_DIR, "model_seq.h5")

SEQUENCE_LENGTH = 30    # deve bater com create_seq_dataset.py
FEATURES_PER_FRAME = 42 # 21 pontos * 2 (x,y) - consistente com create_seq_dataset.py

TEST_SIZE = 0.2
RANDOM_STATE = 42
BATCH_SIZE = 32
EPOCHS = 40
LEARNING_RATE = 1e-3
# -----------------------------------

def load_data(pickle_path=DATA_SEQ_PKL):
    if not os.path.exists(pickle_path):
        raise FileNotFoundError(f"{pickle_path} não encontrado. Rode create_seq_dataset.py primeiro.")
    with open(pickle_path, "rb") as f:
        d = pickle.load(f)
    data = np.asarray(d["data"])  # shape (n_samples, seq_len, features)
    labels = np.asarray(d["labels"])
    return data, labels

def build_model(seq_len=SEQUENCE_LENGTH, feat=FEATURES_PER_FRAME, n_classes=2):
    """
    Modelo simples: Bidirectional LSTM -> Dense
    Pode trocar por GRU, empilhar camadas, ou usar Transformers depois.
    """
    model = Sequential()
    model.add(Masking(mask_value=0.0, input_shape=(seq_len, feat)))
    model.add(Bidirectional(LSTM(128, return_sequences=False)))
    model.add(Dropout(0.4))
    model.add(Dense(64, activation="relu"))
    model.add(Dropout(0.3))
    model.add(Dense(n_classes, activation="softmax"))

    opt = tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE)
    model.compile(optimizer=opt, loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model

def main():
    X, y = load_data()
    print("Dados carregados:", X.shape, y.shape)

    # codifica labels (strings -> inteiros)
    le = LabelEncoder()
    y_enc = le.fit_transform(y)
    n_classes = len(le.classes_)
    print(f"Número de classes: {n_classes} -> {list(le.classes_)}")

    # split
    x_train, x_test, y_train, y_test = train_test_split(X, y_enc, test_size=TEST_SIZE,
                                                        random_state=RANDOM_STATE, stratify=y_enc)
    print("Split feito. Treinando...")

    model = build_model(seq_len=X.shape[1], feat=X.shape[2], n_classes=n_classes)
    model.summary()

    # Callbacks
    chkpt = ModelCheckpoint(MODEL_OUT_PATH, monitor="val_accuracy", save_best_only=True, verbose=1)
    early = EarlyStopping(monitor="val_loss", patience=8, restore_best_weights=True, verbose=1)

    history = model.fit(x_train, y_train,
                        validation_split=0.1,
                        epochs=EPOCHS,
                        batch_size=BATCH_SIZE,
                        callbacks=[chkpt, early],
                        verbose=2)

    # avaliação
    y_pred_prob = model.predict(x_test)
    y_pred = np.argmax(y_pred_prob, axis=1)
    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy no teste: {acc*100:.2f}%")
    print("Classification report:")
    print(classification_report(y_test, y_pred, target_names=le.classes_))

    # salva o encoder de labels junto do modelo (útil na inferência)
    le_path = os.path.join(BASE_DIR, "label_encoder.pickle")
    with open(le_path, "wb") as f:
        pickle.dump(le, f)
    print(f"LabelEncoder salvo em: {le_path}")
    print(f"Modelo final salvo em: {MODEL_OUT_PATH}")

if __name__ == "__main__":
    main()
