# books-to-scrape-data-collection
Python web scraper for collecting book catalog data from Books to Scrape, including pagination, product details, and CSV export.

Project title: Books to Scrape Data Collection

A Python web scraping project that collects book information from Books to Scrape.

Overview

This scraper collects data from the Books to Scrape catalog across all available pages and follows each book's detail page to extract additional information.

The final dataset contains 1,000 books.

Data Collected
Book title
Price
Availability
Rating
Category
Product page URL
Image URL
UPC
Description
Features
Pagination handling
Relative-to-absolute URL conversion with urljoin
Book detail page scraping
HTTP status and request error handling
Tracking of failed pages and failed book requests
CSV export with Pandas
Technologies
Python
Requests
BeautifulSoup
Pandas
Output

The scraper generates:

books.csv

The CSV contains the extracted information for the scraped books.

How to Run

Install the required Python packages:

pip install -r requirements.txt

Then run:

python scraper.py

Notes

This project was created as a practical exercise in Python web scraping, including pagination, URL handling, detail-page extraction, and basic error handling.

