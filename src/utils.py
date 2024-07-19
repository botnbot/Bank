import os
from datetime import datetime, time
from dateutil.relativedelta import relativedelta
from pathlib import Path
from typing import Any, Dict, List
from dotenv import load_dotenv
import pandas as pd
import requests
import json

load_dotenv(".env")





def convert_xlsx_to_list(file_name: str) -> List[dict]:
    transactions = []
    try:
        if not Path(file_name).is_file():
            raise FileNotFoundError(f"Файл '{file_name}' не найден.")

        excel_df = pd.read_excel(file_name)
        transactions = excel_df.to_dict(orient="records")

    except ValueError as e:
        print(type(e))
    except Exception as e:
        print(f"Произошла ошибка при чтении файла '{file_name}': {str(e)}")
    return transactions


def SP500(user_stocks: List[str]) -> dict:
    stock_prices = {}
    api_key = os.getenv("AV_API_KEY")
    for stock in user_stocks:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock}&interval=1min&apikey={api_key}"
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


def exchange_rate(user_currencies: List[str]) -> Dict[str, Any]:
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


def filter_by_time(transactions: list[dict], end_date: str = None) -> list[dict]:
    """Функция фильтрации транзакций по дате (последние три месяца)"""

    date_format_with_time = "%d.%m.%Y %H:%M:%S"
    date_format_without_time = "%d.%m.%Y"

    # Определение даты окончания
    if end_date:
        try:
            end_date_time = datetime.strptime(end_date, date_format_with_time)
        except ValueError:
            end_date_time = datetime.strptime(end_date, date_format_without_time)
    else:
        end_date_time = datetime.now()

    # Вычисление даты начала
    start_date = end_date_time - relativedelta(months=3)
    last_three_months = []


    # Фильтрация транзакций по дате за предшествующие три месяца
    for transaction in transactions:
        transaction_date_str = transaction.get("Дата операции")
        if transaction_date_str:
            try:
                transaction_date = datetime.strptime(transaction_date_str, date_format_with_time)
            except ValueError:
                transaction_date = datetime.strptime(transaction_date_str, date_format_without_time)
            if  start_date <= transaction_date <= end_date_time:
                last_three_months.append(transaction)

    return last_three_months




# if __name__ == "__main__":

    # transactions = convert_xlsx_to_list("data/operations.xlsx")
    # txs = (filter_by_time(transactions,'04.01.2018 14:05:08', ))
    # print(txs['Дата операции'])
    # user_currencies = ["USD", "EUR", "RUB", "GBP"]
    # user_stocks = ["AAPL", "AMZN", "GOOGL", "YANDEX", "MSFT", "TSLA"]
    # print(SP500(user_stocks))
    # print(exchange_rate(user_currencies))
    # print("User Currencies:", user_currencies)
    # print("User Stocks:", user_stocks)