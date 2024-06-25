FROM ubuntu:latest
WORKDIR /APP
COPY . /APP
RUN apt update -y
RUN apt install python3-pip -y
RUN pip install telebot gunicorn flask --break-system-packages
ENTRYPOINT ["bash", "run.sh"]
