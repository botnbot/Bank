import json
import re

import pandas as pd

from loader import load_user_settings
from utils import convert_xlsx_to_list
from utils import filter_from_month_begin


def filter_personal_transfers(transactions):
    """Функция фильтрации переводов физ.лицам"""
    name_pattern = re.compile(r"[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.")

    def is_personal_transfer(transaction):
        """Функция прверки категории и описания"""
        category_check = transaction.get("Категория") == "Переводы"
        description_check = name_pattern.search(transaction.get("Описание", ""))
        return category_check and description_check

    cleaned_transactions = [
        {k: ("" if pd.isna(v) else v) for k, v in transaction.items()} for transaction in transactions
    ]

    filtered_transactions = filter(is_personal_transfer, cleaned_transactions)


    return json.dumps(list(filtered_transactions), ensure_ascii=False, indent=4)
datetime_str = input('Введите дату в формате YYYY-MM-DD HH:MM:SS  ')
file_path = "user_settings.json"
data = load_user_settings(file_path)
path_to_datafile = str(data.get("path_to_datafile"))
transactions = convert_xlsx_to_list(path_to_datafile)
filtered_month = filter_from_month_begin(transactions, datetime_str)
result = filter_personal_transfers(filtered_month)

print("Filtered Transactions:", result)
