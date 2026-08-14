import pandas as pd
import requests
from bs4 import BeautifulSoup
from pprint import pprint

from urllib.parse import urljoin

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/137.0 Safari/537.36)"   
}

page = 1
data = []
failed_books = []
failed_pages = []

rating_map = {
        "One":1,
        "Two":2,
        "Three":3,
        "Four":4,
        "Five":5 
    }


while True:

    if page == 1:
        url = "https://books.toscrape.com/index.html"
    else:
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"

    print(f"\n ==== Scraping page {page} ===")
    print("catalog",url)

    try:
        r = requests.get(url, headers=headers, timeout =10)
        print("status:", r.status_code)
        r.raise_for_status()

    except requests.exceptions.RequestException as e:

        if r.status_code == 404:
            print(f"No more pages. stopped at page {page -1}.")
            break

        failed_pages.append({
            "page": page,
            "url": url,
            "error": str(e)
        })
        break

    r.encoding = "utf-8"
    soup = BeautifulSoup(r.content, "html.parser")
    books = soup.select("article.product_pod")

    if not books:
        break

    for book in books:

        product_info = {}

        title = book.select_one("h3 a")["title"]
        price = book.select_one(".price_color").get_text(strip=True)
        availability = book.select_one(".instock.availability").get_text(strip=True)

        rating_tag = book.select_one(".star-rating")
        if rating_tag:
            rating_text = rating_tag["class"][1]
            rating = rating_map.get(rating_text)
        else:
            rating = None

        href = book.h3.a["href"]
        book_url = urljoin(url, href)


        print("book url:", book_url)

        try:
            response = requests.get(book_url, headers=headers, timeout =10)
            print("detail status:", response.status_code)
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            failed_books.append({
                "title": title,
                "url": book_url,
                "error": str(e)
            })
            continue

        response.encoding = "utf-8"
        detail_soup = BeautifulSoup(response.text, "html.parser")

        breadcrumb = detail_soup.select("ul.breadcrumb li a")
        if len(breadcrumb) > 2:
            category = breadcrumb[2].get_text(strip=True)
        else:
            category = None
        
        product_page_url= urljoin(url,book.div.a["href"])
        img_url = urljoin(url, book.div.a.img["src"])

        table = detail_soup.select_one(".table")
        rows =  table.find_all("tr")
        for row in rows:
            key = row.find("th").get_text(strip=True)
            value = row.find("td").get_text(strip=True)
            product_info[key] = value

        upc = product_info["UPC"]
        description_tag = detail_soup.select_one("#product_description + p")
        if description_tag:
            description = description_tag.get_text(strip=True)
        else:
            description = None

        data.append({
            "title":title,
            "price":price,
            "availability":availability,
            "rating":rating,
            "category":category,
            "product page url":product_page_url,
            "img url":img_url,
            "UPC":upc,
            "description":description
        })

    page += 1

print("Failed pages:")
pprint(failed_pages)

print("\nFailed books:")
pprint(failed_books)

print(f"\nTotal books scraped: {len(data)}")
print(f"Failed pages: {len(failed_pages)}")
print(f"Failed books: {len(failed_books)}")

df=pd.DataFrame(data)
print(df)

df.to_csv("books.csv", index=False, encoding="utf-8-sig")