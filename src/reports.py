from loader import load_user_settings
from utils import filter_transactions_3m, filter_transactions_by_category
import pandas as pd
from typing import Optional


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    datetime_str = date
    data = load_user_settings("user_settings.json")
    path_to_datafile = str(data.get("path_to_datafile"))
    df_to_func = pd.read_excel(path_to_datafile)
    all_transactions = df_to_func.to_dict(orient="records")
    transactions_3m = filter_transactions_3m(all_transactions, datetime_str)
    result = filter_transactions_by_category(transactions_3m, category)
    return result
