import warnings
import subprocess
import threading
import numpy as np
import signal
import sys
import re
import os
import asyncio
from backend.message import say
from backend.face_recognizer import capture_face
from backend.get_user_voice import get_voice_response
from backend.ws_server import start_ws_server
from backend.data.data_manager import get_all_representations, insert_client
from dotenv import load_dotenv
from google import genai

warnings.filterwarnings("ignore")
load_dotenv(override=True)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=GOOGLE_API_KEY)


async def start_app(initialize_web_socket = True):
    if initialize_web_socket:
        ws_process = threading.Thread(target=start_ws_server, daemon=True)
        ws_process.start()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = f"file://{current_dir}/frontend/index.html"

    browser_process = subprocess.Popen(
        ["google-chrome", "--new-window", file_path], preexec_fn=os.setsid
    )

    await say("", first_message=True)
    await say("Antes de iniciarmos, preciso saber com quem estou falando")
    await say("Para te identificar, por favor, preciso que olhe para a câmera")

    max_atempts = 3
    attempts = 0
    found = False

    while attempts < max_atempts:
        await say("Podemos prosseguir ?")
        response = await get_voice_response()
        if (
            response
            and any(
                word in response.lower()
                for word in ["sim", "claro", "ok", "vamos", "pode"]
            )
            and "não" not in response.lower()
        ):
            await say("Ótimo. Vamos lá.")
            await say("Tente centralizar seu rosto na tela")
            face = await capture_face()
            if face is not None:
                registers = get_all_representations()
                for name, image_representation in registers:
                    dist = np.linalg.norm(face - image_representation)
                    if dist < 0.6:
                        await say(f"Acesso autorizado. Olá {name}")
                        found = True
                        break
                if found:
                    break
                if not found:
                    await say(
                        "Não encontrei você na minha base de dados. Posso te cadastrar para que você tenha acesso aos meus conhecimentos ?"
                    )
                    response = await get_voice_response()
                    if response and any(
                        word in response.lower()
                        for word in ["sim", "claro", "ok", "vamos", "pode"]
                    ):
                        await say("Ok. poderia me informar seu nome?")
                        name = await get_voice_response()
                        if name:
                            name = name.strip().split()[-1]
                        await say("E sua idade?")
                        age = await get_voice_response()
                        if age:
                            match = re.search(r"d+", age)
                            age = int(match.group()) if match else None
                        insert_client(name, age, face.tobytes())
                        await say(
                            f"Cadastro realizado com sucesso! Agora você pode acessar meus conhecimentos, {name}!"
                        )

                        found = True
                        break

        if response is None:
            await say("Desculpe, não consegui te ouvir. Poderia repetir?")
            attempts += 1

        else:
            await say(
                "Que pena! Não poderei te ajudar. Somente pessoas autorizadas podem acessar meu conhecimento."
            )
            await say("Desligando sistema!")
            await asyncio.sleep(1)
            os.killpg(os.getpgid(browser_process.pid), signal.SIGTERM)
            sys.exit(0)

    if attempts >= max_atempts:
        await say(
            "Desculpe, mas não consegui entender suas respostas após várias tentativas."
        )
        await say("Desligando sistema!")
        await asyncio.sleep(2)
        os.killpg(os.getpgid(browser_process.pid), signal.SIGTERM)
        sys.exit(0)

    if found:
        first_question = True
    while True:
        if first_question:
            await say("O que você gostaria de saber?")
            first_question = False

        response = None
        while response is None:
            response = await get_voice_response()
            if response is None:
                await say("Não entendi. Pode repetir, por favor?")

        if "desligar" in response.lower():
            await say("Desligando sistema!")
            await asyncio.sleep(2)
            os.killpg(os.getpgid(browser_process.pid), signal.SIGTERM)
            sys.exit(0)

        if "reiniciar" in response.lower():
            await say("Reiniciando sistema")
            await asyncio.sleep(2)
            os.killpg(os.getpgid(browser_process.pid), signal.SIGTERM)
            start_app()

        instructions = (
            "Responda como Jarvis, o assistente de inteligência artificial do Homem de Ferro: breve, direto, humano e com um tom natural e amigável, como um assistente pessoal. "
            "Evite usar tópicos ou listas. "
            "Sempre finalize perguntando se há mais alguma dúvida ou se posso ajudar em algo mais."
            f"Considere que, se {name} for um nome feminino, responda no gênero feminino; caso contrário, use o masculino. "
        )

        content = f"{instructions}\nPergunta: {response}"

        model_response = client.models.generate_content(
            model="gemini-2.0-flash", contents=content
        )

        await say(model_response.text)


asyncio.run(start_app())

