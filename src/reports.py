from loader import load_user_settings
from utils import filter_transactions_3_months, filter_transactions_by_category
import pandas as pd
from typing import Optional


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    datetime_str = date
    data = load_user_settings("user_settings.json")
    all_transactions = transactions.to_dict(orient="records")
    transactions_3_months = filter_transactions_3_months(all_transactions, datetime_str)
    result = filter_transactions_by_category(transactions_3_months, category)
    return result
