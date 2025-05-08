FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt setup.py ./
RUN pip install --no-cache-dir .

COPY . .

CMD ["run-library-api"]
