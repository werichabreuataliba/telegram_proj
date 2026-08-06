FROM python:3.11-slim

WORKDIR /app

# Instala bibliotecas do sistema operacional necessárias
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --upgrade pip

RUN pip install -r ChatBOT/requirements.txt

CMD ["python", "-m", "ChatBOT.Telegram_BOT"]