import prompt


def welcome():
    """Приветствие и первый запрос команды"""
    print("***")
    print("<command> exit - Выйти из программы")
    print("<command> help - Справочная информация")
    prompt.string("Введите команду: ")