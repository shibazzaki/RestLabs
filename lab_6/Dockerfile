# базовий образ з Python 3.11
FROM python:3.11-slim

# створюємо робочу папку
WORKDIR /app

# копіюємо лише ті файли, що потрібні для інсталяції
COPY requirements.txt setup.py ./

# інсталюємо залежності
RUN pip install --no-cache-dir .

# копіюємо решту коду
COPY . .

# відкриваємо порт
EXPOSE 5000

# точка входу — запускає Flask через наш консольний скрипт
CMD ["run-library-api"]
