# Sử dụng image Python 3.11.7 chính thức
FROM python:3.11.7-slim

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
    poetry install && \
    alembic upgrade head

# Lệnh khởi động container
CMD ["/app/venv/bin/python", "main.py", "--env", "prod", "--debug"]


FROM python:3.11-slim

# Thit lập các biên môi trường proxy

ENV HTTP_PROXY=http://10.255.249.100:3128

ENV HTTPS_PROXY=http://10.255.249.100:3128

# Thit lập thư mục làm việc trong container

WORKDIR /app

# Sao chép file requirements.txt vào container

COPY requirements.txt

# Cài đặt các thư viện từ requirements.txt qua proxy

RUN pip install --no-cache-dir -r requirements.txt

ENV HTTP PROXY=

ENV HTTPS_PROXY=

# Sao chép toàn bộ mã nguũn vào container

COPY

# Lệnh chạy ứng dụng (có thì thay đi tuỳ vào ứng dụng của bạn)

CMD ["python", "main.py"]