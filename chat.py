from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from pathlib import Path

app = FastAPI()
connected_users = []

HTML_FILE_PATH = Path("templates/chat.html")

@app.get("/")
async def get_chat_page():
    if HTML_FILE_PATH.exists():
        html_content = HTML_FILE_PATH.read_text(encoding="utf-8")
        return HTMLResponse(html_content)
    else:
        return HTMLResponse("<h1>Файл chat.html не найден</h1>")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_users.append(websocket)

    try:
        await websocket.send_text("Добро пожаловать в чат!")

        while True:
            data = await websocket.receive_text()

            for user in connected_users:
                try:
                    await user.send_text(data)
                except:
                    pass

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        if websocket in connected_users:
            connected_users.remove(websocket)