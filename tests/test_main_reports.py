import pandas as pd
from _datetime import datetime
from src.loader import load_user_settings
from src.reports import spending_by_category

data = load_user_settings("user_settings.json")
path_to_datafile = str(data.get("path_to_datafile"))

df_to_func = pd.read_excel(path_to_datafile)  # преобразуем из Excel, т.к. DataFrame взять негде
cat = 'Дом и ремонт'
datetime_str = '2018-06-18'
try:
    date = datetime.strptime(datetime_str, "%Y-%m-%d")
except ValueError:
    date = datetime.now()

result_js = spending_by_category(df_to_func, cat, date)

