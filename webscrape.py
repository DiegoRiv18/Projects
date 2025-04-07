import requests
from bs4 import BeautifulSoup
import re
import json
import time
import pandas as pd

# Set up request
headers = {"User-Agent": "Mozilla/5.0"}
cookies = {
    "birthtime": "1004572800",  # corresponds to a valid birthdate (e.g., Jan 1, 1988)
    "lastagecheckage": "1-November-2001" 
}

search_url = "https://store.steampowered.com/search/?filter=topsellers"
search_page = requests.get(search_url, headers=headers, cookies=cookies)
search_soup = BeautifulSoup(search_page.text, "html.parser")

# Find top sellers
game_data = []
results = search_soup.select('a.search_result_row')

for result in results:
    url = result['href'].split('?')[0]
    title = result.select_one('.title').text.strip()

    price_block = result.select_one('.search_price, .search_price_discount_combined')
    if price_block:
        # Extract text and clean it
        price_text = price_block.get_text(separator=' ', strip=True).replace('Free to Play', '$0.00')
        prices = re.findall(r'[\$€£]\d+(?:\.\d{2})?', price_text)
        price = prices[-1] if prices else price_text.strip() or "Unknown"
    else:
        price = "Unknown"


    game_data.append({
        "title": title,
        "url": url,
        "price": price
    })


# For each game, extract the tags
def extract_tags_from_game(url):
    try:
        game_page = requests.get(url, headers=headers, cookies=cookies)
        soup = BeautifulSoup(game_page.text, "html.parser")
        for script in soup.find_all("script"):
            if "InitAppTagModal" in script.text:
                match = re.search(r'InitAppTagModal\(\s*\d+,\s*(\[\{.*?\}\])', script.text)
                if match:
                    tag_data_json = match.group(1)
                    tag_data = json.loads(tag_data_json)
                    return [tag["name"] for tag in tag_data]
    except Exception as e:
        print(f"Error processing {url}: {e}")
    return []

# Collect tags for the top games
topsellers_data = []

for game in game_data[:50]:  # Limit to top 10
    print(f"Processing {game['title']} - {game['url']}")
    tags = extract_tags_from_game(game["url"])
    topsellers_data.append({
        "title": game["title"],
        "url": game["url"],
        "price": game["price"],
        "tags": tags
    })
    time.sleep(1)


# 5. Optional: Convert to DataFrame
df = pd.DataFrame(topsellers_data)
print(df)
