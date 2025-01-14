import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-john-scripts",  # Tên package bạn muốn xuất bản lên PyPI
    version="0.0.1",    # Phiên bản đầu tiên, ví dụ 0.0.1
    author="John Tran",
    author_email="rintran720@gmail.com",
    description="This is a demo library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rintran720/py-john-scripts",  # Link GitHub project (nếu có)
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",   # Chọn license phù hợp
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',                       # Yêu cầu version Python tối thiểu
    install_requires=[
        # Nếu có phụ thuộc (VD requests, numpy,...), thêm vào đây
        # "requests>=2.0.0",
    ],
)
