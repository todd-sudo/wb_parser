from typing import Union


def calculate_percentage_of_prices(
        price_wb: Union[int, float], price_1c: Union[int, float]
) -> Union[int, float]:
    """ Рассчитывает процентное отношение цен
    """
    try:
        percentage = price_1c / price_wb * 100 - 100
        percentage = round(percentage, 2)
    except ZeroDivisionError:
        return 0
    return percentage
