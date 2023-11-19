#  Written by Vladislav Glinkin

import requests
import json
import os
from bs4 import BeautifulSoup


def main():
    parsing('https://www.afisha.ru/msk/theatre/theatre_list/')
    print('Parsing done')


def parsing(url):
    print('Parsing in process...')

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    theaters_names = soup.find_all('a',  class_='CjnHd y8A5E MnbCM')

    for theater_name in theaters_names:

        theater_url = theater_name.get('href')
        theater_url = f'https://www.afisha.ru{theater_url}'
        response = requests.get(theater_url)
        soup = BeautifulSoup(response.text, 'lxml')
        spectacles = soup.find_all('a', class_="CjnHd y8A5E nbCNS yknrM")

        for spectacle in spectacles:

            #  Initializing the dictionary and lists for storing data
            information = {}
            actors_in_spectacle = list()
            director = list()
            spectacles_dates = list()

            spectacle_url = spectacle.get('href')
            spectacle_url = f'https://www.afisha.ru{spectacle_url}'
            response = requests.get(spectacle_url)
            soup = BeautifulSoup(response.text, 'lxml')
            actors = soup.find_all('a', class_="CjnHd y8A5E QAXd5")

            #  We go through each person from the cast and divide the cast into two groups (actor/director)
            for actor in actors:
                if actor.contents[2].text == 'Режиссёр':
                    director.append(actor.contents[1].text)
                else:
                    actors_in_spectacle.append(actor.contents[1].text)
            director = list(set(director))
            actors_in_spectacle = list(set(actors_in_spectacle))

            dates = soup.find_all('time', class_='D6YRu')
            for date in dates:
                spectacles_dates.append(date.text)

            #  Initialize the keys for the dictionary and set the corresponding values
            information['spectacle_name'] = spectacle.text
            information['spectacle_url'] = spectacle_url
            information['theater_name'] = theater_name.text
            information['theater_url'] = theater_url
            information['director'] = director
            information['actors'] = actors_in_spectacle
            information['dates'] = spectacles_dates

            if os.listdir(path='.').count('spectacles') == 0:
                os.mkdir('spectacles')

            #  Outputting the dictionary to a json file
            #  Loop through '/' and replace with '|' to avoid error
            #  [Errno 2] No such file or directory (Unformatted string doesn't work(r-type))
            filename = spectacle.text.replace('/', '|', spectacle.text.count('/'))
            file = open(f'spectacles/{filename}', mode='w')
            json.dump(information, file, indent=4, ensure_ascii=False)

            print(f'{spectacle.text} - DONE')


main()
