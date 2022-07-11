def task(array: str) -> int:
    """
    Функция возвращающая первый '0' в строке.
    :param array: - наша строка
    :return: - индекс первого '0' в строке
    """
    return array.find('0')


if __name__ == '__main__':
    print(task("111111111110000000000000000"))
# >> OUT: 11
