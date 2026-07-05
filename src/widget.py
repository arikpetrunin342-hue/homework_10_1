def mask_account_card(mask_account: str) -> str:
    """Функция, которая маскирует номер счета или номер карты"""
    if mask_account[:4] == "Счет":
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

from datetime import datetime

def get_date(date: str) -> str:
    """Функция, которая возвращает строку с датой в другом формате"""
    correct_date = datetime.fromisoformat(date)
    return correct_date.strftime('%d.%m.%Y')
