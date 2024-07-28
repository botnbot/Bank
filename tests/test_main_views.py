import pandas as pd
from _datetime import datetime

from src.loader import load_user_settings
from src.reports import spending_by_category
from src.services import personal_transfers
from src.utils import convert_xlsx_to_list
from src.views import main_page

data = load_user_settings("user_settings.json")
path_to_datafile = str(data.get("path_to_datafile"))

df_to_func = pd.read_excel(path_to_datafile)  # преобразуем из Excel, т.к. DataFrame взять негде

datetime_str = '2018-06-18'
result_main_page = print(main_page(df_to_func, datetime_str))
try:
    date = datetime.strptime(datetime_str, "%Y-%m-%d")
except ValueError:
    date = datetime.now()
