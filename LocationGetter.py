"""
This is the utility code, used for web scraping, writing to spreadsheets.
"""

from typing import Dict, List, Tuple

import requests
from bs4 import BeautifulSoup
import csv
import datetime


# TODO TEST THIS
def get_bar_height(location: str) -> Tuple[Dict, List]:
    ret_dict = {}
    ret_list = []
    url = 'https://www.google.com/search?q='
    div_class = 'cwiwob'
    usual_class = 'QWaAwc'
    now_class = 'VKx1id'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    response = requests.get(url + location, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    bigdiv = soup.find("div", class_="jvCr1e")

    if bigdiv is None:
        return ret_dict, ret_list

    bars = bigdiv.find_all('div', class_=div_class)

    if len(bars) == 0:
        return ret_dict, ret_list

    for a in bars:
        style = a.attrs['style']
        classes = a.attrs['class']
        px = style.split(':')[1]
        px = px[:-3]
        px = round(float(px) / 75 * 100)
        # print(px)
        if len(classes) == 1:
            ret_list.append(px)
            continue
        if usual_class in classes:
            ret_dict['Usual'] = px
            ret_list.append(float(px))
        elif now_class in classes:
            ret_dict['Current'] = px
        else:
            if 'Unknown' in ret_dict:
                ret_dict['Unknwon'] += [px]
            else:
                ret_dict['Unknown'] = [px]
            ret_list.append(px)
    return ret_dict, ret_list


def write_dict(dicl, filename):
    """Precondition: Usual and Current in dict
    """
    # Hour 0-23
    # 0 is monday??
    # Day 0-6
    day = datetime.datetime.today().weekday()
    hour = datetime.datetime.now().hour
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    csve = filename
    file = open(csve, 'a', newline='', encoding='UTF-8')
    writist = csv.writer(file, lineterminator='\n')
    lst = [day, hour, dicl['Usual'], dicl['Current'], date]
    writist.writerow(lst)
    file.close()
