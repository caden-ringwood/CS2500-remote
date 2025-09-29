import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.imdb.com/chart/top/"

headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

titles = []
years = []
ratings = []
votes = []

movies = soup.select("li.ipc-metadata-list-summary-item")

for movie in movies:
    # Title (remove the rank number like "1.")
    raw_title = movie.find("h3").text.strip()
    title = " ".join(raw_title.split(" ")[1:])
    
    # Year → first <span> in cli-title-metadata
    year_tag = movie.select_one("div.cli-title-metadata span.cli-title-metadata-item")
    year = year_tag.text if year_tag else None
    
    # Rating value
    rating_tag = movie.find("span", class_="ipc-rating-star--imdb")
    rating = rating_tag.text.strip() if rating_tag else None
    
    # Votes
    vote_tag = movie.find("span", class_="ipc-rating-star--voteCount")
    vote_count = vote_tag.text.strip("()") if vote_tag else None
    
    titles.append(title)
    years.append(year)
    ratings.append(rating)
    votes.append(vote_count)

df = pd.DataFrame({
    "Title": titles,
    "Year": years,
    "Rating": ratings,
    "Votes": votes
})

print(df.head(10))
