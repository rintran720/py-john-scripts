import ssl
import aiohttp
from aiohttp import ClientSession, ClientConnectorError, ClientWebSocketResponse
from Logger import Logger

logger = Logger(prefix='AsyncWebsocketClient')

class WebsocketClient:
    """
    Một client WebSocket async dùng aiohttp:
    - Hỗ trợ proxy (HTTP proxy)
    - Hỗ trợ SSL
    - Tự động reconnect khi gửi/nhận bị lỗi (mức cơ bản)
    """

    def __init__(self, url, proxy=None, ssl_verify=False):
        """
        :param url: URL websocket (ví dụ wss://echo.websocket.org)
        :param proxy: URL proxy (nếu cần), ví dụ: "http://my-proxy:8080"
        :param ssl_verify: bool, True => xác thực SSL, False => bỏ qua
        """
        self.url = url
        self.proxy = proxy
        self.ssl_verify = ssl_verify

        # Session và websocket
        self.session: ClientSession = None
        self.ws: ClientWebSocketResponse = None

    async def connect(self):
        """
        Tạo session và kết nối WebSocket.
        Nếu đã kết nối thì đóng trước rồi kết nối lại.
        """
        await self.disconnect()  # đảm bảo session cũ (nếu có) được đóng

        # Tạo SSLContext nếu cần
        ssl_context = None
        if not self.ssl_verify:
            # Bỏ qua xác thực SSL (chỉ nên dùng test)
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

        # Tạo session
        self.session = aiohttp.ClientSession()

        try:
            self.ws = await self.session.ws_connect(
                self.url,
                proxy=self.proxy,         # ví dụ: "http://proxyhost:8080"
                ssl=ssl_context           # None => mặc định, custom => theo ssl_verify
            )
            logger.info(f"Đã kết nối WebSocket với proxy={self.proxy}")
        except ClientConnectorError as e:
            logger.error(f"Không thể kết nối WebSocket với proxy={self.proxy}: {e}")
            # Tuỳ bạn muốn raise, hoặc chờ retry...
            raise

    async def disconnect(self):
        """
        Đóng websocket và session (nếu tồn tại).
        """
        if self.ws is not None:
            await self.ws.close()
            self.ws = None
            logger.info("Đã đóng WebSocket.")

        if self.session is not None:
            await self.session.close()
            self.session = None
            logger.info("Đã đóng session.")

    async def send_message(self, message: str):
        """
        Gửi message (string) lên WebSocket server.
        Nếu chưa có kết nối -> connect.
        Nếu lỗi => reconnect và gửi lại 1 lần.
        """
        if self.ws is None or self.ws.closed:
            await self.connect()

        try:
            await self.ws.send_str(message)
            logger.info(f"[SEND] {message}")
        except Exception as e:
            # Thử reconnect
            logger.warning(f"Lỗi khi gửi: {e}. Thử reconnect...")
            await self.connect()
            await self.ws.send_str(message)
            logger.info(f"[SEND] (sau reconnect) {message}")

    async def receive_message(self):
        """
        Chờ (blocking async) nhận 1 message từ WebSocket.
        Nếu lỗi => reconnect rồi thử nhận lại 1 lần.
        Trả về:
          - str: nếu server gửi text
          - None: nếu không nhận được (có thể do lỗi)
        """
        if self.ws is None or self.ws.closed:
            await self.connect()

        try:
            msg = await self.ws.receive()
            if msg.type == aiohttp.WSMsgType.TEXT:
                logger.info(f"[RECV] {msg.data}")
                return msg.data
            elif msg.type == aiohttp.WSMsgType.CLOSE:
                logger.warning("Server đóng kết nối, thử reconnect...")
                await self.connect()
                return None
            elif msg.type == aiohttp.WSMsgType.ERROR:
                logger.warning(f"Lỗi WSMsgType.ERROR, thử reconnect...")
                await self.connect()
                return None
            else:
                logger.warning(f"Nhận message loại: {msg.type}, nội dung: {msg.data}")
                return None
        except Exception as e:
            logger.warning(f"Lỗi khi nhận message: {e}. Thử reconnect...")
            await self.connect()
            return None
