import subprocess
import sys
import os
import asyncio
from backend.message import say
from backend.face_recognizer import capture_face
from backend.get_user_voice import get_voice_response

async def start_app():
    # Abre o navegador
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = f"file://{current_dir}/frontend/index.html"

    browser_process = subprocess.Popen(["google-chrome", file_path])
    
    await say("", first_message=True)
    await say("Antes de iniciarmos, preciso saber com quem estou falando")
    await say("Para te identificar, por favor, preciso que olha para a câmera")
    await say("Podemos prosseguir?")

    response = await get_voice_response()
    if response and any(word in response.lower() for word in ["sim", "claro", "ok", "vamos", "pode"]):
        await say("Ótimo! Vamos lá!")
        await say("Tente centralizar seu rosto na tela")
        face = await capture_face()
    
    else:
        await say("Que pena! Não poderei te ajudar. Somente pessoas autorizadas podem acessar meu conhecimento.")
        await say("Desligando sistema!")
        await asyncio.sleep(2)
        subprocess.run(['pkill', '-f', f'google-chrome.*{file_path}'], shell=True)
        sys.exit(0)
 

if __name__ == "__main__":
    asyncio.run(start_app())