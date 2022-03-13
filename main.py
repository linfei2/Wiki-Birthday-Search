from datetime import datetime

import requests
from bs4 import BeautifulSoup
from termcolor import colored


def ask_for_input():
    user_input = input(
        "Find out when famous people were born. Enter a name or type q to quit: "
    )
    return user_input


def show_error_message(response):
    if response.status_code == 404:
        print(colored("\nI don't know this person. Try again.\n", "red"))
    elif response.status_code == 504:
        print(colored("\nThe system is down.\n", "red"))
    else:
        print(colored("\nUnknown error.\n", "red"))


def main():
    while True:
        user_input = ask_for_input()
        if user_input != "q":
            response = requests.get("https://www.wikipedia.org/wiki/" + user_input)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, features="html.parser")
                try:
                    table = soup.find("table", class_="infobox")
                    date_element = table.find("span", class_="bday")
                    formatted_date = datetime.strptime(
                        str(date_element.contents[0]), "%Y-%m-%d"
                    ).strftime("%d %B %Y")
                    print(
                        colored(
                            f"\n{user_input} was born on {formatted_date}\n", "blue"
                        )
                    )
                except AttributeError:
                    print(colored("\nBirthday date unknown.\n", "yellow"))
            else:
                show_error_message(response)
        else:
            print("\nBye!")
            break


if __name__ == "__main__":
    main()
