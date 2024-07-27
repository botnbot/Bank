import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime
from src.loader import load_user_settings
from src.reports import spending_by_category
from src.services import personal_transfers
from src.utils import convert_xlsx_to_list
from src.views import main_page

# Mock функции для тестов
@patch('src.loader.load_user_settings')
def test_load_user_settings(mock_load_user_settings):
    mock_load_user_settings.return_value = {"path_to_datafile": "data/operations.xlsx"}
    data = load_user_settings("user_settings.json")
    assert data.get("path_to_datafile") == "data/operations.xlsx"

@patch('src.utils.convert_xlsx_to_list')
@patch('pandas.read_excel')
def test_data_loading(mock_read_excel, mock_convert_xlsx_to_list):
    mock_convert_xlsx_to_list.return_value = [{"dummy": "data"}]
    mock_read_excel.return_value = pd.DataFrame({"dummy": ["data"]})

    df_to_func = pd.read_excel("dummy_path.xlsx")
    list_to_func = convert_xlsx_to_list("dummy_path.xlsx")

    assert list_to_func == [{"dummy": "data"}]
    assert df_to_func.shape == (1, 1)

@patch('src.reports.spending_by_category')
def test_spending_by_category(mock_spending_by_category):
    mock_spending_by_category.return_value = {"total": 100}
    cat = "food"
    date = datetime(2024, 7, 27)

    result = spending_by_category(pd.DataFrame(), cat, date)
    assert result == {"total": 100}

@patch('src.services.personal_transfers')
def test_personal_transfers(mock_personal_transfers):
    mock_personal_transfers.return_value = {"transfers": 50}
    date_str = "2024-07-27"

    result = personal_transfers([], date_str)
    assert result == {"transfers": 50}

@patch('src.views.main_page')
def test_main_page(mock_main_page):
    mock_main_page.return_value = {
        "greeting": "Доброе утро",
        "cards": [],
        "top_transactions": [],
        "currency_rates": {}
    }
    date_str = "2024-07-27"

    result = main_page(pd.DataFrame(), date_str)
    expected_result = {
        "greeting": "Доброе утро",
        "cards": [],
        "top_transactions": [],
        "currency_rates": {}
    }
    assert result == expected_result

def test_invalid_date():
    with pytest.raises(ValueError):
        datetime.strptime("invalid-date", "%Y-%m-%d")
