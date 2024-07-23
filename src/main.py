from reports import spending_by_category
from views import main_page
from services import personal_transfers
import pandas as pd
print(
    """Выберите категорию для отображения
        1 Главная страница
        2 Сервис фильтрации по переводам (физическим лицам)
        3 Отчет по категории трат"""
)
menu = ""
while menu not in ("1", "2", "3"):
    menu = input("Введите номер \n")
    if menu not in ("1", "2", "3"):
        print("Некорректный ввод.Введите 1, 2, или 3. \n")
    if menu == "1":
        print("Главная страница")
        print(main_page())
    elif menu == "2":
        print("Выбран сервис фильтрации (переводы физическим лицам")
        print(personal_transfers())
    elif menu == "3":
        print(" Выбран очет по категории трат")

        df_to_func = pd.read_excel('data/operations.xlsx')   #условность, т.к. DataFrame взять негде

        cat = input("Введите категорию")
        date = input("Введите  дату для отчета в формате YYYY-MM-DD HH:MM:SS  ")
        print(spending_by_category(df_to_func, cat, date))
