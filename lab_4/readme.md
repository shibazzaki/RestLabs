# Lab 4: Library API (Flask + PostgreSQL + Docker + Cursor Pagination)

...

## GET /books

### Параметри

- `limit` (integer, дефолт 10)  
- `cursor` (string, формат `<ISO_created_at>|<last_id>`, дефолт — з початку)

### Відповідь

```json
{
  "items": [
    { "id": "...", "title": "...", "author": "...", "published_year": ..., "created_at": "2025-05-08T12:34:56.789123" },
    …
  ],
  "next_cursor": "2025-05-08T12:34:56.789123|<last_id>"    # або null, якщо більше нема
}

![image](https://github.com/user-attachments/assets/d3a26249-94b5-42cd-bc80-a5f2611e74b8)
