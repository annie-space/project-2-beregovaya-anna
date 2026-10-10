# Primitive DB

Консольная база данных на Python.

## Установка

```bash
uv sync
```

## Запуск

```bash
uv run project
```

## Управление таблицами

- `create_table <имя> <столбец1:тип> <столбец2:тип> ...` — создать таблицу
- `list_tables` — показать список всех таблиц
- `drop_table <имя>` — удалить таблицу
- `help` — справка
- `exit` — выход

Поддерживаемые типы: `int`, `str`, `bool`.

### Пример

```
Введите команду: create_table users name:str age:int is_active:bool
Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int, is_active:bool

Введите команду: list_tables
- users

Введите команду: drop_table users
Таблица "users" успешно удалена.
```

## CRUD-операции

- `insert into <имя> values (<знач1>, <знач2>, ...)` — добавить запись
- `select from <имя>` — вывести все записи
- `select from <имя> where <столбец> = <значение>` — фильтр
- `update <имя> set <столбец> = <значение> where <столбец> = <значение>` — обновить
- `delete from <имя> where <столбец> = <значение>` — удалить
- `info <имя>` — информация о таблице

Строковые значения указываются в кавычках: `"Sergei"`.

### Пример

```
Введите команду: insert into users values ("Sergei", 28, true)
Запись с ID=1 успешно добавлена в таблицу "users".

Введите команду: select from users where age = 28
+----+--------+-----+-----------+
| ID |  name  | age | is_active |
+----+--------+-----+-----------+
| 1  | Sergei |  28 |    True   |
+----+--------+-----+-----------+

Введите команду: update users set age = 29 where name = "Sergei"
Запись с ID=1 в таблице успешно обновлена.

Введите команду: delete from users where ID = 1
Запись с ID=1 успешно удалена.
```