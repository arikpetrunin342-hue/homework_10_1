
def filter_by_currency(transactions, key = "USD"):
    return (x for x in transactions if x.get("operationAmount") and x["operationAmount"].get("currency")
                                        and (x["operationAmount"]["currency"].get("name") == key
                                             or x["operationAmount"]["currency"].get("name") == key))

def transaction_descriptions(transactions):
    for transaction in transactions:
        desc = transaction.get("description")
        if desc is not None:
            yield desc
        else:
            yield ""

def card_number_generator(start=1, end=int(1e15)):

    if not isinstance(start, int) or not isinstance(end, int):
        raise TypeError("Аргументы должны быть целыми числами.")
    if start < 1 or end > int(1e15):
        raise ValueError("Номера карт должны быть в диапазоне от 1 до 9999999999999999")
    if start > end:
        raise ValueError("Конечное значение должно быть больше начального.")

    for number in range(start, end + 1):
        num_str = f"{number:016d}"

        formated_card = " ".join([num_str[i: i + 4] for i in range(0, len(num_str), 4)])

        yield formated_card
