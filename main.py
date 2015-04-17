import requests
from bs4 import BeautifulSoup
import re
import time

def get_page(urlLink):
    page = requests.get(urlLink)
    return page


# return BeautifulSoup(page.text)

def get_number(adId):
    headers = {'X-Requested-With': 'XMLHttpRequest'}
    number = requests.get('http://kolesa.kz/ajax/show-advert-phones/?id=' + adId, headers=headers)
    return number.text

def parse_html(html):
    return BeautifulSoup(html)

def get_car_list(html):
    cars_names = []
    tree = parse_html(html)
    cars = tree.select(".sky-main #main-container .clearfix #content-left .cars-marks .links .clearfix.cars-marks-popular ul li a")
    for car in cars:
        cars_names.append(car['href'])
    return cars_names



def get_page_count(html):
    page = html
    without_unic = remove_unicode(page)
    span_re = re.compile('<td class=\"buttons\".*?>(.+?)</td>')
    spans = span_re.search(without_unic).group()
    parsed_spans = parse_html(spans)
    last_page = parsed_spans.select('span a')[-1].text
    return str(last_page)

def remove_unicode(html):
    without_unic_re = re.compile('([^\x00-\x7F]|\\n)+')
    without_unic = without_unic_re.sub('', html)
    return without_unic

def get_ids(page):
    ids = []
    without_unic = remove_unicode(page)

    a_re = re.compile('<section id=\"content-left\".*?>(.+?)</section>')
    sections = a_re.search(without_unic).group()
    tree = BeautifulSoup(sections)
    aS = tree.select('.good .descr .in .header-search a')

    for a in aS:
        href = a['href']
        id = href.split('/')[-1]
        number = str(remove_unicode(get_number(id)))
        ids.append((id, number))
    print(ids)
    return ids


def run():
    url = 'http://kolesa.kz/cars/'
    ids = []
    i = 2
    t = requests.get(url)
    count = get_page_count(t.text)
    ids.append(get_ids(t.text))
    while i<count:
        t_url = url+"?page="+str(i)
        print(t_url)
        t = requests.get(t_url)
        count = get_page_count(t.text)
        ids.append(get_ids(t.text))
        i+=1
        time.sleep(1)

if __name__ == "__main__":
    run()