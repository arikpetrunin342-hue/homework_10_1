import re
from typing import Union


def get_mask_account(mask__account: Union[int, str]) -> Union[int, str]:
    """Функция, которая выводит две * и последние 4 символа"""
    mask_account = re.sub(r"\D+", "", mask__account)
    if len(mask_account.replace(" ", "")) > 20:
        return "Вы ввели слишком много символов"
    elif len(mask_account.replace(" ", "")) == 0:
        return ""
    elif len(mask_account.replace(" ", "")) < 20:
        return "Вы пропустили некоторое количество символов"
    mask_account = "**" + str(mask_account)[-4:]
    return mask_account


def get_mask_card_number(card__number: Union[str, int]) -> Union[str, int]:
    """Функция маскирует номер карты в формате:
    XXXX XX** **** XXXX
    Автоматически удаляет пробелы из ввода."""
    card_number = re.sub(r"\D+", "", card__number)
    s = str(card_number).replace(" ", "")

    if len(s) == 0:
        return ""
    elif len(s) < 16:
        return "Номер слишком короткий"
    elif len(s) > 16:
        return "Номер слишком длинный"

    masked = s[:4] + " " + s[4:6] + "**" + " " + "****" + " " + s[-4:]

    return masked
