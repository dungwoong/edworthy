"""
Just some experimental stuff I was messing around with before writing main.py
"""

import requests
from bs4 import BeautifulSoup

URL = 'https://www.google.com/search?q='
EDWORTHY = 'edworthy+park'
BOWNESS = 'bowness+park'
NOSEHILL = 'nose+hill+park'
PRINCESISLAND = 'prince%27s+island+park'
DIVS = ['D6mXgd', ]


def get_edworthy_mobile():
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup)


def get_edworthy_windows():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup)


def get_edworthy_final(location):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    response = requests.get(URL+location, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    # this is the div that contains all the little divs for the time periods
    bigdiv = soup.find("div", class_="jvCr1e")
    print(bigdiv.contents)
    print(len(bigdiv))
    # I think at this point, we can just get all the individual data stuffs.
    div_class = 'D6mXgd'
    # I think this is the interesting one, with the height.
    div_class2 = 'cwiwob'
    for bar in bigdiv:
        a = bar.find('div', class_=div_class2)
        if a is not None:
            style = a.attrs['style']
            classes = a.attrs['class']
            # list_ = ''.join(style).split(';')
            # list_ = [i.strip() for i in list_]
            # dict_ = dict(i.split(':') for i in list_)
            px = style.split(':')[1]
            print(a)
            print(px[:-3])
            print(classes)
            # very bad code cuz it could easily go wrong but its ok
            # ok so this code finds all the normal cwiwobs, and the one at the current time has a different class.


def get_edworthy_final1(location):
    usual_height = 0
    now_height = 0
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    response = requests.get(URL+location, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    # this is the div that contains all the little divs for the time periods
    bigdiv = soup.find("div", class_="jvCr1e")
    # print(bigdiv.contents)
    # print(len(bigdiv))
    # I think at this point, we can just get all the individual data stuffs.
    # I think this is the interesting one, with the height.
    div_class2 = 'cwiwob'
    usual_class = 'QWaAwc'
    rn_class = 'VKx1id'
    bars = bigdiv.find_all('div', class_=div_class2)
    for a in bars:
        style = a.attrs['style']
        classes = a.attrs['class']
        px = style.split(':')[1]
        px = px[:-3]
        # print(px)
        # print(classes)
        if len(classes) == 1:
            continue
        if usual_class in classes:
            usual_height = float(px)
        if rn_class in classes:
            now_height = float(px)

    print(f"report for {location.replace('+', ' ')}")
    print(f"Usual is {usual_height}, Now it's {now_height}, which is a {round((now_height/usual_height) * 100)}%")


get_edworthy_final1(BOWNESS)
get_edworthy_final1(NOSEHILL)
get_edworthy_final1(EDWORTHY)
get_edworthy_final1(PRINCESISLAND)
