# —————————————————————————————
# IMPORTAÇÃO DE BIBLIOTECAS NECESSÁRIAS
# —————————————————————————————
import os
import cv2

# —————————————————————————————
# DEFINIÇÃO DO DIRETÓRIO DE DADOS
# —————————————————————————————
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# —————————————————————————————
# DEFINIÇÃO DE PARÂMETROS DO DATASET
# —————————————————————————————
number_of_classes = 5  # Número de classes (ex: 5 gestos)
dataset_size = 100

# —————————————————————————————
# INICIALIZAÇÃO DA CAPTURA DE VÍDEO
# —————————————————————————————
cap = cv2.VideoCapture(0)

# —————————————————————————————
# COLETA DE IMAGENS PARA CADA CLASSE
# —————————————————————————————
for j in range(number_of_classes):
    # Cria o diretório da classe, se não existir
    if not os.path.exists(os.path.join(DATA_DIR, str(j))):
        os.makedirs(os.path.join(DATA_DIR, str(j)))

    print('Collecting data for class {}'.format(j))

    # —————————————————————————————
    # AGUARDA O USUÁRIO PRESSIONAR 'Q' PARA INICIAR
    # —————————————————————————————
    while True:
        ret, frame = cap.read()
        cv2.putText(frame, 'Ready? Press "Q" ! :)', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
        cv2.imshow('frame', frame)
        if cv2.waitKey(25) == ord('q'):
            break

    # —————————————————————————————
    # CAPTURA E SALVA AS IMAGENS DA CLASSE
    # —————————————————————————————
    counter = 0
    while counter < dataset_size:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        cv2.waitKey(25)
        cv2.imwrite(os.path.join(DATA_DIR, str(j), '{}.jpg'.format(counter)), frame)
        counter += 1

# —————————————————————————————
# FINALIZAÇÃO DA CAPTURA E FECHAMENTO DAS JANELAS
# —————————————————————————————
cap.release()
cv2.destroyAllWindows()
