# —————————————————————————————
# IMPORTAÇÃO DE BIBLIOTECAS
# —————————————————————————————
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

# —————————————————————————————
# DEFINIÇÃO DO DIRETÓRIO BASE
# —————————————————————————————
BASE_DIR = os.path.dirname(__file__)

# —————————————————————————————
# CARREGAMENTO DOS DADOS
# —————————————————————————————
data_dict = pickle.load(open(os.path.join(BASE_DIR, 'data.pickle'), 'rb'))

data = np.asarray(data_dict['data'])
labels = np.asarray(data_dict['labels'])

# —————————————————————————————
# DIVISÃO DOS DADOS EM TREINO E TESTE
# —————————————————————————————
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

# —————————————————————————————
# CRIAÇÃO E TREINAMENTO DO MODELO
# —————————————————————————————
model = RandomForestClassifier()

model.fit(x_train, y_train)

# —————————————————————————————
# AVALIAÇÃO DO MODELO
# —————————————————————————————
y_predict = model.predict(x_test)

score = accuracy_score(y_predict, y_test)

print('{}% of samples were classified correctly !'.format(score * 100))

# —————————————————————————————
# SALVAMENTO DO MODELO TREINADO
# —————————————————————————————
with open(os.path.join(BASE_DIR, 'model.p'), 'wb') as f:
    pickle.dump({'model': model}, f)
f.close()
