from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

connected_users = []

html_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Простой чат</title>
</head>
<body>
    <h2>WebSocket Чат</h2>
    <div>
        <input type="text" id="username" placeholder="Ваше имя" value="Аноним">
        <button onclick="connectWebSocket()">Подключиться</button>
    </div>
    <div>
        <input type="text" id="messageInput" placeholder="Сообщение" disabled>
        <button onclick="sendMessage()" disabled id="sendBtn">Отправить</button>
    </div>
    <div id="chatMessages" style="border:1px solid #ccc;height:300px;overflow-y:scroll;padding:10px;"></div>

    <script>
        let ws = null;
        let username = "Аноним";

        function connectWebSocket() {
            username = document.getElementById("username").value || "Аноним";

            // Подключаемся к WebSocket
            ws = new WebSocket("ws://" + window.location.host + "/ws");

            ws.onopen = function() {
                addMessage("Подключено к чату как: " + username);
                document.getElementById("messageInput").disabled = false;
                document.getElementById("sendBtn").disabled = false;
            };

            ws.onmessage = function(event) {
                addMessage(event.data);
            };

            ws.onerror = function(error) {
                addMessage("Ошибка подключения");
            };

            ws.onclose = function() {
                addMessage("Отключено от чата");
                document.getElementById("messageInput").disabled = true;
                document.getElementById("sendBtn").disabled = true;
            };
        }

        function sendMessage() {
            const input = document.getElementById("messageInput");
            const message = input.value.trim();

            if (message && ws) {
                // Отправляем имя и сообщение через двоеточие
                ws.send(username + ": " + message);
                input.value = "";
            }
        }

        function addMessage(text) {
            const chatDiv = document.getElementById("chatMessages");
            const messageDiv = document.createElement("div");
            messageDiv.textContent = text;
            chatDiv.appendChild(messageDiv);
            chatDiv.scrollTop = chatDiv.scrollHeight;
        }

        // Отправка сообщения по Enter
        document.getElementById("messageInput").addEventListener("keypress", function(e) {
            if (e.key === "Enter") {
                sendMessage();
            }
        });
    </script>
</body>
</html>
"""


@app.get("/")
async def get_chat_page():
    return HTMLResponse(html_page)

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

