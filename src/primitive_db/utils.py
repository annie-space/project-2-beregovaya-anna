"""Доп функции для работы с файлами"""

import json
import os

from primitive_db.constants import DATA_DIR, META_FILE


def load_metadata(filepath=META_FILE):
    """Загружает метаданные из JSON-файла, а если файла нет — пустой словарь"""
    try:
        with open(filepath, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_metadata(data, filepath=META_FILE):
    """Сохраняет метаданные в JSON-файл"""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _table_path(table_name):
    """Возвращает путь к JSON-файлу данных таблицы"""
    return os.path.join(DATA_DIR, f"{table_name}.json")


def load_table_data(table_name):
    """Загружает данные таблицы из файла. Если файла нет — пустой список"""
    try:
        with open(_table_path(table_name), encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    """Сохраняет данные таблицы в JSON-файл"""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(_table_path(table_name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)