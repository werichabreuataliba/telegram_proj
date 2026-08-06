FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r ChatBOT/requirements.txt

CMD ["python", "-m", "ChatBOT.Telegram_BOT"]