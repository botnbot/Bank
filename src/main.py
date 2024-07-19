from loader import load_user_settings
from utils import convert_xlsx_to_list, filter_by_time
from dotenv import load_dotenv
from views import  SP500, exchange_rate, greeting



file_path = "user_settings.json"
data = load_user_settings(file_path)
user_currencies = data.get("user_currencies", [])
user_stocks = data.get("user_stocks", [])
path_to_datafile = str(data.get("path_to_datafile"))


greeting = greeting('10.01.2018 12:43:34')    #Eсли необходимо использовать текущую дату - параметр даты оставить пустым
print(greeting)

transactions = convert_xlsx_to_list(path_to_datafile)
# print(transactions)




last_3_months = filter_by_time(transactions, '13.08.2020 12:49:53')
print(last_3_months)

# sorted_by_date = sort_by_date(last_3_m)
# print(sorted_by_date)

# stock_prices = SP500(user_stocks)
# print(stock_prices)
#
# currency_rates = exchange_rate(user_currencies)
# print(currency_rates)
