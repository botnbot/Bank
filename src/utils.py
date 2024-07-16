from typing import List

import pandas as pd


def convert_xlsx_to_list(file_name: str) -> List[dict]:
    excel_df = pd.read_excel(file_name)
    transactions = excel_df.to_dict(orient="records")
    return transactions

if __name__ == "__main__":
    print(convert_xlsx_to_list('data/operations10.xlsx'))