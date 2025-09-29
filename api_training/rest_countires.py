import pandas as pd
import requests

r = requests.get("https://restcountries.com/v3.1/all?fields=name,region,population,languages")

data = r.json()

df = pd.json_normalize(data)[["name.common", "region", "population", "languages.spa"]]
df = df.rename(columns={"name.common": "country", "languages.spa": "spanish"})

print("QUESTION 1: Top 10 most populated countries")
print(df.sort_values(by="population", ascending=False).head(10))

print('\n',"QUESTION 2: Region with most contries")
big_reg = df["region"].value_counts().idxmax()
print(big_reg, df["region"].value_counts().max())

print('\n',"QUESTION 3: Total of Spanish speaking countries")
print(df["spanish"].count())