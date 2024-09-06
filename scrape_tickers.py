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

# Find the table or container that has the data (inspect the page source to find the correct tag and class)
# Assuming companies are in 'tr' tags with 'td' tags for company and ticker details
table = soup.find('table')  # Look for the main table

# Loop through all rows in the table
for row in table.find_all('tr')[1:]:  # Skipping the header
    columns = row.find_all('td')
    
    if len(columns) >= 2:
        company_name = columns[1].text.strip().lower()  # Column with company name
        ticker_symbol = columns[0].text.strip().upper()  # Column with ticker symbol
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
