import pandas as pd

from utils import filter_transactions_3_months, filter_transactions_by_category


def spending_by_category(transactions: pd.DataFrame, category: str, datetime) -> pd.DataFrame:
    all_transactions = transactions.to_dict(orient="records")
    transactions_3_months = filter_transactions_3_months(all_transactions, datetime)
    result = filter_transactions_by_category(transactions_3_months, category)
    return result
