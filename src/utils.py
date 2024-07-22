from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
from pathlib import Path
from typing import Any
import re
import json
import os
from datetime import datetime
from math import isnan
from typing import Any
import requests
from datetime import datetime
from typing import List, Dict, Any, Optional
from dateutil.relativedelta import relativedelta

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


def filter_transactions_3m(transactions: list[dict[str, Any]], date_str: Optional[str] = None) -> list[dict[str, Any]]:
    """Функция фильтрации транзакций за последние три месяца от заданной даты"""
    try:
        if date_str is None:
            date_str = datetime.now()
        else:
            date_str = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        date_str = datetime.now()
    three_months_ago = date_str - relativedelta(months=3)
    filtered_transactions_3m = []
    for transaction in transactions:
        date_str = transaction.get('Дата операции')
        if date_str:
            try:
                transaction_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                if transaction_date >= three_months_ago:
                    filtered_transactions_3m.append(transaction)
            except ValueError:
                continue
    return filtered_transactions_3m


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


def SP500(user_stocks: list[str]) -> dict[str, Any]:
    """Функция, возвращающая курс выбранных акций"""
    stock_prices = {}
    api_key = os.getenv("AV_API_KEY")
    for stock in user_stocks:
        url = (f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol"
               f"={stock}&interval=1min&apikey={api_key}")
        response = requests.get(url)
        data = response.json()

        if "Meta Data" in data:
            try:
                last_refreshed = data["Meta Data"]["3. Last Refreshed"]
                stock_prices[stock] = data["Time Series (1min)"][last_refreshed]["1. open"]
            except KeyError:
                stock_prices[stock] = "N/A"
                print(f"Ошибка получения данных для акции {stock}: Неверная структура данных")
        else:
            stock_prices[stock] = "N/A"
            print(f"Ошибка получения данных для акции {stock}: {data}")
    return stock_prices


def exchange_rate(user_currencies: list[str]) -> dict[str, Any]:
    """Функция, возвращающая курс выбранных валют к рублю"""
    apikey = os.getenv("API_KEY")
    results = {}
    for currency in user_currencies:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount=1"
        headers = {"apikey": apikey}
        response = requests.get(url, headers=headers)
        data = response.json()

        if "result" in data:
            results[currency] = round(data["result"], 2)
        else:
            results[currency] = {"rate_to_rub": "N/A", "error": data.get("error", "Unknown error")}
    return results


def filter_transactions_by_category(transactions: list[dict[str, any]], category: str) -> pd.DataFrame:
    """ Фильтрует транзакции по заданной категории и возвращает DataFrame."""
    df = pd.DataFrame(transactions)
    filtered_df = df[df['category'] == category]
    return filtered_df
