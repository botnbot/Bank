from utils import create_response


def main_page(datetime_str: str) -> str:
    # datetime_str = input("Введите дату в формате YYYY-MM-DD HH:MM:SS  ")
    response_json = create_response(datetime_str)

    return response_json
