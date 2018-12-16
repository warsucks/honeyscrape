import requests
import itertools
from unidecode import unidecode
from bs4 import BeautifulSoup

from names import woman_names, bay_area_city_names

simplified_woman_names = [unidecode(name).lower() for name in woman_names]


def make_request_body(name, state, page_number):
    return {
        'action': "CUSTOM_REFRESH",
        'clientState': {
            'nameOrEmail': name,
            'state': state,
            'fromMonth': "06",
            'fromYear': "2019",
            'toMonth': "12",
            'toYear': "2020"
        },
        'pageNumber': page_number,
        'recordsPerPage': None,
        'sortOrder': "DESCENDING",
        'tableId': "wr-search-result-table"
    }


def get_data(name, state):
    url = 'https://www.amazon.com/wedding/search-mrtable-ajax/ref=wr_search_cont_search'
    resp = requests.post(url, json=make_request_body(name, state, 1))
    text_html = resp.text
    # need to get rid of weirdly placed script tags that cause beautiful soup to not be able
    # to find table elements
    # note: there might be a way to do this with beautiful soup but `extract`
    # when i tried it also extracted all the children (the table elements)
    text_html = text_html.replace('<script type="text/html">', '').replace(
        '</script>', '')
    soup = BeautifulSoup(text_html, 'lxml')
    num_records = int(soup.find(id='recordCount').get_text().strip())
    records = (soup.find(id=f'wr_search_result_record_{n}')
               for n in range(num_records))
    return (parse_record(r) for r in records
            if is_in_city_list(r, bay_area_city_names))


def parse_record(record_soup):
    owner = record_soup.find('td', {'data-column': 'owner'}).get_text().strip()
    partner = record_soup.find('td', {
        'data-column': 'partner'
    }).get_text().strip()
    event_date = record_soup.find('td', {
        'data-column': 'date'
    }).get_text().strip()
    event_location = record_soup.find('td', {
        'data-column': 'eventLocation'
    }).get_text().strip()

    return {
        "owner": owner,
        "partner": partner,
        "date": event_date,
        "location": event_location,
        "owner_has_woman_name": woman_name_in_name(owner),
        "partner_has_woman_name": woman_name_in_name(partner)
    }


def woman_name_in_name(name):
    for w in simplified_woman_names:
        if w in unidecode(name.lower()):
            return True
    return False


def is_in_city_list(record_soup, city_list):
    event_location = record_soup.find('td', {
        'data-column': 'eventLocation'
    }).get_text().strip()
    # match if city name from known list is contained in the name
    # sometimes users enter the location name sorta wrong (this won't work for all of their wrong entries)
    for city in bay_area_city_names:
        if city.lower() in event_location.lower():
            return True
    return False


def get_data_for_all_names():
    for name in simplified_woman_names:
        for d in get_data(name, "CA"):
            yield d


if __name__ == "__main__":
    for d in get_data_for_all_names():
        print(d)
