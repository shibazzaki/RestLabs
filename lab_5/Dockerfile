FROM python:3.11-slim

WORKDIR /app

# Встановлюємо залежності
COPY requirements.txt setup.py ./
RUN pip install --no-cache-dir .

# Копіюємо код
COPY . .

# Точка входу
CMD ["run-library-api"]
