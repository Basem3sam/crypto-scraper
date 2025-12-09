from bs4 import BeautifulSoup
import requests

# Simple get request and get the page HTML
response = requests.get("https://coinmarketcap.com/")
soup = BeautifulSoup(response.text, 'html.parser')

# Find all table rows
rows = soup.find_all('tr')

cryptos = []

# Extract crypto data from each row
for row in rows:
  rank_tag = row.find('p', class_='sc-71024e3e-0')
  name_tag = row.find('p', class_='sc-65e7f566-0')
  symbol_tag = row.find('p', class_='coin-item-symbol')
  price_tag = row.find('span', string=lambda text: text and '$' in text)
  
  if name_tag or symbol_tag:
    rank = rank_tag.get_text(strip=True) if rank_tag else "NONE"
    name = name_tag.get_text(strip=True) if name_tag else "NONE"
    symbol = symbol_tag.get_text(strip=True) if symbol_tag else "NONE"
    price = price_tag.get_text(strip=True) if price_tag else "NONE"
    
    if name != "NONE" or symbol != "NONE":
      cryptos.append({
        'rank': rank,
        'name': name,
        'symbol': symbol,
        'price': price
      })

# Print table
if cryptos:
  print(f"{'Rank':<6} {'Name':<20} {'Symbol':<10} {'Price':<15}")
  print("=" * 60)

  for crypto in cryptos:
    # Shorten long names for better table alignment
    if len(crypto['name']) > 20:
      name = crypto['name'][:17] + "..."
    else:
      name = crypto['name']
    
    print(f"{crypto['rank']:<6} {name:<20} {crypto['symbol']:<10} {crypto['price']:<15}")
  
print(f"\nSuccessfully scraped {len(cryptos)} cryptocurrencies!")