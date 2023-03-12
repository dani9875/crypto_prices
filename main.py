from bs4 import BeautifulSoup
import requests
import re
import pandas as pd


site = "https://www.coingecko.com/?page="
number_of_pages_to_be_scraped = 116

coin_name = []
price = []
volume_24h = []
market_cap = []

for i in range(number_of_pages_to_be_scraped):
    _page = site + str(i+1)
    req=requests.get(_page)
    content=req.text
    soup=BeautifulSoup(content)

    name_span = soup.find_all("span", {"class": "lg:tw-flex font-bold tw-items-center tw-justify-between"})
    price_td = soup.find_all("td", {"class": "td-price price text-right"})
    volume_24h_td = soup.find_all("td", {"class": "td-liquidity_score lit text-right col-market"})
    market_cap_td = soup.find_all("td", {"class": "td-market_cap cap col-market cap-price text-right"})

    for span in name_span:
        coin_name.append(span.text.strip())

    for span_money in price_td:
        children = span_money.findChildren("div" , recursive=False)
        price.append(children[0].text.strip())

    for span_money in volume_24h_td:
        volume_24h.append(span_money.text.strip())

    for span_money in market_cap_td:
        children = span_money.findChildren("div" , recursive=False)
        market_cap.append(span_money.text.strip())
    
    
df = pd.DataFrame(list(zip(coin_name, price, volume_24h, market_cap)), columns=["Coin name", "Price", "24h volume.", "Mkt cap"])
df.to_csv('data.csv', index=False)