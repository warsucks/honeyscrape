import csv
import time
import random

from names import woman_names
from amazon_registry import get_data
from google_search import fetch_and_parse_results

platforms = {'linkedin', 'facebook', 'instagram'}
csv_columns = [
    'owner', 'partner', 'date', 'location', 'owner_has_woman_name',
    'partner_has_woman_name', 'owner_linkedin', 'owner_facebook',
    'owner_instagram', 'partner_linkedin', 'partner_facebook',
    'partner_instagram'
]


def add_search_results_to_data(row):
    # Mutates row, adding top results for each social media platform for the women

    # Just always search for both people in the couple
    for role in {'owner', 'partner'}:
        for p in platforms:
            location_results = search_name_location_platform(
                row[role], row['location'], p)

            # try 'bay area' for location too
            bay_area_results = search_name_location_platform(
                row[role], 'bay area', p)

            row[f"{role}_{p}"] = location_results + bay_area_results

    return row


def search_name_location_platform(name, location, platform):
    # Go slow to not get caught scraping, wait 5-10 seconds between google searches
    time.sleep(random.uniform(5, 10))
    return fetch_and_parse_results(name, location, platform, 10)


if __name__ == "__main__":
    woman_names_list= list(woman_names)
    woman_names_list.sort()
    for name in woman_names_list:
        print(f"DOING FOR NAME {name}")
        with open(f'honeyscrape_amazon_results_{name}.csv', 'w') as f:
            w = csv.DictWriter(f, fieldnames=csv_columns)
            w.writeheader()
            for d in get_data(name, "CA"):
                result_dict = add_search_results_to_data(d)
                w.writerow(result_dict)
                print(f"wrote results {result_dict}\n\n\n")
            f.close()
