from loader import load_user_settings
from utils import convert_xlsx_to_list, filter_from_month_begin, filter_personal_transfers

def personal_transfers():
    datetime_str = input("Введите дату в формате YYYY-MM-DD HH:MM:SS  ")
    file_path = "user_settings.json"
    data = load_user_settings(file_path)
    path_to_datafile = str(data.get("path_to_datafile"))
    transactions = convert_xlsx_to_list(path_to_datafile)
    filtered_month = filter_from_month_begin(transactions, datetime_str)
    result = filter_personal_transfers(filtered_month)
    return result
print("Переводы физлицам:", personal_transfers())
