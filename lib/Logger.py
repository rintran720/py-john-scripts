from datetime import datetime

# Cách dùng
    # logger = Logger(prefix="Main")  # Bật in màu

    # logger.info("Đây là thông tin INFO")
    # logger.warning("Đây là cảnh báo WARNING")
    # logger.error("Đây là lỗi ERROR")
    # logger.debug("Đây là thông tin DEBUG")
    # logger.debug(f"GET /posts?id=1 =>  {get_response}")

try:
    from colorama import Fore, Style, init
    # Khởi tạo colorama (để trên Windows cũng in màu được)
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    # Nếu không cài colorama, ta vẫn dùng ANSI code hoặc in thường
    COLORAMA_AVAILABLE = False

class Logger:
    """
    Logger in màu kèm thời gian, có thể tuỳ chỉnh mức độ log
    """

    def __init__(self, use_color=True, date_format="%Y-%m-%d %H:%M:%S", prefix="DEFAULT"):
        """
        :param use_color: Có in màu hay không
        :param date_format: Định dạng thời gian cho log
        """
        self.use_color = use_color and COLORAMA_AVAILABLE
        self.date_format = date_format
        self.prefix = prefix

    def _log(self, level, message, color):
        timestamp = datetime.now().strftime(self.date_format)
        if self.use_color:
            print(f"{color}[{timestamp}] [{self.prefix}] [{level}] {message}{Style.RESET_ALL}")
        else:
            print(f"[{timestamp}] [{self.prefix}] [{level}] {message}")

    def info(self, message):
        self._log("INFO", message, Fore.GREEN if self.use_color else "")

    def warning(self, message):
        self._log("WARNING", message, Fore.YELLOW if self.use_color else "")

    def error(self, message):
        self._log("ERROR", message, Fore.RED if self.use_color else "")

    def debug(self, message):
        self._log("DEBUG", message, Fore.CYAN if self.use_color else "")
