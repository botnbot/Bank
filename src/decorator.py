import functools


def log_result_to_file(file_name=None):
    """
    Декоратор, записывающий результат функции в файл.
    Аргумент функции - путь для сохранения файла.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if file_name is None:
                # Если имя файла не передано, используем имя по умолчанию
                file_name = f"{func.__name__}_result.txt"
            with open(file_name, "w") as file:
                file.write(str(result))
            return result

        return wrapper

    return decorator if file_name is None else decorator(file_name)
