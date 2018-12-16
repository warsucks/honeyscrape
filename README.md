# Honeyscrape
Scripts to scrape for users

## Dependencies
To run locally, you must have python3 installed.

## Run Locally
From project root, run:
`pip install -r requirements.txt`
`PYTHONPATH=. python honeyscrape.py`.

This will write a CSV in the project root called `honeyscrape_amazon_results_{name}.csv` for each woman's name search, which you can open in any software that reads CSV files (e.g., Microsoft Excel, MacOS Numbers).