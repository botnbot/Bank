from loader import load_user_settings
from utils import convert_xlsx_to_list, SP500, exchange_rate
from utils import greeting
from dotenv import load_dotenv

load_dotenv(".env")

file_path = "user_settings.json"
data = load_user_settings(file_path)
user_currencies = data.get("user_currencies", [])
user_stocks = data.get("user_stocks", [])
path_to_datafile = str(data.get("path_to_datafile"))


greeting = greeting('10.01.2018 12:43:34')    #Eсли необходимо использовать текущую дату - параметр даты оставить пустым
print(greeting)

transactions = convert_xlsx_to_list(path_to_datafile)
print(transactions)

# stock_prices = SP500(user_stocks)
# print(stock_prices)
#
# currency_rates = exchange_rate(user_currencies)
# print(currency_rates)
