import sounddevice as sd
import numpy as np
import speech_recognition as sr
from scipy.io.wavfile import write
from pynput import keyboard
from backend.ws_server import send_signal_to_frontend

async def get_voice_response():
    fs = 16000
    filename = "temp_user_audio.wav"
    recording = []
    is_recording = False
    stop_recording = False

    await send_signal_to_frontend("Pressione a barra de espaço para iniciar/parar a gravação.")

    def on_press(key):
        nonlocal is_recording, stop_recording
        if key == keyboard.Key.space:
            if not is_recording:
                is_recording = True
            else:
                stop_recording = True
                return False

    with keyboard.Listener(on_press=on_press) as listener:
        while not is_recording:
            pass

        while not stop_recording:
            await send_signal_to_frontend("Gravando... ")
            block = sd.rec(1024, samplerate=fs, channels=1, dtype="int16")
            sd.wait()
            recording.append(block)

        listener.join()
    
    await send_signal_to_frontend("Gravação concluída.")

    if not recording:
        print("Nenhuma gravação foi feita.")
        return None

    recording = np.concatenate(recording, axis=0)
    write(filename, fs, recording)

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(filename) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language="pt-BR")
            print(f"Resposta reconhecida: {text}")
            return text if text else None
    except Exception as e:
        print(f"Ocorreu um erro na transcrição: {e}")
        return None
