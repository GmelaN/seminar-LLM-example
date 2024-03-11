from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from ollama import chat
import asyncio

app = FastAPI()

app.mount("/main", StaticFiles(directory="front-end", html=True), name="front-end")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        # 사용자 입력 데이터
        user_input = await websocket.receive_text()

        data = f"Please summarize the following text in three lines." \
               f"input:\n{user_input}"
        

        # Stream에서 데이터를 읽고 클라이언트에 전송
        async for chunk in async_generator(data):
            await websocket.send_text(chunk)


async def async_generator(data: str):
    stream = chat(
        model='llama2',
        messages=[{'role': 'user', 'content': data}],
        stream=True,
    )

    for chunk in stream:
        yield chunk['message']['content']
