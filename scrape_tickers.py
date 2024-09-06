import requests
from bs4 import BeautifulSoup

# URL to scrape
url = "https://stockanalysis.com/stocks/"

# Fetch the content of the webpage
response = requests.get(url)
if response.status_code != 200:
    print(f"Failed to fetch the webpage. Status code: {response.status_code}")
    exit()

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Dictionary to store company-to-ticker mapping
COMPANY_TO_TICKER_MAP = {}

# Find the table or container that has the data (for this case, assuming it's in 'a' tags)
for link in soup.find_all('a', href=True):
    # Some links might not be valid tickers, so filter out invalid ones
    if link['href'].startswith('/stocks/') and len(link.text.split()) > 1:
        ticker_symbol = link['href'].split('/')[-1].upper()  # Extract ticker from href
        company_name = link.text.lower()  # Convert company name to lowercase
        COMPANY_TO_TICKER_MAP[company_name] = ticker_symbol

# Check some sample data
print(f"Extracted {len(COMPANY_TO_TICKER_MAP)} tickers.")
print({k: COMPANY_TO_TICKER_MAP[k] for k in list(COMPANY_TO_TICKER_MAP)[:10]})  # Print first 10 entries

# Optionally, write the result to a Python file to be imported later
with open("company_ticker_map.py", "w") as file:
    file.write("COMPANY_TO_TICKER_MAP = {\n")
    for company, ticker in COMPANY_TO_TICKER_MAP.items():
        file.write(f"    '{company}': '{ticker}',\n")
    file.write("}\n")
