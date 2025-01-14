import cloudscraper

# Cách dùng
# proxy = "http://10.10.1.10:3128"
# requester = CloudflareRequester(
#     base_url="https://example-protected-by-cf.com",
#     headers={"Authorization": f"Bearer {token}"},
#     proxies={"http": proxy, "https": proxy},
# )


DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
}

class CloudflareRequester:
    """
    Class để gửi request tới API được Cloudflare bảo vệ.
    Sử dụng cloudscraper để vượt qua challenge và duy trì session.
    """
    def __init__(self, base_url, headers=None, proxies=None):
        """
        :param base_url: string - URL gốc của API (ví dụ: https://example.com)
        :param headers: dict - headers mặc định cho mọi request (nếu có)
        :param proxies: dict - cấu hình proxy (nếu có)
        """
        # Tạo một scraper, tương tự requests.Session nhưng có cơ chế bypass CF
        self.scraper = cloudscraper.create_scraper(browser={'custom': 'chrome'})
        self.base_url = base_url.rstrip('/')
        self.scraper.headers.update(DEFAULT_HEADERS)
        
        # Nếu có headers, thêm vào scraper.headers
        if headers:
            self.scraper.headers.update(headers)
        
        # Nếu có proxies, thêm vào scraper.proxies
        if proxies:
            self.scraper.proxies.update(proxies)

    def get(self, endpoint="", params=None, headers=None, **kwargs):
        """
        Gửi yêu cầu GET tới endpoint (VD: /api/v1/users),
        kèm tham số params, headers...
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.scraper.get(url, params=params, headers=headers, **kwargs)
        response.raise_for_status()
        return response.json()
    
    def post(self, endpoint="", data=None, json=None, headers=None, **kwargs):
        """
        Gửi yêu cầu POST tới endpoint (VD: /api/v1/users),
        kèm dữ liệu data, json, headers...
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.scraper.post(url, data=data, json=json, headers=headers, **kwargs)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint="", data=None, json=None, headers=None, **kwargs):
        """
        Gửi yêu cầu PUT tới endpoint (VD: /api/v1/users),
        kèm dữ liệu data, json, headers...
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.scraper.put(url, data=data, json=json, headers=headers, **kwargs)
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint="", headers=None, **kwargs):
        """
        Gửi yêu cầu DELETE tới endpoint (VD: /api/v1/users),
        kèm headers...
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.scraper.delete(url, headers=headers, **kwargs)
        response.raise_for_status()
        return response.json()