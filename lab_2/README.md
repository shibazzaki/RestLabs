# Lab 2: Library API with FastAPI

## Опис
Проста асинхронна REST API для сутності **Book** (ID, title, author, published_year)  
– зберігає в пам’яті (`List[Book]`), валідує через Pydantic,  
– 4 ендпоінти:  
1. `GET  /books`  
2. `GET  /books/{id}`  
3. `POST /books`  
4. `DELETE /books/{id}`  

## Встановлення

```bash
cd lab_2
pip install .
