```markdown
# Lab 6: Library API з Flask-RESTful і Swagger UI (Docker)

## Опис
Ця лабораторна реалізовує простий CRUD-API для колекції книг:
- **Flask-RESTful** для побудови ресурсів  
- **marshmallow** для валідації даних  
- **flasgger** для автоматичної генерації Swagger UI  

Усі сервіси запускаються в Docker-контейнері через Docker Compose.

---

## Вимоги
- [Docker](https://www.docker.com/)  
- [docker-compose](https://docs.docker.com/compose/)

---

## Структура `lab_6/`

```

lab\_6/
├── Dockerfile
├── docker-compose.yml
├── setup.py
├── requirements.txt
├── README.md
└── library\_api/
├── **init**.py
├── app.py
├── resources.py
└── schemas.py

````

---

## Запуск через Docker Compose

1. Перейдіть у папку `lab_6`:
   ```bash
   cd lab_6
````

2. Побудуйте образ і підніміть контейнер:

   ```bash
   docker-compose up --build
   ```

   * **build** – будує образ з вашим кодом і встановлює залежності
   * **up** – запускає контейнер із Flask API

3. Після успішного старту:

   * API доступне на `http://localhost:5000`
   * Swagger UI доступне на `http://localhost:5000/apidocs/`

> Завдяки монтуванню коду через `volumes` у `docker-compose.yml`, при зміні файлів у локальній папці повторне перезбирання не потрібне — просто збережіть зміни, і Flask у контейнері зберігає їх автоматично (в режимі `development`).

---

## Зупинка та очищення

Щоб зупинити і видалити контейнери:

```bash
docker-compose down
```

---

## Ендпоінти

### GET `/books`

Отримати список всіх книг

```bash
curl http://localhost:5000/books
```

### POST `/books`

Додати нову книгу

```bash
curl -X POST http://localhost:5000/books \
     -H "Content-Type: application/json" \
     -d '{"title":"Dune","author":"Frank Herbert","published_year":1965}'
```

### GET `/books/{id}`

Отримати книгу за ID

```bash
curl http://localhost:5000/books/<book_id>
```

### DELETE `/books/{id}`

Видалити книгу

```bash
curl -X DELETE http://localhost:5000/books/<book_id> -v
```

---

## Взаємодія зі Swagger UI

Відкрийте в браузері `http://localhost:5000/apidocs/` для:

* Інтерактивного перегляду моделей
* Автоматичного формування та виконання запитів

---


