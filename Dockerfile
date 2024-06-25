FROM python:3.9

# PyCharm kurulum dosyalarını indir
RUN apt-get update && apt-get install -y \
    wget \
    unzip

RUN wget https://download.jetbrains.com/python/pycharm-community-2023.1.1.tar.gz
RUN tar -xzf pycharm-community-2023.1.1.tar.gz -C /opt/
RUN ln -s /opt/pycharm-community-2023.1.1/bin/pycharm.sh /usr/bin/pycharm

# Çalışma dizinini belirle
WORKDIR /app

# Uygulama kaynak kodlarını kopyala
COPY . .

# PyCharm'ı çalıştır
CMD ["pycharm", "run"]
