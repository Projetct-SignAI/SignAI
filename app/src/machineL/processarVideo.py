def processarVideo(caminho_video):
    import cv2
    import mediapipe as mp

    mp_hands = mp.solutions.hands
    cap = cv2.VideoCapture(caminho_video)
    traducao = ""

    with mp_hands.Hands() as hands:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            # Processar frame
            # Prever gesto com seu modelo
            # Agregar resultados em texto

    cap.release()
    return traducao
