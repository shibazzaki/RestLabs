# lab_5/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Спочатку копіюємо ВСІ файли проєкту
COPY . /app

# Встановлюємо залежності і сам пакет
RUN pip install --no-cache-dir .

# Запускаємо команду з entry_point
CMD ["run-library-api"]
