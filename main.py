from datetime import datetime

import requests
from bs4 import BeautifulSoup
from termcolor import colored


QUIT_CHAR = "q"


def ask_for_input():
    user_input = input(
        "Find out when famous people were born. Enter a name or type q to quit: "
    )
    return user_input


def show_error_message(response):
    if response.status_code == 404:
        print(colored("\nI don't know this person. Try again\n", "red"))
    elif response.status_code == 504:
        print(colored("\nThe system is down\n", "red"))
    else:
        print(
            colored(
                f"\nError, invalid response status code: {response.status_code}\n",
                "red",
            )
        )


def find_birthday(response):
    soup = BeautifulSoup(response.content, features="html.parser")
    table = soup.find("table", class_="infobox")
    if table:
        date_element = table.find("span", class_="bday")
        if date_element:
            return date_element
    return None


def show_birthday(date_element):
    try:
        return datetime.strptime(str(date_element.contents[0]), "%Y-%m-%d").strftime(
            "%d %B %Y"
        )
    except ValueError:
        print(colored("\nFormatting error\n", "red"))


def main():
    while True:
        user_input = ask_for_input()
        if user_input == QUIT_CHAR:
            print("\nBye!")
            break
        else:
            response = requests.get("https://www.wikipedia.org/wiki/" + user_input)
            if response.status_code == 200:
                birthday = find_birthday(response)
                if not birthday:
                    print(colored("\nBirthday date unknown\n", "yellow"))
                else:
                    formatted_date = show_birthday(birthday)
                    if formatted_date:
                        print(
                            colored(
                                f"\n{user_input} was born on {formatted_date}\n", "blue"
                            )
                        )
            else:
                show_error_message(response)


if __name__ == "__main__":
    main()
