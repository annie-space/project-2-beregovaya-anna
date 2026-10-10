"""Доп функции для работы с файлами"""

import json

from primitive_db.constants import META_FILE


def load_metadata(filepath=META_FILE):
    """Загружает метаданные из JSON-файла, а если файла нет — пустой словарь."""
    try:
        with open(filepath, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_metadata(data, filepath=META_FILE):
    """Сохраняет метаданные в JSON-файл."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)