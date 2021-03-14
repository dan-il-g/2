FROM python:3.8

WORKDIR /opt/app

COPY requirements.txt .
RUN pip3 install \
   --upgrade pip -r requirements.txt

COPY . .
RUN find . -name __pycache__ -type d -exec rm -rv {} +

ENV TZ=Asia/Yekaterinburg
