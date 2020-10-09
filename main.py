from bs4 import BeautifulSoup
from datetime import datetime
from termcolor import colored
import requests

while True:
    name = input('Find out when famous people were born. Enter a name or type q to quit: ')
    if name != 'q':
        try:
            url = requests.get('https://www.wikipedia.org/wiki/' + name)
            soup = BeautifulSoup(url.content, features='html.parser')
            table = soup.find('table', class_="infobox")
            date = table.find('span', class_="bday")
            date_format = datetime.strptime(date.contents[0], '%Y-%m-%d').strftime('%d %B %Y')
            print(colored('\n{} was born on {}\n'.format(name, date_format), 'blue'))
        except AttributeError:
            print(colored("\nI don't know this person. Try again.\n", 'red'))
    else:
        print('\nBye!')
        break

