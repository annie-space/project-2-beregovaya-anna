"""Парсеры команд: where, set, values"""



def parse_values(raw):
    """Разбирает строку вида '("Sergei", 28, true)' в список значений

    Значения приводятся к нужному типу по столбцам позже, здесь только строки
    """
    raw = raw.strip()
    if raw.startswith("(") and raw.endswith(")"):
        raw = raw[1:-1]
    tokens = [t.strip() for t in raw.split(",") if t.strip()]
    return tokens


def _cast(value, target_type):
    """Приводит строковое значение к нужному типу"""
    if target_type == "int":
        return int(value)
    if target_type == "bool":
        return value.strip().lower() in ("true", "1", "yes")
    return value.strip().strip('"').strip("'")


def parse_condition(tokens, column_types):
    """Разбирает список вида ['age', '=', '28'] в (столбец, значение)

    column_types — словарь {имя: тип}
    """
    if len(tokens) != 3 or tokens[1] != "=":
        raise ValueError("Ожидается условие вида <столбец> = <значение>")
    column, _, raw_value = tokens
    if column not in column_types:
        raise KeyError(f'Столбец "{column}" не найден.')
    return column, _cast(raw_value, column_types[column])


def parse_set(tokens, column_types):
    """Разбирает список вида ['age', '=', '29'] в (столбец, значение)"""
    return parse_condition(tokens, column_types)