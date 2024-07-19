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


def greeting(date_str: str = datetime.now()) -> str:
    dt = datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")
    current_time = dt.time()

    if time(6, 0, 0) <= current_time <= time(10, 59, 59):
        greeting_message = "Доброе утро"
    elif time(11, 0, 0) <= current_time <= time(15, 59, 59):
        greeting_message = "Добрый день"
    elif time(16, 0, 0) <= current_time <= time(22, 59, 59):
        greeting_message = "Добрый вечер"
    else:
        greeting_message = "Доброй ночи"

    response = {"greeting": greeting_message}

    return json.dumps(response, ensure_ascii=False)


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

