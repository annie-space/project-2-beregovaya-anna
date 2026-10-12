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

## Обработка ошибок, подтверждения и кэширование

- Ошибки БД (отсутствие таблицы, неверный тип, отсутствие файла) обрабатываются централизованно через декоратор `handle_db_errors`.
- Опасные операции (`drop_table`, `update`, `delete`) запрашивают подтверждение через `confirm_action`.
- `insert` и `select` логируют время выполнения через `log_time`.
- Результаты одинаковых `select`-запросов кэшируются с помощью замыкания `create_cacher`.

### Пример

```
Введите команду: drop_table users
Вы уверены, что хотите выполнить "удаление таблицы"? [y/n]: y
Таблица "users" успешно удалена.
```
## Демонстрация

Полный сценарий работы:

1. Запуск: `uv run project`
2. Создание таблицы: `create_table users name:str age:int is_active:bool`
3. Вставка: `insert into users values ("Sergei", 28, true)`
4. Выборка: `select from users`
5. Обновление: `update users set age = 29 where name = "Sergei"` (подтверждение `y`)
6. Удаление: `delete from users where ID = 1` (подтверждение `y`)
7. Удаление таблицы: `drop_table users` (подтверждение `y`)