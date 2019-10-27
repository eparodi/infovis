from bs4 import BeautifulSoup
from categories import CATEGORIES

import sys
import pandas as pd
import requests

cookies = {
    "sessionid": sys.argv[1],
    "wants_mature_content": "1",
    "birthtime": "786945601",
}

def make_request(appid):
    response = requests.get(
        'https://store.steampowered.com/app/{appid}'.format(appid=appid), cookies=cookies)
    if response.url == 'https://store.steampowered.com/':
        return None
    return response.text

def get_main_genre(soup):
    gs = soup.find_all("a", class_="app_tag")
    for g in gs:
        genre = g.get_text().strip('\r').strip(
            '\n').strip('\t').strip(' ')
        if genre in CATEGORIES:
            return genre
    return None

def get_price(soup):
    DATA_PRICE = "data-price-final"
    game_purchase_action = soup.find(class_="game_purchase_action")
    if not game_purchase_action:
        return 0
    price_div = game_purchase_action.find(class_="price")
    if price_div and DATA_PRICE in price_div.attrs:
        return float(price_div[DATA_PRICE]) / 100
    return 0

def is_multiplayer(soup):
    multiplayer = soup.find(id="category_block").find(
        text="Multi-player")
    return True if multiplayer else False

def get_review(soup):
    game_review_summary = soup.find(class_="game_review_summary")
    result = game_review_summary.get_text()
    return None if 'review' in result else result


errors = []

def parse_page(text, row):
    soup = BeautifulSoup(text, 'html.parser')
    try:
        row["genre"] = get_main_genre(soup)
        row["reviews"] = get_review(soup)
        row["is_multiplayer"] = is_multiplayer(soup)
        row["price"] = get_price(soup)
    except:
        errors.append(row["appid"])

def apply_to_row(r):
    html_page = make_request(r["appid"])
    if html_page:
        parse_page(html_page, r)
    else:
        errors.append(r["appid"])
    return r

df = pd.read_csv('steam_games.csv')
df["is_multiplayer"] = None
df["genre"] = None
df["price"] = None
df["reviews"] = None
df = df.apply(apply_to_row, axis=1)

print(errors)
df.to_csv('steam_games_decorated.csv', sep='\t', encoding='utf-8', index=False)
