import json
import os

# Cách dùng
    # tokens = FileHandler(TOKEN_FILE).read()
    # proxies = FileHandler(PROXY_FILE).read()

class FileHandler:
    """
    Class hỗ trợ đọc/ghi file định dạng .txt hoặc .json
    - .txt:
      + Đọc: trả về list các dòng (mỗi dòng là 1 string)
      + Ghi (list/dict):
        * list -> ghi mỗi phần tử trên 1 dòng
        * dict -> ghi mỗi cặp key: value trên 1 dòng
    - .json:
      + Đọc: trả về dict hoặc list (tùy nội dung JSON)
      + Ghi (list/dict): sử dụng json.dump
    """
    def __init__(self, file_path):
        """
        Khởi tạo với đường dẫn tới file cần xử lý
        """
        self.file_path = file_path

    def read(self):
        """
        Đọc nội dung file.
        - Nếu là file .txt -> trả về list các dòng (list of strings)
        - Nếu là file .json -> trả về dict hoặc list (tùy nội dung JSON)
        """
        # Kiểm tra file có tồn tại không
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(f"Không tìm thấy file: {self.file_path}")

        _, file_ext = os.path.splitext(self.file_path)
        file_ext = file_ext.lower()

        if file_ext == '.txt':
            return self._read_txt()
        elif file_ext == '.json':
            return self._read_json()
        else:
            raise ValueError("Chỉ hỗ trợ file .txt hoặc .json")

    def write(self, data):
        """
        Ghi dữ liệu vào file.
        - Nếu là file .txt:
          + Nếu data là list -> mỗi phần tử trên 1 dòng
          + Nếu data là dict -> mỗi cặp key-value trên 1 dòng
        - Nếu là file .json -> ghi dữ liệu bằng json.dump
        """
        _, file_ext = os.path.splitext(self.file_path)
        file_ext = file_ext.lower()

        if file_ext == '.txt':
            self._write_txt(data)
        elif file_ext == '.json':
            self._write_json(data)
        else:
            raise ValueError("Chỉ hỗ trợ file .txt hoặc .json")

    def _read_txt(self):
        """
        Đọc file .txt và trả về list các dòng (đã lược bỏ ký tự xuống dòng)
        """
        with open(self.file_path, 'r', encoding='utf-8') as f:
            content_lines = f.read().splitlines()
        return content_lines

    def _read_json(self):
        """
        Đọc file .json và trả về dữ liệu (dict hoặc list)
        """
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    def _write_txt(self, data):
        """
        Ghi dữ liệu vào file txt:
        - list -> mỗi item là một dòng
        - dict -> mỗi cặp key: value là một dòng
        """
        with open(self.file_path, 'w', encoding='utf-8') as f:
            if isinstance(data, list):
                for item in data:
                    f.write(str(item) + '\n')
            elif isinstance(data, dict):
                for key, value in data.items():
                    f.write(f"{key}: {value}\n")
            else:
                raise ValueError("Chỉ hỗ trợ ghi list hoặc dict cho file .txt")

    def _write_json(self, data):
        """
        Ghi dữ liệu vào file .json (list hoặc dict)
        """
        if not isinstance(data, (list, dict)):
            raise ValueError("Chỉ hỗ trợ ghi list hoặc dict cho file .json")

        with open(self.file_path, 'w', encoding='utf-8') as f:
            # ensure_ascii=False để giữ tiếng Việt, indent=4 để format đẹp
            json.dump(data, f, ensure_ascii=False, indent=4)

    def write_to_line(self, line_number, content):
        """
        Ghi (thay thế) nội dung vào dòng line_number (1-based) trong file.
        - line_number: số thứ tự dòng cần ghi (1-based)
        - content: nội dung cần ghi vào dòng
        """
        # Kiểm tra nếu file không tồn tại, tạo file mới
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                pass

        # Đọc tất cả các dòng trong file
        with open(self.file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Nếu số dòng yêu cầu vượt quá số dòng hiện có,
        # chúng ta cần 'bổ sung' dòng trống cho đến khi đạt line_number.
        if line_number > len(lines):
            # Dùng vòng lặp để thêm dòng trống nếu cần
            lines += ["\n"] * (line_number - len(lines) - 1)
            # Sau đó thêm dòng mới
            lines.append(content + "\n")
        else:
            # Thay thế dòng x bằng content
            # line_number - 1 vì list trong Python đánh index từ 0
            lines[line_number - 1] = content + "\n"

        # Ghi đè lại toàn bộ các dòng vào file
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)