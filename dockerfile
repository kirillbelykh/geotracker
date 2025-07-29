FROM python:3.12-slim

WORKDIR /app

# Копируем зависимости
COPY requirements.txt .
COPY wait-for-it.sh ./wait-for-it.sh

# Устанавливаем зависимости и делаем скрипт исполняемым
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x wait-for-it.sh

# Копируем остальной код
COPY . .

# Запускаем после ожидания БД
CMD ["./wait-for-it.sh", "db:5432", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]