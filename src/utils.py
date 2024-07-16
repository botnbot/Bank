from typing import List
import pandas as pd
from pathlib import Path


def convert_xlsx_to_list(file_name: str) -> List[dict]:
    transactions = []
    try:
        if not Path(file_name).is_file():
            raise FileNotFoundError(f"Файл '{file_name}' не найден.")

        excel_df = pd.read_excel(file_name)
        transactions = excel_df.to_dict(orient="records")

    except ValueError as e:
        print(type((e)))
    except Exception as e:
        print(f"Произошла ошибка при чтении файла '{file_name}': {str(e)}")

    return transactions


if __name__ == "__main__":
    print(convert_xlsx_to_list('data/operations10.xlsx'))