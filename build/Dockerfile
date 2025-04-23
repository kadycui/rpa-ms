FROM registry.cn-guangzhou.aliyuncs.com/kadycui/python:3.10-slim

WORKDIR /app

COPY build/requirements.txt .

RUN pip install --no-cache-dir -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r requirements.txt

COPY ../src/ .

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
