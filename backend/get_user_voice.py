import sounddevice as sd
import numpy as np
import speech_recognition as sr
from scipy.io.wavfile import write


async def get_voice_response():
    fs = 16000
    duration = 20
    silence_threshold = 500
    silence_duration = 2
    initial_tolerance = 5
    filename = "temp_user_audio.wav"

    print("Gravando...")

    recording = []
    silence_counter = 0
    elapsed_time = 0
    for _ in range(int(fs * duration / 1024)):
        block = sd.rec(1024, samplerate=fs, channels=1, dtype="int16")
        sd.wait()
        recording.append(block)

        volume = np.abs(block).mean()
        elapsed_time =+ 1024 / fs

        if elapsed_time <= initial_tolerance:
            continue

        if volume < silence_threshold:
            silence_counter += 1024 / fs
            if silence_counter >= silence_duration:
                print("Silêncio detectado. Interrompendo gravação.")
                break
        else:
            silence_counter = 0

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
