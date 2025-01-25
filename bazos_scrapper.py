from requests import get, Response
from bs4 import BeautifulSoup
from sys import argv
from re import match


def exception_controller(error) -> str:
    """
    :param error: Type of error occurred
    :return: Modified error message
    """
    exceptions = {
        RuntimeError: "Connection to server run out!",
        TimeoutError: "Connection to server run out!",
        ConnectionAbortedError: "Connection aborted by server!",
        ConnectionError: "An unexpected error occurred!",
        ConnectionResetError: "Connection reset!",
        ConnectionRefusedError: "Connection refused by error!",
        BrokenPipeError: "Pipe was broken!"
    }

    return exceptions[error]


def get_response(url: str) -> Response | None:
    """
    :param url: URL address of website
    :return: received response object from website
    """
    try:
        response: Response = get(url)
        return response
    except Exception as error:
        print(exception_controller(error))
        return


def catch_title(content: BeautifulSoup) -> str:
    """
    :param content: content ("source code") of website
    :return: Title of the product from website
    """
    title: str = content.find(class_="nadpisdetail").text
    return title


def catch_date(content: BeautifulSoup) -> str:
    """
    :param content: Content ("source code") of website
    :return: Last date of change from website
    """
    date: str = content.find(class_="velikost10").text
    start: int = date.find("[") + 1
    end: int = date.find("]")
    return date[start:end]


def catch_price(content: BeautifulSoup) -> str:
    """
    :param content: Content ("source code") of website
    :return: Price of product from website
    """
    price_class: str = content.find(class_="listadvlevo").text
    price_position: int = price_class.index("Cena:  ") + 7

    price: str = price_class[price_position:]
    price = price[0:price.index("€") + 1]
    return price


def catch_description(content: BeautifulSoup) -> str:
    """
    :param content: Content ("source code") of user website
    :return: Description of product from website
    """
    description_class: str = content.find(class_="popisdetail").text
    return description_class


def format_description(description: str) -> None:
    """
    :param description: Description of product from website
    :return: Formatted version of description where every line has maximum of
    80 characters
    """
    for i in range(0, len(description), 80):
        print(description[i:i+80])


def is_valid_url(url: str) -> bool:
    """
    :param url: URL from user
    :return: Returns if URL address of website is valid
    """
    valid_format: str = r"^https:\/\/\w*\.bazos\.sk.*$"
    if not match(valid_format, url):  # In current version we only accept bazos
        return False
    if len(url) == 0:
        return False
    return True


def print_info(title: str, price: str, date: str, description: str) -> None:
    """
    :param title: Title of product
    :param price: Price of product
    :param date: Date of last change of product
    :param description: Description of product
    :return Formatted version of informations of product:
    """
    print(f"Title: {title}")
    print(f"Price: {price}")
    print(f"Date: {date}")
    print(f"Description:\n{description}")


def main() -> None:
    if len(argv) != 2:
        print("Wrong number of arguments. Usage:"
               "python3 bazos_scrapper.py <URL>")
        return

    url: str = argv[1]  # Program takes URL as first argument
    if not is_valid_url(url):
        print("Invalid URL!")
        return

    response: Response = get_response(url)
    if response.status_code != 200:
        print(f"Failed to retrieve page. Status code {response.status_code}!")
        return

    # Extracting Data
    content: BeautifulSoup = BeautifulSoup(response.text, "html.parser")

    try:
        title: str = catch_title(content)
        price: str = catch_price(content)
        date: str = catch_date(content)
        description: str = catch_description(content)
    except Exception:
        print("Invalid URL!")
        return

    print_info(title, price, date, description)


if __name__ == "__main__":
    main()
