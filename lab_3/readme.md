## Lab 3 (postgres + alchemy + docker)

````markdown
# Lab 3: Library API (Flask + PostgreSQL + Docker)

## Огляд
Цей проект реалізує просте REST-API для управління колекцією книг.  
— **Фреймворк**: Flask  
— **ORM**: SQLAlchemy (Flask-SQLAlchemy)  
— **База даних**: PostgreSQL (контейнер Docker)  
— **Пагінація**: Limit-Offset на ендпоінті `GET /books`  
— **Контейнеризація**: `docker-compose` піднімає окремі сервіси для API та БД

---

## Зміст

- [Передумови](#передумови)  
- [Налаштування](#налаштування)  
- [Запуск](#запуск)  
- [API-ендпоінти](#api-ендпоінти)  
- [Limit-Offset пагінація](#limit-offset-пагінація)  
- [Робота з базою даних](#робота-з-базою-даних)  
- [Зупинка та очищення](#зупинка-та-очищення)  
- [FAQ](#faq)  
- [Ліцензія](#ліцензія)  

---

## Передумови

1. Встановлений Docker & Docker Compose  
2. Python 3.8+ (для локальної інсталяції пакета, якщо потрібно)

---

## Налаштування

1. Склонуйте репозиторій та перейдіть у папку:
   ```bash
   git clone <ваш-репо-url>
   cd lab_3
````

2. Перегляньте файл `.env` (за потреби створіть його на основі `.env.example`):

   ```dotenv
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=library
   DATABASE_URL=postgresql://postgres:postgres@db:5432/library
   ```

---

## Запуск

1. Збудуйте та запустіть сервіси:

   ```bash
   docker-compose up --build
   ```

2. Почекати, поки:

   * контейнер `db` ініціалізує PostgreSQL і створить базу
   * контейнер `api` запустить Flask-додаток на порті **5000**

3. Переконайтесь, що API працює:

   ```bash
   curl http://localhost:5000/books
   # має повернути: []
   ```

---

## API-ендпоінти

### 1. `GET /books`

* **Опис**: Повертає список книг із пагінацією
* **Параметри запиту**:

  * `limit` (int, optional, default=10) — максимальна кількість записів
  * `offset` (int, optional, default=0) — зсув від початку
* **Приклад**:

  ```bash
  curl "http://localhost:5000/books?limit=5&offset=10"
  ```
* **Відповідь**: `200 OK`

  ```json
  [
    {
      "id": "uuid-1",
      "title": "1984",
      "author": "George Orwell",
      "published_year": 1949
    },
    …
  ]
  ```

### 2. `GET /books/{id}`

* **Опис**: Повертає одну книгу за вказаним `id`
* **Параметри в URL**: `id` (string, UUID)
* **Приклад**:

  ```bash
  curl http://localhost:5000/books/uuid-1
  ```
* **Відповідь**:

  * `200 OK` з об’єктом книги
  * `404 Not Found` якщо книга відсутня

### 3. `POST /books`

* **Опис**: Додає нову книгу
* **Тіло запиту** (JSON):

  ```json
  {
    "title": "The Hobbit",
    "author": "J.R.R. Tolkien",
    "published_year": 1937
  }
  ```
* **Приклад**:

  ```bash
  curl -X POST http://localhost:5000/books \
       -H "Content-Type: application/json" \
       -d '{"title":"The Hobbit","author":"J.R.R. Tolkien","published_year":1937}'
  ```
* **Відповідь**:

  * `201 Created` з новоствореним об’єктом (включно з полем `id`)
  * `400 Bad Request` з деталями помилок валідації

### 4. `DELETE /books/{id}`

* **Опис**: Видаляє книгу за `id`
* **Приклад**:

  ```bash
  curl -X DELETE http://localhost:5000/books/uuid-1
  ```
* **Відповідь**:

  * `204 No Content` — успішно видалено
  * `404 Not Found` — якщо книга не знайдена

---

## Limit-Offset пагінація

Параметри:

| Параметр | Тип | Значення за замовчуванням | Опис                         |
| -------- | --- | ------------------------- | ---------------------------- |
| `limit`  | int | `10`                      | Максимум записів у відповіді |
| `offset` | int | `0`                       | Зсув від початку переліку    |

Зміна цих значень дозволяє завантажувати довгі переліки частинами.

---

## Робота з базою даних

1. Підключитися до контейнера БД:

   ```bash
   docker-compose exec db psql -U postgres -d library
   ```
2. Переглянути таблиці:

   ```
   \dt
   ```
3. Переглянути структуру таблиці `books`:

   ```
   \d books
   ```

---

## Зупинка та очищення

Щоб завершити роботу і видалити контейнери (але зберегти дані в Docker-volumes):

```bash
docker-compose down
```

Щоб також видалити volume з даними:

```bash
docker-compose down -v
```

---

## FAQ

**Q:** Як змінити порт API?
**A:** В `docker-compose.yml` змініть рядок `ports: - "5000:5000"` на інший, наприклад `"8080:5000"`.

**Q:** Де зберігається база між перезапусками?
**A:** У volume `db_data` (налаштований у `docker-compose.yml`).
