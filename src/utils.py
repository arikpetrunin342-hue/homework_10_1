import json
from pathlib import Path


def load_operations(path: str) -> list[dict]:
    """Принимает путь до JSON-файла и возвращает список словарей с транзакциями.
    Если файл не найден или пуст/невалидный, возвращается пустой список."""
    full_path = Path(__file__).parent.parent / path
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            data =  json.load(f)
            if isinstance(data, list):
                return data
            else:
                return []
    except (ValueError, FileNotFoundError, json.JSONDecodeError):
        return []
