import requests
from bs4 import BeautifulSoup

# Adapted from http://edmundmartin.com/scraping-google-with-python/

USER_AGENT = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}


def fetch_results(search_term, number_results, language_code):
    assert isinstance(search_term, str), 'Search term must be a string'
    assert isinstance(number_results,
                      int), 'Number of results must be an integer'
    escaped_search_term = search_term.replace(' ', '+')

    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(
        escaped_search_term, number_results, language_code)
    response = requests.get(google_url, headers=USER_AGENT)
    response.raise_for_status()

    return response.text


def parse_results(html):
    soup = BeautifulSoup(html, 'lxml')
    found_results = []
    rank = 1
    result_block = soup.find_all('div', attrs={'class': 'g'})
    for result in result_block:
        link = result.find('a', href=True)
        title = result.find('h3')
        description = result.find('span', attrs={'class': 'st'})
        if link and title:
            link = link['href']
            title = title.get_text()
            if description:
                description = description.get_text()
            if link != '#':
                found_results.append({
                    'title': title,
                    'link': link,
                    'description': description
                })
                rank += 1
    return found_results


def fetch_and_parse_results(search_terms, number_results):
    html = fetch_results(search_terms, number_results, 'en')
    return parse_results(html)


if __name__ == '__main__':
    fetch_and_parse_results("Nicholas Passanisi linkedin", 10)
