import speech_recognition as sr
from backend.message import say

async def get_voice_response():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Aguardando resposta de voz...")
        audio = recognizer.listen(source)
        print("Reconhecendo...")
        try:
            response = recognizer.recognize_google(audio, language="pt-BR")
            print(f"Resposta reconhecida: {response}")
            return response
        except sr.UnknownValueError:
            await say("Desculpe, não consegui entender o que você disse.")
            return None
        except sr.RequestError as e:
            await say(f"Erro ao se conectar ao serviço de reconhecimento de voz: {e}")
            return None