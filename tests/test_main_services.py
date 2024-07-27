from _datetime import datetime
from src.loader import load_user_settings
from src.services import personal_transfers
from src.utils import convert_xlsx_to_list

data = load_user_settings("user_settings.json")
path_to_datafile = str(data.get("path_to_datafile"))

list_to_func = convert_xlsx_to_list(path_to_datafile) # преобразуем из Excel, т.к. список словарей взять негде
datetime_str = '2018-06-18'
try:
    datetime_str = datetime.strptime(datetime_str, "%Y-%m-%d")
except ValueError:
    datetime_str = datetime.strftime(datetime.now(), "%Y-%m-%d")
result_service = personal_transfers(list_to_func, datetime_str)