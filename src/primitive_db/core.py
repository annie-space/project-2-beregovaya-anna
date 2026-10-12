"""Основная логика работы с таблицами."""

from primitive_db.constants import ID_COLUMN, VALID_TYPES
from primitive_db.decorators import confirm_action, handle_db_errors, log_time

# ---------- Управление таблицами ----------


@handle_db_errors
def create_table(metadata, table_name, columns):
    """Создаёт таблицу с заданными столбцами."""
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    parsed_columns = [ID_COLUMN]
    for col in columns:
        if ":" not in col:
            print(f"Некорректное значение: {col}. Попробуйте снова.")
            return metadata
        name, col_type = col.split(":", 1)
        if col_type not in VALID_TYPES:
            print(
                f"Некорректный тип: {col_type}. "
                f"Допустимы: {', '.join(VALID_TYPES)}."
            )
            return metadata
        parsed_columns.append(f"{name}:{col_type}")

    metadata[table_name] = parsed_columns
    print(
        f'Таблица "{table_name}" успешно создана со столбцами: '
        f'{", ".join(parsed_columns)}'
    )
    return metadata


@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
    """Удаляет таблицу из метаданных."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata


def list_tables(metadata):
    """Печатает список всех таблиц."""
    if not metadata:
        print("Список таблиц пуст.")
        return
    for name in metadata:
        print(f"- {name}")


# ---------- Вспомогательные ----------


def _column_types(metadata, table_name):
    """Возвращает словарь {имя: тип} для таблицы."""
    schema = metadata[table_name]
    result = {}
    for item in schema:
        name, col_type = item.split(":", 1)
        result[name] = col_type
    return result


def _cast(value, col_type):
    """Приводит строку к нужному типу."""
    if col_type == "int":
        return int(value)
    if col_type == "bool":
        return str(value).lower() in ("true", "1", "yes")
    return str(value)


# ---------- CRUD ----------


@handle_db_errors
@log_time
def insert(metadata, data, table_name, values):
    """Добавляет запись в таблицу."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return data

    column_types = _column_types(metadata, table_name)
    fields = [c for c in column_types if c != "ID"]

    if len(values) != len(fields):
        print(
            f"Ошибка: ожидалось {len(fields)} значений, "
            f"получено {len(values)}."
        )
        return data

    record = {"ID": (max((r["ID"] for r in data), default=0) + 1)}
    for field, value in zip(fields, values):
        record[field] = _cast(value, column_types[field])

    data.append(record)
    print(f'Запись с ID={record["ID"]} успешно добавлена в таблицу "{table_name}".')
    return data


@handle_db_errors
@log_time
def select(data, where=None):
    """Возвращает список записей, подходящих под условие where."""
    if where is None:
        return list(data)
    column, value = where
    return [row for row in data if row.get(column) == value]


@handle_db_errors
@confirm_action("обновление записи")
def update(data, set_clause, where_clause):
    """Обновляет записи, подходящие под where_clause."""
    column, value = where_clause
    set_column, set_value = set_clause
    updated_ids = []
    for row in data:
        if row.get(column) == value:
            row[set_column] = set_value
            updated_ids.append(row["ID"])
    if updated_ids:
        for rid in updated_ids:
            print(f"Запись с ID={rid} в таблице успешно обновлена.")
    else:
        print("Записи, подходящие под условие, не найдены.")
    return data


@handle_db_errors
@confirm_action("удаление записи")
def delete(data, where_clause):
    """Удаляет записи, подходящие под where_clause."""
    column, value = where_clause
    removed_ids = [row["ID"] for row in data if row.get(column) == value]
    remaining = [row for row in data if row.get(column) != value]
    if removed_ids:
        for rid in removed_ids:
            print(f"Запись с ID={rid} успешно удалена.")
    else:
        print("Записи, подходящие под условие, не найдены.")
    return remaining


def info(metadata, table_name, data):
    """Печатает информацию о таблице."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return
    print(f"Таблица: {table_name}")
    print(f"Столбцы: {', '.join(metadata[table_name])}")
    print(f"Количество записей: {len(data)}")