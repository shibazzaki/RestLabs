````markdown
# Lab 6: Library API з Flask-RESTful і Swagger UI

## Опис
Проста REST-API для управління колекцією книг:
- **Flask-RESTful** для побудови ресурсів  
- **marshmallow** для валідації вхідних даних  
- **flasgger** для автоматичної документації (Swagger UI)  

## Можливості
- Отримання списку всіх книг  
- Додавання нової книги  
- Пошук книги за `id`  
- Видалення книги за `id`  
- Інтерактивна Swagger-документація на `/apidocs/`

---

## Вимоги
- Python ≥ 3.8  
- virtualenv або venv  
- (опціонально) Docker, якщо хочете запустити в контейнері  

---

## Встановлення

1. Клонувати репозиторій і перейти в папку:
   ```bash
   git clone <your-repo-url>
   cd lab_6
````

2. Створити та активувати віртуальне оточення:

   ```bash
   python3 -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate         # Windows
   ```

3. Встановити залежності:

   ```bash
   pip install --upgrade pip
   pip install .
   ```

---

## Запуск сервера

Після встановлення виконайте:

```bash
run-library-api
```

Сервер стартує на `http://0.0.0.0:5000`.
Swagger UI - за адресою: `http://localhost:5000/apidocs/`

---

## Конфігурація

У цьому лабі налаштувань майже нема, все працює «з коробки». Якщо потрібно змінити порт чи debug-режим, редагуйте `app.run()` у `library_api/app.py`.

---

## Ендпоінти

### 1. Отримати всі книги

```
GET /books
```

**Відповідь** `200 OK`

```json
[
  {
    "id": "uuid-1",
    "title": "1984",
    "author": "George Orwell",
    "published_year": 1949
  },
  ...
]
```

### 2. Додати книгу

```
POST /books
Content-Type: application/json

{
  "title": "The Hobbit",
  "author": "J.R.R. Tolkien",
  "published_year": 1937
}
```

**Відповідь** `201 Created`

```json
{
  "id": "new-uuid",
  "title": "The Hobbit",
  "author": "J.R.R. Tolkien",
  "published_year": 1937
}
```

**Помилка валідації** `400 Bad Request`

```json
{
  "published_year": ["Must be between 0 and 2025"]
}
```

### 3. Отримати книгу за ID

```
GET /books/{book_id}
```

* **200 OK**
* **404 Not Found**

```json
{ "message": "Book not found" }
```

### 4. Видалити книгу

```
DELETE /books/{book_id}
```

* **204 No Content**
* **404 Not Found**

```json
{ "message": "Book not found" }
```

---

## Swagger UI

Переходьте на `http://localhost:5000/apidocs/` для інтерактивного перегляду:

* Опис ресурсів та моделей
* Можливість проганяти запити прямо з браузера

---

## Тестування

###  curl

```bash
# Додати книгу
curl -X POST http://localhost:5000/books \
  -H "Content-Type: application/json" \
  -d '{"title":"Dune","author":"Frank Herbert","published_year":1965}'

# Отримати всі
curl http://localhost:5000/books

# Отримати за ID
curl http://localhost:5000/books/<book_id>

# Видалити
curl -X DELETE http://localhost:5000/books/<book_id> -v
```

