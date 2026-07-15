import re
from datetime import datetime


def mask_account_card(mask_account: str) -> str:
    """Функция, которая маскирует номер счета или номер карты"""
    if mask_account is None or len(mask_account) == 0:
        return ""
    if not isinstance(mask_account, str):
        return ""
    mask_account = mask_account.strip()
    if len(mask_account) == 0:
        return ""
    elif mask_account[:4] == "Счет":
        mask_account = mask_account[:5] + "**" + mask_account[-4:]
    else:
        mask_account = mask_account[:-10] + "******" + mask_account[-4:]
        mask_account = (
            mask_account[:-16]
            + mask_account[-16:-12]
            + " "
            + mask_account[-12:-8]
            + " "
            + mask_account[-8:-4]
            + " "
            + mask_account[-4:]
        )
    return mask_account


def get_date(dates: str) -> str:
    """Функция, которая возвращает строку с датой в другом формате"""
    if not dates or len(dates) == 0:
        return ""
    date = re.sub(r"\D+", "", dates)
    date = date[:8]
    try:
        dt = datetime.fromisoformat(date)
        return dt.strftime("%d.%m.%Y")
    except ValueError:
        return ""
