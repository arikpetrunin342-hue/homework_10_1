import pandas as pd


def read_csv_transactions(csv_path):
    """Функция считывает финансовые операции из CSV файла.

    Args:
        csv_path (str): Путь к CSV файлу.

    Returns:
        list of dict: Список словарей, где каждый словарь — это одна транзакция."""
    df = pd.read_csv(csv_path, sep=";", encoding="utf-8")
    return df.to_dict(orient="records")


def read_excel_transactions(excel_path):
    """Функция считывает финансовые операции из XLSX файла.

    Args:
        excel_path (str): Путь к Excel файлу.

    Returns:
        list of dict: Список словарей, где каждый словарь — это одна транзакция."""
    df = pd.read_excel(excel_path)
    return df.to_dict(orient="records")
