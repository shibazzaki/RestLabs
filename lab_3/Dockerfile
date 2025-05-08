FROM python:3.11-slim

WORKDIR /app

# Спочатку скопіюємо все
COPY . .

# Тепер встановимо наш пакет у середовище
RUN pip install --no-cache-dir .

# Запуск через entry point, визначений у setup.py
CMD ["run-library-api"]
