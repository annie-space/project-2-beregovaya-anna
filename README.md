\# Primitive DB



Консольная база данных на Python



\## Установка



```bash

uv sync

```



\## Запуск



```bash

uv run project

```



\## Управление таблицами



\- `create\_table <имя> <столбец1:тип> <столбец2:тип> ...` — создать таблицу

\- `list\_tables` — показать список всех таблиц

\- `drop\_table <имя>` — удалить таблицу

\- `help` — справка

\- `exit` — выход



Поддерживаемые типы: `int`, `str`, `bool`.



\### Пример



```

Введите команду: create\_table users name:str age:int is\_active:bool

Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int, is\_active:bool



Введите команду: list\_tables

\- users



Введите команду: drop\_table users

Таблица "users" успешно удалена.

```

