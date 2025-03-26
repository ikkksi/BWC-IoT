from typing import Tuple
import websockets


class IWebsocketApp:
    WK: dict
    RK: dict
    ILLEGAL: dict

    def __init__(self, address: str, port: int) -> None: ...

    async def _auth_bridge(self, websocket: websockets.WebSocketServerProtocol, path: str) -> bool: ...

    async def _middleware(self, websocket: websockets.WebSocketServerProtocol, path: str) -> Tuple[bool, websockets.WebSocketServerProtocol, str]: ...

    async def _handler(self, websocket: websockets.WebSocketServerProtocol, path: str) -> None: ...

    async def _broadcast(self, message: str, sender: websockets.WebSocketServerProtocol) -> None: ...

    async def run(self) -> None: ...