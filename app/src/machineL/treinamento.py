import json
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import joblib

# 1. Carrega os dados
with open("oi_landmarks.json", "r", encoding="utf-8") as f:
    data = json.load(f)

X = []  # landmarks (features)
y = []  # labels (ex: 'oi')

for sample in data:
    flat_landmarks = np.array(sample["landmarks"]).flatten()
    X.append(flat_landmarks)
    y.append(sample["label"])

X = np.array(X)
y = np.array(y)

# 2. Treina o modelo KNN
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X, y)

# 3. Salva o modelo treinado
joblib.dump(knn, "modelo_knn_oi.pkl")

print("✅ Modelo KNN treinado e salvo como 'modelo_knn_oi.pkl'")
