FROM registry.cn-shanghai.aliyuncs.com/payun/python:3.7

RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple

COPY ["./requirements.txt", "."]
RUN pip install -r requirements.txt

COPY ["./", "/srv"]
WORKDIR /srv

EXPOSE 8080
ENTRYPOINT ["uvicorn", "index:app", "--host","0.0.0.0", "--port", "8080"]
