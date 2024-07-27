import pandas as pd
from _datetime import datetime

from src.loader import load_user_settings
from src.reports import spending_by_category
from src.services import personal_transfers
from src.utils import convert_xlsx_to_list
from src.views import main_page

data = load_user_settings("user_settings.json")
path_to_datafile = str(data.get("path_to_datafile"))

list_to_func = convert_xlsx_to_list(path_to_datafile) # преобразуем из Excel, т.к. список словарей взять негде
df_to_func = pd.read_excel(path_to_datafile)  # преобразуем из Excel, т.к. DataFrame взять негде

datetime_str = input("Введите дату для формирования отчета в формате YYYY-MM-DD  ")

print(
    """Выберите категорию для отображения
        1 Главная страница
        2 Сервис фильтрации по переводам (физическим лицам)
        3 Отчет по категории трат"""
)
menu = ""
while menu not in ("1", "2", "3"):
    menu = input("Введите номер категории\n")
    if menu not in ("1", "2", "3"):
        print("Некорректный ввод.Введите 1, 2, или 3. \n")
    if menu == "1":
        print("Главная страница")
        print(main_page(df_to_func, datetime_str))
    elif menu == "2":
        print("Выбран сервис фильтрации (переводы физическим лицам)")
        print(personal_transfers(list_to_func, datetime_str))
    elif menu == "3":
        print(" Выбран очет по категории трат ")
        cat = input("Введите категорию трат\n")
        try:
            date = datetime.strptime(datetime_str, "%Y-%m-%d")
        except ValueError:
            print("Введена некорректная дата. Была использована текущая дата")
            date = datetime.now()
        result_js = spending_by_category(df_to_func, cat, date)
        print(result_js)

        if __name__ == "__main__":

