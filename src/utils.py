from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
from pathlib import Path
from typing import Any
import re
import json

load_dotenv(".env")


def convert_xlsx_to_dataframe(file_name: str) -> pd.DataFrame:
    '''Функция преобразующая файл xlsx в DataFrame'''
    df = pd.DataFrame()
    try:
        if not Path(file_name).is_file():
            raise FileNotFoundError(f"Файл '{file_name}' не найден.")

        df = pd.read_excel(file_name)

    except ValueError as e:
        print(f"Произошла ошибка при чтении файла '{file_name}': {e}")
    except Exception as e:
        print(f"Произошла ошибка при чтении файла '{file_name}': {str(e)}")

    return df


def convert_xlsx_to_list(file_name: str) -> list:
    transactions = []
    try:
        if not Path(file_name).is_file():
            raise FileNotFoundError(f"Файл '{file_name}' не найден.")

        excel_df = pd.read_excel(file_name)
        transactions = excel_df.to_dict(orient="records")

    except ValueError as e:
        print(f"Произошла ошибка при чтении файла '{file_name}': {e}")
    except Exception as e:
        print(f"Произошла ошибка при чтении файла '{file_name}': {str(e)}")

    return transactions


def filter_from_month_begin(transactions: list, end_date: Any = datetime.now()) -> list[dict]:
    """Функция фильтрации транзакций по дате (с начала месяца)"""

    # Определение форматов дат
    date_format_with_time_iso = "%Y-%m-%d %H:%M:%S"
    date_format_with_time_rus = "%d.%m.%Y %H:%M:%S"
    date_format_without_time_iso = "%Y-%m-%d"
    date_format_without_time_rus = "%d.%m.%Y"

    # Определение даты окончания
    if end_date:
        try:
            end_date_time = datetime.strptime(end_date, date_format_with_time_iso)
        except ValueError:
            end_date_time = datetime.strptime(end_date, date_format_without_time_iso)
    else:
        end_date_time = datetime.now()

    # Определение даты начала месяца
    start_date = end_date_time.replace(day=1)

    filtered_transactions = []

    for transaction in transactions:
        transaction_date_str = transaction.get("Дата операции")
        if transaction_date_str:
            # Попытка разобрать дату транзакции
            try:
                transaction_date = datetime.strptime(transaction_date_str, date_format_with_time_iso)
            except ValueError:
                try:
                    transaction_date = datetime.strptime(transaction_date_str, date_format_without_time_iso)
                except ValueError:
                    try:
                        transaction_date = datetime.strptime(transaction_date_str, date_format_with_time_rus)
                    except ValueError:
                        transaction_date = datetime.strptime(transaction_date_str, date_format_without_time_rus)
            if start_date <= transaction_date <= end_date_time:
                filtered_transactions.append(transaction)

    return filtered_transactions


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