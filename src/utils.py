import json
import logging
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
LOGS_DIR = ROOT_DIR / "logs"
formatter = logging.Formatter("%(asctime)s: %(name)s: %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(LOGS_DIR / "utils.log", encoding="utf-8", mode="w")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)


def load_operations(path: str) -> list[dict]:
    """Принимает путь до JSON-файла и возвращает список словарей с транзакциями.
    Если файл не найден или пуст/невалидный, возвращается пустой список."""
    logger.info("Начало работы.")
    full_path = Path(__file__).parent.parent / path
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                logger.info("Список словарей с транзакциями найден. Завершение работы.")
                return data
            else:
                logger.info("Ничего не нашлось. Завершение работы.")
                return []
    except (ValueError, FileNotFoundError, json.JSONDecodeError):
        logger.error("Возникла ошибка. Возвращен пустой список. Завершение работы.")
        return []
