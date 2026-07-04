from operator import itemgetter


def filter_by_state(
        data: list[dict], key: str = "EXECUTED"
) -> list[dict]:
    """Функция фильтрации по статусу"""
    correct_list = []

    for item in data:
        if item.get("state") == key:
            correct_list.append(item)
    return correct_list


def sort_by_date(list_of_dict: list[dict], reverse: bool = True) -> list[dict]:
    """Функция сортировки по дате"""
    return sorted(list_of_dict, key=itemgetter("date"), reverse=reverse)
