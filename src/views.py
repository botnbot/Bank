import pandas as pd
from typing import Any

from .utils import create_response


def main_page(df: pd.DataFrame, datetime_str: str) -> Any:
    response_json = create_response(df, datetime_str)

    return response_json
