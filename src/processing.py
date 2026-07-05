from operator import itemgetter
from typing import Dict, List


def filter_by_state(
    data: List[Dict[str, str]], key: str = "EXECUTED"
) -> List[Dict[str, str]]:
    """Filters a list of operations by their state status.

    Args:
        data: A list of dictionaries representing operations.
        key: The status value to filter by (default is "EXECUTED").

    Returns:
        A list of dictionaries that match the specified status."""
    correct_list = []

    for item in data:
        if item.get("state") == key:
            correct_list.append(item)
    return correct_list


def sort_by_date(
    list_of_dict: List[Dict[str, str]], reverse: bool = True
) -> List[Dict[str, str]]:
    """Sorts a list of dictionaries by the 'date' key.

    Args:
        list_of_dict: A list of dictionaries containing a 'date' key.
        reverse: If True, sorts in descending order (default is True).

    Returns:
        A new list sorted by date."""
    return sorted(list_of_dict, key=itemgetter("date"), reverse=reverse)
