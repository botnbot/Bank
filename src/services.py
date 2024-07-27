import json
import re
from typing import Any

import pandas as pd

from .utils import filter_from_month_begin


def personal_transfers(list_of_transactions: list[dict[str, Any]], datetime_str: str) -> str:
    """
    Фильтрует переводы физическим лицам из списка транзакций с начала указанного месяца.
    """
    filtered_month = filter_from_month_begin(list_of_transactions, datetime_str)
    def is_personal_transfer(transaction: dict[str, Any]) -> bool:
        """
        Проверяет, является ли транзакция переводом физическому лицу.
        """
        name_pattern = re.compile(r"[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.")
        category_check = transaction.get("Категория") == "Переводы"
        description_check = name_pattern.search(transaction.get("Описание", ""))
        return category_check and description_check

    # Приведение данных (замена NaN на "")
    cleaned_transactions = [
        {k: ("" if pd.isna(v) else v) for k, v in transaction.items()}
        for transaction in filtered_month
    ]
    # Фильтрация транзакций
    filtered_transactions = filter(is_personal_transfer, cleaned_transactions)
    # Преобразование в JSON
    result_json = json.dumps(list(filtered_transactions), ensure_ascii=False, indent=4)
    return result_json