"""Команды"""

import shlex

import prompt
from prettytable import PrettyTable

from primitive_db.core import (
    create_table,
    delete,
    drop_table,
    info,
    insert,
    list_tables,
    select,
    update,
)
from primitive_db.parser import parse_condition, parse_set, parse_values
from primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)


def print_help():
    """Печатает справку по командам."""
    print("\n***Операции с данными***")
    print("Функции:")
    print(
        "<command> insert into <имя_таблицы> values "
        "(<значение1>, <значение2>, ...) - создать запись."
    )
    print(
        "<command> select from <имя_таблицы> where <столбец> = <значение> "
        "- прочитать записи по условию."
    )
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print(
        "<command> update <имя_таблицы> set <столбец1> = <новое_значение1> "
        "where <столбец_условия> = <значение_условия> - обновить запись."
    )
    print(
        "<command> delete from <имя_таблицы> where <столбец> = <значение> "
        "- удалить запись."
    )
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def _print_rows(metadata, table_name, rows):
    """Выводит список записей в виде prettytable."""
    if not rows:
        print("Записи не найдены.")
        return
    columns = [c.split(":")[0] for c in metadata[table_name]]
    table = PrettyTable()
    table.field_names = columns
    for row in rows:
        table.add_row([row.get(c) for c in columns])
    print(table)


def _col_types(metadata, table_name):
    """Возвращает словарь {имя: тип} для таблицы."""
    return {
        c.split(":")[0]: c.split(":")[1] for c in metadata[table_name]
    }


def run():
    """Основной цикл программы."""
    print("***База данных***")
    print_help()

    while True:
        try:
            user_input = prompt.string("Введите команду: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nВыход.")
            break

        if not user_input:
            continue

        args = shlex.split(user_input)
        command = args[0].lower()

        if command == "exit":
            print("Выход.")
            break

        if command == "help":
            print_help()
            continue

        if command == "create_table":
            if len(args) < 3:
                print("Некорректное значение. Попробуйте снова.")
                continue
            metadata = load_metadata()
            metadata = create_table(metadata, args[1], args[2:])
            save_metadata(metadata)
            continue

        if command == "drop_table":
            if len(args) != 2:
                print("Некорректное значение. Попробуйте снова.")
                continue
            metadata = load_metadata()
            metadata = drop_table(metadata, args[1])
            save_metadata(metadata)
            continue

        if command == "list_tables":
            metadata = load_metadata()
            list_tables(metadata)
            continue

        if command == "insert":
            # insert into <table> values (...)
            if (
                len(args) < 5
                or args[1].lower() != "into"
                or args[3].lower() != "values"
            ):
                print("Некорректное значение. Попробуйте снова.")
                continue
            metadata = load_metadata()
            table_name = args[2]
            raw_values = " ".join(args[4:])
            values = parse_values(raw_values)
            data = load_table_data(table_name)
            data = insert(metadata, data, table_name, values)
            save_table_data(table_name, data)
            continue

        if command == "select":
            # select from <table> [where <col> = <val>]
            if len(args) < 3 or args[1].lower() != "from":
                print("Некорректное значение. Попробуйте снова.")
                continue
            metadata = load_metadata()
            table_name = args[2]
            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue
            data = load_table_data(table_name)
            if len(args) == 3:
                rows = select(data)
            elif len(args) == 7 and args[3].lower() == "where":
                column, value = parse_condition(
                    args[4:7], _col_types(metadata, table_name)
                )
                rows = select(data, (column, value))
            else:
                print("Некорректное значение. Попробуйте снова.")
                continue
            _print_rows(metadata, table_name, rows)
            continue

        if command == "update":
            # update <table> set <col> = <val> where <col> = <val>
            if (
                len(args) < 10
                or args[2].lower() != "set"
                or args[6].lower() != "where"
            ):
                print("Некорректное значение. Попробуйте снова.")
                continue
            metadata = load_metadata()
            table_name = args[1]
            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue
            types = _col_types(metadata, table_name)
            set_clause = parse_set(args[3:6], types)
            where_clause = parse_condition(args[7:10], types)
            data = load_table_data(table_name)
            data = update(data, set_clause, where_clause)
            save_table_data(table_name, data)
            continue

        if command == "delete":
            # delete from <table> where <col> = <val>
            if (
                len(args) < 7
                or args[1].lower() != "from"
                or args[3].lower() != "where"
            ):
                print("Некорректное значение. Попробуйте снова.")
                continue
            metadata = load_metadata()
            table_name = args[2]
            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue
            types = _col_types(metadata, table_name)
            where_clause = parse_condition(args[4:7], types)
            data = load_table_data(table_name)
            data = delete(data, where_clause)
            save_table_data(table_name, data)
            continue

        if command == "info":
            if len(args) != 2:
                print("Некорректное значение. Попробуйте снова.")
                continue
            metadata = load_metadata()
            table_name = args[1]
            data = load_table_data(table_name)
            info(metadata, table_name, data)
            continue

        print(f"Функции {command} нет. Попробуйте снова.")