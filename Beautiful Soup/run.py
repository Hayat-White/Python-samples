#!/usr/bin/python3.7
from bs4 import BeautifulSoup
import sys

with open("output1.html", "r", encoding="utf-8") as fp:
	html_content = fp.read()

soup = BeautifulSoup(html_content, 'html.parser')


listings = soup.find_all("li", class_="cl-static-search-result")

for listing in listings:
	name = listing.find("div", class_="title").text.strip()
	price_tag = listing.find("div", class_="price")
	price = price_tag.text.strip() if price_tag else "N/A"
	print("Item:",name,"Price:",price)
	print()
total_items = len(listings)
print("Total number of items:",total_items)

