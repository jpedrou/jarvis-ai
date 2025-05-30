import asyncio
import edge_tts
import pygame
import os
import numpy as np
import soundfile as sf
from backend.ws_server import send_signal_to_frontend

async def speak_jarvis(text):
    try:
        voice = "pt-BR-AntonioNeural"
        
        communicate = edge_tts.Communicate(text, voice, rate = "+28%")
        await communicate.save("temp.mp3")

        data, samplerate = sf.read("temp.mp3")
        
        delay = int(0.05 * samplerate)
        echo = np.zeros_like(data)
        echo[delay:] = data[:-delay] * 0.3
        data = data + echo
        
        sf.write("output.mp3", data, samplerate)

        pygame.mixer.init()
        pygame.mixer.music.load('output.mp3')
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.01)
            
        pygame.mixer.quit()
        os.remove('temp.mp3')
        os.remove('output.mp3')
        
    except Exception as e:
        print(f"Erro: {str(e)}")

async def say(text, first_message=False):
    if first_message:
        text = f"Olá, eu sou o Járvis"

    await send_signal_to_frontend(text)
    await speak_jarvis(text)
    
