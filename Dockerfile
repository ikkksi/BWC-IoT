FROM python:3.10-slim

WORKDIR /usr/BWC-IoT

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

COPY . .

EXPOSE 2048
CMD ["python", "src/main.py"]