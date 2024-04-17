FROM python:3.7

WORKDIR ERDEM

COPY . .

RUN apt update -y

RUN apt install npm -y

RUN apt install python3-pip -y


CMD ["bash", "run.sh"]
