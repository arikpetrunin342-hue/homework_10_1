import logging
import re
from pathlib import Path
from typing import Union

ROOT_DIR = Path(__file__).parent.parent
LOGS_DIR = ROOT_DIR / "logs"
formatter = logging.Formatter("%(asctime)s: %(name)s: %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(LOGS_DIR / "masks.log", encoding="utf-8", mode="w")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)


def get_mask_account(mask__account: Union[int, str]) -> Union[int, str]:
    """Функция, которая выводит две * и последние 4 символа"""
    logger.info("Начало работы.")
    mask_account = re.sub(r"\D+", "", mask__account)
    if len(mask_account.replace(" ", "")) > 20:
        logger.info("Введено символов больше чем нужно. Завершение работы.")
        return "Вы ввели слишком много символов."
    elif len(mask_account.replace(" ", "")) == 0:
        logger.info("Ничего не введено.")
        return ""
    elif len(mask_account.replace(" ", "")) < 20:
        logger.info("Некоторое количество символов было пропущено. Завершение работы.")
        return "Вы пропустили некоторое количество символов."
    mask_account = "**" + str(mask_account)[-4:]
    logger.info("Всё введено корректно. Завершение работы.")
    return mask_account


def get_mask_card_number(card__number: Union[str, int]) -> Union[str, int]:
    """Функция маскирует номер карты в формате:
    XXXX XX** **** XXXX
    Автоматически удаляет пробелы из ввода."""
    logger.info("Начало работы.")
    card_number = re.sub(r"\D+", "", card__number)
    s = str(card_number).replace(" ", "")

    if len(s) == 0:
        logger.info("Ничего не введено.")
        return ""
    elif len(s) < 16:
        logger.info("Некоторое количество символов было пропущено. Завершение работы.")
        return "Номер слишком короткий."
    elif len(s) > 16:
        logger.info("Введено символов больше чем нужно. Завершение работы.")
        return "Номер слишком длинный."

    masked = s[:4] + " " + s[4:6] + "**" + " " + "****" + " " + s[-4:]

    logger.info("Всё введено корректно. Завершение работы.")
    return masked
