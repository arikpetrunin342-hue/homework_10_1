from typing import Union


def get_mask_account(mask_account: Union[int, str]) -> Union[int, str]:
    """Функция, которая выводит две * и последние 4 символа"""
    mask_account = "**" + str(mask_account)[-4:]
    return mask_account


from typing import Union


def get_mask_card_number(card_number: Union[str, int]) -> Union[str, int]:
    """Функция, которая выводит первые 6 символов и последние 4 символа, оставшиеся символы заменяются на *"""
    card_number = str(card_number)[:6] + "******" + str(card_number)[-4:]
    card_number = (
        str(card_number)[:4] + " " + str(card_number)[4:8] + " " + str(card_number)[8:12] + " " + str(card_number)[12:]
    )
    return card_number
