# Lab 3: Library API (Flask + PostgreSQL + Docker + Cursor Pagination)

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
