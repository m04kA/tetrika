import requests
import bs4
import time
import asyncio
import aiohttp
import string
import logging_conf
from loguru import logger

# Алфовит
alphabet_ru = "АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
alphabet = alphabet_ru + string.ascii_uppercase

result = {}  # Словарь для хранения количества животных по первой букве алфавита.

wikiUrl = "https://ru.wikipedia.org"  # Ссылка на википедию


async def get_page(url: str, session=None):
    """
    Получение страницы с помощью aiohttp через запрос.
    :param url: - ссылка на страницу, содержимое которой хотим получить
    :param session: - сессия для запроса
    :return: - содержимое страницы
    """
    if session is None:
        async with aiohttp.ClientSession() as session:
            logger.info("Request page: " + url)
            async with session.get(url, timeout=10) as response:
                return await response.text()
    else:
        logger.info("Request page: " + url)
        try:
            async with session.get(url, timeout=10) as response:
                return await response.text()
        except aiohttp.client_exceptions.ClientConnectorError:
            await asyncio.sleep(0.1)
            logger.error("Error connection. Restart connection. URL: " + url)
            return await get_page(url, session)

async def get_count_animals_acync(symbol: str) -> str:
    """
    Заполенине глобального словаря количеством животных по определённой букве.
    :param symbol: - Заглавная буква алфавита.
    :return:
    """
    async with aiohttp.ClientSession() as session:
        urlSelected = f"https://ru.wikipedia.org/w/index.php?title=Категория%3AЖивотные_по_алфавиту&from={symbol}"
        while True:
            if urlSelected != f"https://ru.wikipedia.org/w/index.php?title=Категория%3AЖивотные_по_алфавиту&from={symbol}":
                urlSelected = "".join([wikiUrl, urlSelected])  # Собираем ссылку для запроса на следующую страницу.
                logger.debug("Create new url: " + urlSelected + "\nSymbol: " + symbol)
            await asyncio.sleep(0.01)  # Задержка в 0.01 секунды
            html = await get_page(urlSelected, session=session)
            soup = bs4.BeautifulSoup(html, 'html.parser')
            try:
                # Поиск блока с основным содержанием страницы.
                content = soup.find("div", {"id": "mw-pages"}).find_all("div", {"class": "mw-category-group"})
                for el in content:
                    if el.find("h3").text == symbol:  # Проверка на найденный символ.
                        if result.get(symbol, None) is None:  # Создание ключа в словаре если его нет.
                            logger.info("Start work with symbol: " + symbol)
                            result[symbol] = 0
                            print("Start " + symbol)  # Показатель работы программы.
                        result[symbol] += len([i.text for i in el.find_all("li")])
                    else:
                        # Нашли другую букву, значит наша буква уже закончилась.
                        break
                # Поиск ссылки на следующую страницу.
                if url := soup.find("a", string="Следующая страница"):
                    logger.debug(f"Next page for symbol '{symbol}': " + url.get("href"))
                    urlSelected = str(url.get("href"))
                    continue
                else:
                    break
            except Exception as err:
                # Обработка ошибок для понимания причины проблемы.
                # print(f"error\nurl: {urlSelected}\nsymbol: {symbol}\n{err}")
                logger.error(f"error\nurl: {urlSelected}\nsymbol: {symbol}\n{err}")
            # except aiohttp.client_exceptions.ClientConnectorError:
            #     # Перезапуск при ошибке подключения.
            #     logger.error("Error connection. Restart programm. Symbol: " + symbol)
            #     result[symbol] = 0
            #     print("Restart " + symbol)
            #     answ = await get_count_animals_acync(symbol)
            #     return answ
        return f"Finish - {symbol}"  # Окончание работы по определённой букве.


async def main():
    """
    Основная функция для запуска асинхронного приложения.
    :return:
    """
    futures = [get_count_animals_acync(symbol) for symbol in alphabet]  # Создание задач для параллельного выполнения.
    for future in asyncio.as_completed(futures):  # Ожидание завершения всех задач.
        response = await future
        print(response)  # Вывод выполнения задачи.


def print_result(result: dict) -> None:
    """
    Вывод результата выполнения программы.
    :return:
    """
    print("\nРезультат:")
    for key, value in result.items():
        print(f"{key}: {value}")


def main_sync(result: dict) -> dict:
    """
    Основная функция для запуска синхронного приложения.

    Основная идея в том, что мы переходим на первую страницу, парсим, переходим на следующую и так до последней страницы.
    :return:
    """
    urlSelected = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"  # Первоначальная ссылка.
    while True:
        if urlSelected != "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту":
            urlSelected = "".join([wikiUrl, urlSelected])
            logger.debug("Create new url: " + urlSelected)
        time.sleep(0.01)  # Задержка в 0.01 секунды
        logger.info("Request page: " + urlSelected)
        response = requests.get(urlSelected).text  # Получение страницы через запрос.
        soup = bs4.BeautifulSoup(response, 'html.parser')
        # Поиск блока с основным содержанием страницы.
        content = soup.find("div", {"id": "mw-pages"}).find_all("div", {"class": "mw-category-group"})
        for el in content:  # Обрабатываем всё тело страницы.
            if result.get(el.find("h3").text, None) is None:  # Создание ключа в словаре если его нет.
                logger.info("Start work with symbol: " + el.find("h3").text)
                result[el.find("h3").text] = 0
                print("Start " + el.find("h3").text)
            result[el.find("h3").text] += len([i.text for i in el.find_all("li")])
        # Поиск ссылки на следующую страницу.
        if url := soup.find("a", string="Следующая страница"):
            logger.debug(f"Next page for symbol '{el.find('h3').text}': " + url.get("href"))
            urlSelected = str(url.get("href"))
        else:
            logger.info("Finish work with all symbols")
            # Страницы закончились, вывод результата.
            break
    return result


if __name__ == "__main__":
    """
    Вариант решения задачи через асинхронное приложение.
    """
    print("Asyncronous")
    start = time.time()
    ioloop = asyncio.new_event_loop()
    ioloop.run_until_complete(main())
    print(f"Time - {time.time() - start}")
    print("end of asyncronous")
    print_result(result)
    # ioloop.close()
    # ------------------------------------------------------------------------------------------------------------------
    """
    Вариант решения задачи через синхронное приложение.
    """
    result = {}
    print("Syncronous")
    start = time.time()
    main_sync(result)
    print(f"Time - {time.time() - start}")
    print_result(result)
