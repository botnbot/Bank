import os
from utils import convert_xlsx_to_dataframe, filter_from_month_begin, exchange_rate, SP500
from loader import load_user_settings
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pathlib import Path
from typing import Any
from dotenv import load_dotenv
import pandas as pd
import json
from math import isnan

load_dotenv(".env")



def create_response(transactions: list[dict[str, Any]], datetime_str: str) -> str:
    """Функция формирования JSON-ответа"""
    date_format_with_time = "%Y-%m-%d %H:%M:%S"
    date_format_without_time = "%Y-%m-%d"
    try:
              current_datetime = datetime.strptime(datetime_str, date_format_with_time)
    except ValueError:
        try:
            current_datetime = datetime.strptime(datetime_str, date_format_without_time)
        except ValueError:
            print("Неверный формат даты и времени. Будет использовано текущее время.")
            current_datetime = datetime.now()
    current_time = current_datetime.time()
    if 5 <= current_time.hour < 12:
        greeting = "Доброе утро"
    elif 12 <= current_time.hour < 18:
        greeting = "Добрый день"
    elif 18 <= current_time.hour < 23:
        greeting = "Добрый вечер"
    else:
        greeting = "Доброй ночи"
    card_summary = {}
    for transaction in transactions:
        card_number = transaction.get("Номер карты")
        if isinstance(card_number, str):
            card_number = card_number[-4:]
        else:
            continue
        amount = transaction.get("Сумма операции", 0)
        if isinstance(amount, float) and isnan(amount):
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

    # Топ-5 транзакций по сумме (учитываем только расходы)
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

    response = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions_list,
        "currency_rates": exchange_rates,
        "stock_prices": stock_prices,
    }

    return json.dumps(response, ensure_ascii=False, indent=4)

datetime_str = input('Введите дату в формате YYYY-MM-DD HH:MM:SS  ')
file_path = "user_settings.json"
data = load_user_settings(file_path)
user_currencies = data.get("user_currencies", [])
user_stocks = data.get("user_stocks", [])
path_to_datafile = str(data.get("path_to_datafile"))
all_transactions = convert_xlsx_to_dataframe(path_to_datafile)
trxns = all_transactions.to_dict(orient="records")
transactions = filter_from_month_begin(trxns, datetime_str)
response_json = create_response(transactions, datetime_str)
print(response_json)
