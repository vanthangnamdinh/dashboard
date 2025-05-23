# Sử dụng image Python 3.11.7 chính thức
FROM python:3.11.7-slim

# Thiết lập các biến môi trường proxy
ENV HTTP_PROXY= 

ENV HTTPS_PROXY=

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép toàn bộ project hiện tại vào thư mục /app trong image
COPY . /app

# Cài đặt các gói cần thiết để tạo virtual environment và biên dịch poetry
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Tạo virtual environment trong thư mục /app/venv
RUN python -m venv /app/venv

# Kích hoạt venv và cài pip, setuptools, poetry, sau đó cài đặt dependencies và chạy alembic
RUN . /app/venv/bin/activate && \
    pip install --upgrade pip setuptools && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install 

# xóa proxy sau khi cài đặt
ENV HTTP_PROXY= 

ENV HTTPS_PROXY=

# Lệnh khởi động container
#CMD ["/app/venv/bin/python", "main.py", "--env", "prod", "--debug"] #Không chạy app bởi vì cần chạy migrate


