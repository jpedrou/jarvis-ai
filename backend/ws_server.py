import uvicorn
import asyncio
from fastapi import FastAPI, WebSocket

def start_ws_server():
        uvicorn.run(
        "backend.ws_server:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )

app = FastAPI()
connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        connections.remove(websocket)

async def send_signal_to_frontend(message):

    while not connections:
         print("Aguardando conexões...")
         await asyncio.sleep(0.25)
    for ws in connections:
        try:
            await ws.send_text(str(message))
        except Exception as e:
             print(f"Erro ao enviar mensagem para o Websocket: {e}")
             connections.remove(ws)