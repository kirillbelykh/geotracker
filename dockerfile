FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip wheel "poetry==2.1.3"
RUN poetry config virtualenvs.create false --local

COPY wait-for-it.sh ./wait-for-it.sh
COPY pyproject.toml poetry.lock ./


RUN poetry install 
RUN chmod +x wait-for-it.sh


COPY . .

CMD ["./wait-for-it.sh", "db:5432", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]