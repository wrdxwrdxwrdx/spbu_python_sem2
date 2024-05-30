import loguru
import requests
from bs4 import BeautifulSoup
from numpy.compat import unicode


def parse(html: str, n: int, no_first: bool = False) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    if no_first:
        quotes = soup.find_all("div", class_="quote__body", limit=n + 1)[1:]
    else:
        quotes = soup.find_all("div", class_="quote__body", limit=n)

    output = []
    for i in range(len(quotes)):
        quote = ""
        for child in quotes[i].children:
            if unicode(child) != "<br/>" and child.text.strip() != "Комикс по мотивам цитаты":
                quote += child.strip() + "\n"
        output.append(quote)
    return output


async def get_last(n: int) -> list[str]:
    html = requests.get("https://башорг.рф/").text
    return parse(html, n, no_first=True)


async def get_best(n: int) -> list[str]:
    html = requests.get("https://башорг.рф/best/2024").text
    return parse(html, n)


async def get_random(n: int) -> list[str]:
    html = requests.get("https://башорг.рф/random").text
    return parse(html, n)


async def get_info(command: str, n: int = 10) -> str:
    logger = loguru.logger

    if command == "BEST":
        return "\n\n".join(await get_best(n))
    elif command == "LAST":
        return "\n\n".join(await get_last(n))
    elif command == "RANDOM":
        return "\n\n".join(await get_random(n))
    else:
        logger.info(f"Unexpected command: {command}")
        return ""
