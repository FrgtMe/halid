FROM ubuntu:latest

# Gerekli paketleri kurmak için kullanılır
RUN apt install python3-pip
RUN pip install jupyter

# Çalışma dizini oluşturulur
WORKDIR /app

# Docker içinde Jupyter Not defterini başlatmak için kullanılır
CMD jupyter notebook --ip 0.0.0.0 --port 8080 --allow-root --no-browser
