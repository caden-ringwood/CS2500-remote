import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "http://books.toscrape.com/catalogue/"

url = base_url + "page-1.html"
response = requests.get(url)
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "html.parser")

titles = []
prices = []
ratings = []
genres = []

books = soup.find_all("article", class_="product_pod")

for book in books:
    # Title
    title = book.h3.a["title"]
    
    # Price (strip £ and convert to float)
    price = book.find("p", class_="price_color").text.strip()
    price = float(price.replace("£", ""))
    
    # Rating (class looks like 'star-rating Three')
    rating_class = book.p["class"]
    rating = rating_class[1]  # e.g., "Three"
    
    # Genre requires going into the book detail page
    detail_url = base_url + book.h3.a["href"]
    detail_page = requests.get(detail_url)
    detail_page.encoding = "utf-8"
    detail_soup = BeautifulSoup(detail_page.text, "html.parser")
    
    # Breadcrumb nav: [Home > Books > Genre > Title]
    genre = detail_soup.find("ul", class_="breadcrumb").find_all("a")[2].text.strip()
    
    # Append data
    titles.append(title)
    prices.append(price)
    ratings.append(rating)
    genres.append(genre)

# Create DataFrame
df = pd.DataFrame({
    "Title": titles,
    "Price": prices,
    "Rating": ratings,
    "Genre": genres
})

print(df.head())
