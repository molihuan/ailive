import asyncio

import logging

import websockets


async def on_message(message):
    print(message)
    # 处理收到的消息
    logging.debug(f"Received message: {message}")

async def on_error(error):
    # 处理错误
    logging.error(f"Error: {error}")

async def on_close():
    # 处理连接关闭
    logging.debug("WebSocket connection closed")

async def on_open():
    # 处理连接建立
    logging.debug("WebSocket connection established")

async def websocket_client():
    uri = "ws://127.0.0.1:8888"
    async with websockets.connect(uri, ping_interval=None) as websocket:
        await on_open()
        try:
            async for message in websocket:
                await on_message(message)
        except websockets.exceptions.ConnectionClosedError:
            await on_close()



if __name__ == "__main__":
    asyncio.run(websocket_client())
