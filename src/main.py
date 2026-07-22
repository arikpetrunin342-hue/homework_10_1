from pathlib import Path

from financial_operations import read_csv_transactions, read_excel_transactions

current_dir = Path(__file__).parent
project_root = current_dir.parent

csv_file = project_root / "data" / "transactions.csv"
excel_file = project_root / "data" / "transactions.xlsx"

print("Данные из CSV:")
for transaction in read_csv_transactions(csv_file)[:3]:
    print(transaction)

print("\nДанные из Excel:")
for transaction in read_excel_transactions(excel_file)[:3]:
    print(transaction)
