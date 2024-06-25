FROM python:3.9

WORKDIR /APP

COPY . /APP

RUN apt update -y

RUN apt install curl -y

RUN curl -fsSL code-server.dev/install.sh | bash

RUN export PASSWORD=12345

ENTRYPOINT ["cat", "/root/.config/code-server/config.yaml", "&", "code-server", "--host", "0.0.0.0", "--port", "443", "--auth", "password"]
