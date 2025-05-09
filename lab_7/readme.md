```markdown
# Lab 5: Library API (FastAPI + MongoDB + Docker)

## Опис
Проста асинхронна REST API для сутності **Book** (поля: `id`, `title`, `author`, `published_year`)  
– Зберігання в MongoDB через Motor (AsyncIOMotorClient)  
– Серіалізація ObjectId за допомогою **pydantic-mongo**  
– Підняття сервісів через Docker Compose  

## Структура
```

lab\_5/
├── Dockerfile
├── docker-compose.yml
├── setup.py
├── requirements.txt
├── README.md
└── library\_api/
├── **init**.py
├── main.py
└── schemas.py

````

## Залежності
У файлі `requirements.txt`:
```text
fastapi>=0.85.0
uvicorn[standard]>=0.18.0
motor>=3.1.1
pydantic-mongo>=0.1.0
````

## Запуск

1. Перейдіть у каталог:

   ```bash
   cd lab_5
   ```

2. Побудуйте і запустіть контейнери:

   ```bash
   docker-compose up --build
   ```

   * Сервіс **mongo** на порту `27017`.
   * Сервіс **api** (FastAPI + Uvicorn) на порту `8000`.

3. **ВАЖЛИВО**
   У `docker-compose.yml` ми вказали рядок під’єднання з параметром `authSource=admin`:

   ```yaml
   environment:
     MONGO_URI: mongodb://mongo_admin:password@mongo:27017/library?authSource=admin
   ```

   Це дозволяє драйверу шукати користувача **mongo\_admin** у базі **admin**, а не **library**.

4. Для зупинки і видалення контейнерів:

   ```bash
   docker-compose down
   ```

## CRUD-ендпоінти

### Створити книгу

```bash
curl -X POST http://localhost:8000/books \
     -H "Content-Type: application/json" \
     -d '{"title":"1984","author":"George Orwell","published_year":1949}'
```

**Відповідь** `201 Created`

```json
{
  "id": "650c0a5e9f1e4b3d9a1e7f12",
  "title": "1984",
  "author": "George Orwell",
  "published_year": 1949
}
```

### Отримати всі книги

```bash
curl http://localhost:8000/books
```

**Відповідь** `200 OK`

```json
[
  {
    "id": "650c0a5e9f1e4b3d9a1e7f12",
    "title": "1984",
    "author": "George Orwell",
    "published_year": 1949
  },
]
```

### Отримати книгу за ID

```bash
curl http://localhost:8000/books/650c0a5e9f1e4b3d9a1e7f12
```

* **400 Bad Request** — якщо формат ID некоректний
* **404 Not Found** — якщо книга не знайдена

### Видалити книгу

```bash
curl -X DELETE http://localhost:8000/books/650c0a5e9f1e4b3d9a1e7f12 -v
```

* **204 No Content** — успішне видалення
* **404 Not Found** — якщо книги не існує


