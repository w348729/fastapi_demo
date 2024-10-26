FROM python:latest as base

# WORKDIR /app

# RUN mkdir -p /app
# COPY ./ /app
# COPY start.sh ./app

ADD . /app
COPY requirements.txt /app
WORKDIR /app

# install python / pip
RUN apt-get update
RUN apt-get install -y python3 python3-pip build-essential

FROM base
#imstall libs
RUN pip install --no-cache-dir -r /app/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN chmod +x /app/*.sh

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]