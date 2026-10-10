"""Команды"""

import shlex

import prompt

from primitive_db.core import create_table, drop_table, list_tables
from primitive_db.utils import load_metadata, save_metadata


def print_help():
    """Печатает справку по командам."""
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


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

        print(f"Функции {command} нет. Попробуйте снова.")