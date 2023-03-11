import requests
from bs4 import BeautifulSoup
import csv
import datetime
from prettytable import PrettyTable

# get symbols from lookup page
url = 'https://finance.yahoo.com/lookup'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

symbols = []
for row in soup.find_all('tr'):
    cols = row.find_all('td')
    if len(cols) > 1:
        symbol = cols[0].text.strip()
        symbols.append(symbol)

# get price from each symbol page
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69'}
base_url = 'https://finance.yahoo.com/quote/'

symbol_prices = {}

for symbol in symbols:
    url = f'{base_url}{symbol}'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    price_tag = soup.find('fin-streamer', {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'})
    if price_tag is not None:
        price = price_tag.text
        symbol_prices[symbol] = price
    else:
        print(f"No price found for symbol {symbol}")


# Create the table
table = PrettyTable()
table.field_names = ["Symbol", "Price"]
for symbol, price in symbol_prices.items():
    table.add_row([symbol, price])

# Print the table with headers and add a string at the end with the date
now = datetime.datetime.now()
date_string = now.strftime("%Y-%m-%d %H:%M:%S")
print(table)
print(f"\nData collected on: {date_string}")

# Save the data to a CSV file with current date in the filename
filename = f"symbol_prices_{now.strftime('%Y-%m-%d_%H-%M-%S')}.csv"
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Symbol", "Price"])
    for symbol, price in symbol_prices.items():
        writer.writerow([symbol, price])
print(f"Data saved to {filename}")
