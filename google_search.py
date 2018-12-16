import requests
from unidecode import unidecode
from bs4 import BeautifulSoup

# Adapted from http://edmundmartin.com/scraping-google-with-python/

USER_AGENT = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}


def fetch_results(name, location, platform, number_results, language_code):
    search_term = f'"{name}" "{location}" "{platform}"'
    escaped_search_term = search_term.replace(' ', '+')

    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(
        escaped_search_term, number_results, language_code)
    response = requests.get(google_url, headers=USER_AGENT)
    response.raise_for_status()

    return response.text


def parse_results(name, location, platform, html):
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
            else:
                description = ""

            # also check if title includes name and platform!
            simplified_title = unidecode(title.lower())
            name_parts = unidecode(name.lower()).split(" ")
            first_name = name_parts[0]
            last_name = name_parts[-1]
            if not ((first_name in simplified_title and last_name in simplified_title and platform.lower() in simplified_title) or (first_name in description and last_name in description)):
                print(f"**1. rejected! {name}, {platform}, {title}, {link}\n")
                break

            # and that the link isn't just another google search link
            if link.startswith('/search'):
                print(f"**2. rejected! {name}, {platform}, {title}, {link}\n")
                break

            if not f"{platform}.com" in link:
                print(f"**3. rejected! {name}, {platform}, {title}, {link}\n")
                break

            print(f"RESULT WAS APPROVED! {name}, {platform}, {title}, {link}\n")

            if link != '#':
                found_results.append({
                    'title': title,
                    'link': link,
                    'description': description
                })
    return found_results


def fetch_and_parse_results(name, location, platform, number_results):
    html = fetch_results(name, location, platform, number_results, 'en')
    return parse_results(name, location, platform, html)
