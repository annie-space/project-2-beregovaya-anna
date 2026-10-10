"""Основная логика работы с таблицами"""

from primitive_db.constants import ID_COLUMN, VALID_TYPES


def create_table(metadata, table_name, columns):
    """Создаёт таблицу с заданными столбцами

    columns — список строк вида 'name:str', 'age:int'.
    Автоматически добавляет столбец ID:int в начало
    """
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует')
        return metadata

    parsed_columns = [ID_COLUMN]
    for col in columns:
        if ":" not in col:
            print(f"Некорректное значение: {col}. Попробуйте снова")
            return metadata
        name, col_type = col.split(":", 1)
        if col_type not in VALID_TYPES:
            print(f"Некорректный тип: {col_type}. Допустимы: {', '.join(VALID_TYPES)}")
            return metadata
        parsed_columns.append(f"{name}:{col_type}")

    metadata[table_name] = parsed_columns
    print(
        f'Таблица "{table_name}" успешно создана со столбцами: '
        f'{", ".join(parsed_columns)}'
    )
    return metadata


def drop_table(metadata, table_name):
    """Удаляет таблицу из метаданных"""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata


def list_tables(metadata):
    """Печатает список всех таблиц"""
    if not metadata:
        print("Список таблиц пуст")
        return
    for name in metadata:
        print(f"- {name}")