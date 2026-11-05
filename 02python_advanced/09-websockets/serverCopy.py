import asyncio
# websocket 可以让客户端和服务端握一次手，之后就是一根一直不会挂断的电话线，谁都能随时说话，这张特性我们叫做全双工
# websocket 是个全双工通信协议，让客户端和服务端建立一次连接之后双方都能随时发消息
# 跟之前的传统http请求不一样，普通的http请求服务器不能主动给客户端推送请求，想实时更新就需要不停的发请求（轮询）会浪费资源
#
import websockets
from websockets.protocol import State
import json
from typing import Set

connected_clients: Set[websockets.ServerConnection] = set()
message_history = []
MAX_HISTORY = 200
print(f"历史消息最大保存条数：{MAX_HISTORY}")


async def safe_send(ws: websockets.ServerConnection, payload: str):
    if ws.state != State.OPEN:
        return
    try:
        await ws.send(payload)
    except Exception as e:
        print(f"发送异常 {ws.remote_address} : {e}")


async def broadcast_online():
    pkg = json.dumps({
        "type": "online_count",
        "count": len(connected_clients)
    }, ensure_ascii=False)
    for cli in connected_clients:
        await safe_send(cli, pkg)


async def handle_client(ws: websockets.ServerConnection):
    print(f"客户端接入: {ws.remote_address}")
    connected_clients.add(ws)
    await broadcast_online()
    try:
        async for raw_msg in ws:
            print(f"收到[{ws.remote_address}]：{raw_msg}")
            try:
                recv_data = json.loads(raw_msg)
            except json.JSONDecodeError:
                recv_data = {"username": "匿名用户", "content": raw_msg}
            if recv_data.get("type") == "req_history":
                history_pkg = json.dumps({
                    "type": "history",
                    "data": message_history
                }, ensure_ascii=False)
                await safe_send(ws, history_pkg)
                continue

            chat_msg = {
                "type": "chat",
                "username": recv_data.get("username", "匿名用户"),
                "content": recv_data.get("content", "")
            }
            message_history.append(chat_msg)
            if len(message_history) > MAX_HISTORY:
                message_history.pop(0)

            send_json = json.dumps(chat_msg, ensure_ascii=False)
            for client in connected_clients:
                await safe_send(client, send_json)

    except websockets.exceptions.ConnectionClosed:
        print(f"客户端断开 {ws.remote_address}")
    finally:
        connected_clients.discard(ws)
        await broadcast_online()


async def main(open_browser: bool = False):
    async with websockets.serve(handle_client, host="0.0.0.0", port=9000):
        print("WebSocket服务启动 ws://127.0.0.1:9000/ws")
        if open_browser:
            from pathlib import Path
            import webbrowser

            page = Path(__file__).with_name("index.html").resolve().as_uri()
            if not webbrowser.open(page):
                print("请手动打开项目目录中的 index.html")
        await asyncio.Future()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="WebSocket 聊天室服务")
    parser.add_argument("--open-browser", action="store_true", help="服务启动后打开聊天页面")
    args = parser.parse_args()
    try:
        asyncio.run(main(open_browser=args.open_browser))
    except KeyboardInterrupt:
        print("服务已停止")