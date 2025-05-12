def traduzir_video(video_bytes):
    # Salva temporariamente
    with open("temp_video.mp4", "wb") as f:
        f.write(video_bytes)

    # Aqui você processa com OpenCV + seu modelo
    from app.src.machineL.processarVideo import processar_video
    texto_final = processar_video("temp_video.mp4")
    return texto_final
