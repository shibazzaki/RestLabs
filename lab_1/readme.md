## Махобей Владислав ІПЗ-32

## 📖 Опис

Пакет `library_api` реалізує простий сервер для роботи з колекцією книг (сутність `Book`). Дані зберігаються в оперативній пам'яті у вигляді списку словників (`List[Dict]`). Для перевірки коректності вхідних даних використовується бібліотека **marshmallow**.

---

## 📁 Структура проекту

```
library_api/
├── setup.py
├── requirements.txt
├── README.md       # цей файл
└── library_api/
    ├── __init__.py
    ├── app.py      # основний код Flask-додатку
    └── schemas.py  # опис marshmallow-схеми для Book
```

---

## ⚙️ Встановлення

1. Клонування репозиторію:

   ```bash
   git clone <URL репозиторію>
   cd library_api
   ```

2. Рекомендовано створити віртуальне оточення:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\\Scripts\\activate    # Windows
   ```

3. Встановлення залежностей:

   ```bash
   pip install .
   ```

---

## 🚀 Запуск сервера

Після встановлення можна запустити API двома способами:

* Через консольний скрипт:

  ```bash
  run-library-api
  ```
* Або без встановлення пакета:

  ```bash
  python -m library_api.app
  ```

Сервер слухає порт **5000** за адресою `http://localhost:5000`.

---

## 🛠 Ендпоінти API

| Метод  | Шлях          | Опис                           |
| ------ | ------------- | ------------------------------ |
| GET    | `/books`      | Отримати список всіх книг      |
| GET    | `/books/{id}` | Отримати одну книгу за її `id` |
| POST   | `/books`      | Додати нову книгу              |
| DELETE | `/books/{id}` | Видалити книгу за її `id`      |

### GET /books

* **Відповідь (200)**: масив об'єктів `Book`.

### GET /books/{id}

* **Параметр**: `id` (UUID рядком)
* **Відповідь (200)**: об'єкт `Book`
* **Помилка (404)**: `{ "message": "Book not found" }`

### POST /books

* **Тіло запиту** (JSON):

  ```json
  {
    "title": "Назва книги",
    "author": "Автор книги",
    "published_year": 2020
  }
  ```
* **Валідація**:

  * `title` та `author`: непорожні рядки.
  * `published_year`: ціле число від 0 до поточного року.
* **Відповідь (201)**: створений об'єкт `Book` з полем `id`.
* **Помилка (400)**: повідомлення валідації від marshmallow.

### DELETE /books/{id}

* **Параметр**: `id` (UUID рядком)
* **Відповідь (204)**: без тіла
* **Помилка (404)**: `{ "message": "Book not found" }`

---

## 📦 Приклади запитів (curl)

* **Отримати всі книги**:

  ```bash
  curl http://localhost:5000/books
  ```

* **Додати книгу**:

  ```bash
  curl -X POST http://localhost:5000/books \
       -H "Content-Type: application/json" \
       -d '{"title":"1984","author":"George Orwell","published_year":1949}'
  ```

* **Отримати книгу за ID**:

  ```bash
  curl http://localhost:5000/books/<ID_книги>
  ```

* **Видалити книгу**:

  ```bash
  curl -X DELETE http://localhost:5000/books/<ID_книги>
  ```

---

