import requests
import urllib3

# Cách dùng
# proxy= "http://10.10.1.10:3128"
# api = Requester("https://jsonplaceholder.typicode.com", headers={"Authorization": f"Bearer {token}"}, proxies= {"http": proxy, "https": proxy})


# # Ví dụ gọi GET /posts?id=1
# # => https://jsonplaceholder.typicode.com/posts?id=1
# get_response = api.get("posts", params={"id": 1})


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DEFAULT_HEADERS = {
      "Content-Type": "application/json",
}

class Requester:
    """
    Lớp Requester giúp gọi request đến các endpoint của API,
    với base_url cố định.
    """
    def __init__(self, base_url, headers=None, proxies=None):
        """
        Khởi tạo Requester với một base_url (ví dụ: https://api.example.com),
        tùy chọn default_headers (dict) để dùng cho mọi request,
        và tùy chọn proxies (dict) để cấu hình proxy.
        """
        self.base_url = base_url.rstrip('/')  # Loại bỏ dấu / ở cuối, nếu có
        self.session = requests.Session()
        self.session.headers.update(headers or DEFAULT_HEADERS)
        if proxies:
            self.session.proxies.update(proxies)

    def get(self, endpoint, params=None):
        """
        Gửi một request GET đến endpoint với các tham số params.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.get(url, params=params, verify=False)
        response.raise_for_status()
        return response.json()
    
    def post(self, endpoint, data=None, json=None):
        """
        Gửi một request POST đến endpoint.
        - `data`: thường dùng để gửi form-encoded (chuỗi, dict), gửi qua body.
        - `json`: gửi dữ liệu dạng JSON (dict), gửi qua body.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.post(url, data=data, json=json, verify=False)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint, data=None, json=None):
        """
        Gửi một request PUT đến endpoint.
        - `data`: thường dùng để gửi form-encoded (chuỗi, dict), gửi qua body.
        - `json`: gửi dữ liệu dạng JSON (dict), gửi qua body.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.put(url, data=data, json=json, verify=False)
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint, params=None):
        """
        Gửi một request DELETE đến endpoint với các tham số params (nếu cần).
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.delete(url, params=params, verify=False)
        response.raise_for_status()
        # Nhiều API khi xóa thành công có thể trả về status code 204 (No Content)
        # hoặc một json xác nhận đã xóa. Nếu trả về 204, response.json() sẽ lỗi.
        # Tùy vào API mà ta trả về response hay response.json() phù hợp.
        # Ở đây, ta tạm trả về response.status_code.
        return response.status_code