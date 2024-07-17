from datetime import datetime, time
import json
from loader import load_user_settings
from utils import convert_xlsx_to_list, SP500, exchange_rate

def greeting(date_str: str) -> str:
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

    response = {
        "greeting": greeting_message
    }

    return json.dumps(response, ensure_ascii=False)

file_path = "user_settings.json"
data = load_user_settings(file_path)
user_currencies = data.get("user_currencies", [])
user_stocks = data.get("user_stocks", [])
path_to_datafile = data.get("path_to_datafile", [])

print(greeting('10.01.2018 12:43:34'))
transactions = convert_xlsx_to_list(path_to_datafile)
print(transactions)

stock_prices = SP500(user_stocks)
print(stock_prices)

currency_rates = exchange_rate(user_currencies)
print(currency_rates)
