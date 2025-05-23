FROM python:3.11-slim

# Thit lập các biên môi trường proxy

ENV HTTP_PROXY= 

ENV HTTPS_PROXY=

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