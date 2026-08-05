import json
import logging
import re
import time
from pathlib import Path

import pandas as pd

import src.masks as mask_utils
from src import widget
from src.widget import mask_account_card

logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)

current_dir = Path(__file__).parent
project_root = current_dir.parent

csv_file = project_root / "data" / "transactions.csv"
excel_file = project_root / "data" / "transactions.xlsx"
json_file = project_root / "data" / "transactions.json"


def mask_description(description):
    parts = re.split(r"( -> |;|,|\bна\s+карту\b|\bсо\s+счета\b)", description)

    masked_parts = []
    for part in parts:
        if not part.strip():
            continue

        card_number_match = re.search(r"\d{16}", part)
        if card_number_match:
            number = int(card_number_match.group())
            masked_card = f"{mask_utils.get_mask_card_number(number)}"
            masked_part = part.replace(str(number), masked_card)

        elif "Счет" in part and len(part) > 5:
            masked_part = "Счет ****"

        else:
            masked_part = part

        masked_parts.append(masked_part)

    return "".join(masked_parts).strip()


def main(file_path=None):
    print("""Привет! Добро пожаловать в программу работы
с банковскими транзакциями.
Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информация о транзакциях из XLSX-файла""")

    input_format = int(input(">>> "))

    if input_format not in [1, 2, 3]:
        print("Ошибка: неверный номер пункта меню!")
        return

    if input_format == 1:
        print("Для обработки выбран JSON-файл.")
    elif input_format == 2:
        print("Для обработки выбран CSV-файл.")
    else:
        print("Для обработки выбран XLSX-файл.")

    while True:
        input_status = input(
            "\nВведите статус, по которому необходимо выполнить фильтрацию.\n"
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n>>>"
        ).strip()

        pattern = r"^\s*(EXECUTED|CANCELED|PENDING)?\s*$"
        match = re.fullmatch(pattern, input_status.upper(), flags=re.IGNORECASE)

        if match is None:
            print(f'Статус операции "{input_status}" недоступен.')
        else:
            break

    status_upper = input_status.upper() if input_status else None

    if status_upper:
        print(f"Операции отфильтрованы по статусу '{status_upper}'.")
    else:
        print("Операции отфильтрованы без учёта статуса.")

    input_data = input("Отсортировать операции по дате? [Да/Нет]\n>>>").upper()
    if input_data in ["YES", "Y", "ДА", "Д"]:
        input_data = "ДА"
    else:
        input_data = "НЕТ"

    input_sort = input("Отсортировать по возрастанию или по убыванию?\n>>>").upper()
    if input_sort == "ПО ВОЗРАСТАНИЮ":
        input_sort = "ВОЗРАСТАНИЮ"
    elif input_sort == "ПО УБЫВАНИЮ":
        input_sort = "УБЫВАНИЮ"

    input_rub = input("Выводить только рублевые транзакции? [Да/Нет]\n>>>").upper()
    if input_rub in ["YES", "Y", "ДА", "Д"]:
        input_rub = "ДА"
    else:
        input_rub = "НЕТ"

    input_word_yes_or_no = input(
        "Отфильтровать операции по определённому слову в описании? [Да/Нет]\n>>>"
    ).upper()
    input_word = ""
    if input_word_yes_or_no.upper() in ["ДА", "Д"]:
        input_word = input("Введите слово по которому вы хотите отфильтровать.\n>>>")
        if not input_word.strip():
            input_word_yes_or_no = "Нет"

    print("Распечатываю итоговый список транзакций...")
    time.sleep(3)

    if input_format == 1:
        with open(json_file, encoding="utf-8") as f:
            json.load(f)  # data =
        df = pd.read_json(json_file)
    elif input_format == 2:
        df = pd.read_csv(csv_file, sep=";", encoding="utf-8")  # , parse_dates=['date']
    elif input_format == 3:
        df = pd.read_excel(excel_file)

    mask = df["state"].str.upper() == status_upper

    if input_rub == "ДА":
        mask &= df["currency_code"].str.upper() == "RUB"

    df["date"] = pd.to_datetime(df["date"], utc=True)

    if input_word and input_word.strip():
        mask &= df["description"].apply(
            lambda x: any(word.upper() == input_word.upper() for word in str(x).split())
        )

    selected_operations = df.loc[
        mask,
        [
            "state",
            "date",
            "amount",
            "currency_code",
            "description",
            "from",
            "to",
        ],
    ]

    #

    ascending_order = True if input_sort == "ВОЗРАСТАНИЮ" else False
    selected_operations.sort_values(by="date", ascending=ascending_order, inplace=True)

    filtered_series = (
        selected_operations["state"]
        .where(selected_operations["state"].str.upper() == status_upper)
        .dropna()
    )
    res = filtered_series.value_counts()
    print(f"Всего банковских операций в выборке: {len(selected_operations)}\n")

    for _, row in selected_operations.iterrows():

        if input_data == "ДА":
            date_str = pd.to_datetime(row["date"]).strftime("%d.%m.%Y")
        else:
            date_str = pd.to_datetime(row["date"]).strftime("%Y-%m-%dT%H:%M:%SZ")

        masked_description_parts = []
        for word in row["description"].split():
            if len(word) == 16 and word.isdigit() or word.startswith("Счет"):
                masked_word = widget.mask_account_card(word)
            else:
                masked_word = word

            masked_description_parts.append(masked_word)

        masked_description = " ".join(masked_description_parts)

        current_from = row["from"]
        current_to = row["to"]

        if pd.isna(current_from):
            from_str = "-"
        else:
            from_str = mask_account_card(str(current_from))

        if pd.isna(current_to):
            to_str = "-"
        else:
            to_str = mask_account_card(str(current_to))

        print(
            f"{date_str} "
            f"{masked_description}\n"
            f"{from_str} -> {to_str}"
            f"\nСумма: {row['amount']} {row['currency_code']}\n"
        )


def run():
    main()


if __name__ == "__main__":
    run()
