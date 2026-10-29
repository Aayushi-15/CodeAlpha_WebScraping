import requests
import pandas as pd
from bs4 import BeautifulSoup

# Public demo website
url = "https://books.toscrape.com/"

# Request the website
response = requests.get(
    url,
    timeout=20,
    headers={"User-Agent": "Mozilla/5.0"}
)

# Check whether the request succeeded
response.raise_for_status()

# Parse the HTML page
soup = BeautifulSoup(response.text, "html.parser")

# Extract book information
books = []

for book in soup.select("article.product_pod"):
    title_tag = book.select_one("h3 a")
    price_tag = book.select_one(".price_color")
    stock_tag = book.select_one(".availability")

    books.append({
        "Title": title_tag["title"].strip(),
        "Price": price_tag.get_text(strip=True),
        "Availability": stock_tag.get_text(" ", strip=True)
    })

# Convert data into a DataFrame
df = pd.DataFrame(books)

# Save data to a CSV file
df.to_csv("books_data.csv", index=False, encoding="utf-8-sig")

print("Web scraping completed successfully!")
print(f"Total books collected: {len(df)}")
print(df.head(10).to_string(index=False))
print("\nData saved in books_data.csv")