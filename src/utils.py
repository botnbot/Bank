import json
import os
import re
from datetime import datetime
from math import isnan
from pathlib import Path
from typing import Any, Optional

import pandas as pd
import requests
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv

from loader import load_user_settings

load_dotenv(".env")


def convert_xlsx_to_dataframe(file_name: str) -> pd.DataFrame:
    """Функция преобразующая файл xlsx в DataFrame"""
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


def greeting():
    current_time = datetime.now()
    if 5 <= current_time.hour < 12:
        return "Доброе утро"
    elif 12 <= current_time.hour < 18:
        return "Добрый день"
    elif 18 <= current_time.hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


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
            end_date_time = datetime.strptime(end_date, date_format_without_time_iso)
        except ValueError:
            print("Введена некорректная дата. Будет использована текущая дата")
            end_date_time = datetime.now()
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


def filter_transactions_3_months(
    transactions: list[dict[str, Any]], date: Optional = datetime.now()
) -> list[dict[str, Any]]:
    three_months_ago = date - relativedelta(months=3)
    print(f"Начало отсчета периода {three_months_ago}")
    print(f"Конец отсчета периода {date}")
    filtered_transactions_3m = []

    for transaction in transactions:
        trxn_date_str = transaction.get("Дата операции")
        if trxn_date_str:
            transaction_date = datetime.strptime(trxn_date_str, "%d.%m.%Y %H:%M:%S")
            if transaction_date:
                if date >= transaction_date >= three_months_ago:
                    filtered_transactions_3m.append(transaction)

    return filtered_transactions_3m


def filter_personal_transfers(transactions: list[dict]) -> Any:
    """Функция фильтрации переводов физ.лицам"""
    name_pattern = re.compile(r"[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.")

    def is_personal_transfer(transaction):
        """Функция прверки категории и описания транзакции"""
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
        url = (
            f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY"
            f"&symbol={stock}&interval=1min&apikey={api_key}"
        )
        response = requests.get(url)
        data = response.json()

        if "Meta Data" in data:
            try:
                last_refreshed = data["Meta Data"]["3. Last Refreshed"]
                stock_prices[stock] = data["Time Series (1min)"][last_refreshed]["1. open"]
            except KeyError:
                stock_prices[stock] = "N/A"
                print(f"Ошибка получения данных для акции {stock}: Неверный код валюты")
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
    """Фильтрует транзакции по заданной категории  за последние 3 месяца и возвращает DataFrame."""
    if not transactions:
        print("Нет транзакций по заданной категории")
        return
    df = pd.DataFrame(transactions)
    if "Категория" not in df.columns:
        raise ValueError('В данных нет столбца "Категория"')
    filtered_df = df[df["Категория"] == category]
    if filtered_df.empty:
        print("По выбранной категории в указанный период трат нет")
    return filtered_df


def create_response(df: pd.DataFrame, datetime_str: str) -> str:
    """Функция формирования JSON-ответа для главной страницы"""
    from utils import greeting

    data = load_user_settings("user_settings.json")
    user_currencies = data.get("user_currencies", [])
    user_stocks = data.get("user_stocks", [])
    trxns = df.to_dict(orient="records")
    transactions = filter_from_month_begin(trxns, datetime_str)

    card_summary = {}
    for transaction in transactions:
        card_number = transaction.get("Номер карты")
        if isinstance(card_number, str):
            card_number = card_number[-4:]
        else:
            continue
        amount = transaction.get("Сумма операции", 0)
        if isinstance and isnan(amount):
            amount = 0
        if amount < 0:
            if card_number not in card_summary:
                card_summary[card_number] = {"total_spent": 0, "cashback": 0}
            card_summary[card_number]["total_spent"] += abs(amount)
            card_summary[card_number]["cashback"] += abs(amount) * 0.01
    cards = []
    for card_number, summary in card_summary.items():
        cards.append(
            {
                "last_digits": card_number,
                "total_spent": round(summary["total_spent"], 2),
                "cashback": round(summary["cashback"], 2),
            }
        )

    # Топ-5 транзакций по сумме
    expense_transactions = [trans for trans in transactions if trans["Сумма операции"] < 0]
    top_transactions = sorted(expense_transactions, key=lambda x: abs(x["Сумма операции"]), reverse=True)[:5]
    top_transactions_list = [
        {
            "date": trans["Дата операции"],
            "amount": trans["Сумма операции"],
            "category": trans["Категория"] if pd.notna(trans["Категория"]) else "",
            "description": trans["Описание"],
        }
        for trans in top_transactions
    ]

    exchange_rates = exchange_rate(user_currencies)
    stock_prices = SP500(user_stocks)
    greeting = greeting()

    response = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions_list,
        "currency_rates": exchange_rates,
        "stock_prices": stock_prices,
    }
    return json.dumps(response, ensure_ascii=False, indent=4)
