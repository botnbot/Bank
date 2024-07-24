from utils import create_response
import pandas as pd

def main_page(df: pd.DataFrame, datetime_str: str) -> str:
    # datetime_str = input("Введите дату в формате YYYY-MM-DD HH:MM:SS  ")
    response_json = create_response(df, datetime_str)

    return response_json
