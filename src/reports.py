import json
from datetime import datetime, timedelta

import pandas as pd
from src.utils import filter_transactions_by_category


def spending_by_category(transactions: pd.DataFrame, category: str, current_datetime: datetime) -> str:
    '''
    Функция, возвращающая транзакции за 3 месяца по определенной категории.
    '''
    all_transactions = transactions.to_dict(orient="records")
    # Определяем дату 3 месяца назад
    three_months_ago = current_datetime - timedelta(days=90)
    print(f"Начало отсчета периода: {three_months_ago}")
    print(f"Конец отсчета периода: {current_datetime}")

    transactions_3_months = []
    for transaction in all_transactions:
        trxn_date_str = transaction.get("Дата операции")
        if trxn_date_str:
            try:
                # Преобразуем строку с датой в объект datetime
                transaction_date = datetime.strptime(trxn_date_str, "%d.%m.%Y %H:%M:%S")
                # Проверяем, попадает ли дата транзакции в нужный диапазон
                if three_months_ago <= transaction_date <= current_datetime:
                    transactions_3_months.append(transaction)
                    # print(transactions_3_months['Дата операции'])
            except ValueError as e:
                print(f"Ошибка преобразования даты: {e}")
    if not transactions_3_months:
                return json.dumps([], ensure_ascii=False, indent=4)

            # Фильтруем транзакции по категории
    result = filter_transactions_by_category(transactions_3_months, category)
    if  result.empty:
        list_of_dicts = []

    else:
        list_of_dicts = result.to_dict(orient='records')

    result_json = json.dumps(list_of_dicts, ensure_ascii=False, indent=4)
    return result_json
