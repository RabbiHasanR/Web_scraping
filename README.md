# Ecommerce Web Scraper

This project is a web scraper that uses Selenium, Python, BeautifulSoup, and Chromium to extract data from websites. It is designed to help automate the process of collecting data from web pages. My Targeting Website is:

* [https://shop.adidas.jp/men/](https://shop.adidas.jp/men/)  **Porduct Navigate Page**
* [https://shop.adidas.jp/products/HB9386/](https://shop.adidas.jp/products/HB9386/)  **Porduct Details Page**


# Task List

* Scrap total 200-300 products detail page
* Collect Data
* Store in spreadsheat

# Feature

* Collect single product details page data and store in spreadsheat
* Collect multitple products deatils page data and store in spreadsheat
* Collect data concurrently for multiple urls

# Data Collection Topic

* Breadcrumb Category
* Porduct Inforamtion
    * Product Name
    * Product Category Name
    * Product Price
    * Product Available size list
* Product Images Urls
* List of Cordinate Products Information
    * Product Name
    * Product Price
    * Product Page Url
    * Product Image Source
    * Product Number
* Product Description
    * Description Title
    * General Description
    * Itemization Description
* Tale Of Size
* Special Function 
* Review Information
    * Rating
    * Number Of Reviews
    * Recommended Rate
    * Review rating of each items
* List Of User Reviews
    * Date 
    * Rating
    * Review Title
    * Review Description
    * Reviewer ID
* List Of Keywords

# File Structure

* `main/webscraper.py` handle selenium.
* `main/navigation_page.py` scrap [https://shop.adidas.jp/men/](https://shop.adidas.jp/men/)
* `main/products_page.py` scrap list of products detail page links
* `main/util.py` some util method for using collect data.
* `main/product_details_page.py` collect product details page data.
* `main/main.py` run scraper

# Limitations

* When scraping multiple url concurrently it takes too much time.
* If the internet is slow, then clicking doesn't work and the full page doesn't load properly.
* Without open selenium chrome browser sometimes the full page doesn't load properly and clicks don't work.

# Prerequisites

Before running this program, you need to have the following tools and libraries installed:

* Python 3.11.2
* Selenium 4.8.2
* BeautifulSoup 4.11.2
* Chromium 111.0.5563.64
* Pandas 1.5.3
* webdriver-manager 3.8.5

To install the required libraries, run the following commands in your terminal:
```console
    pip install -r requirments.txt  
```

# Running the Program

To run the program, execute the following command in your terminal:
```console
    cd main
    python main.py
    Do you want to scrap single product info? (y/n):
```
If Y:
```console
    Enter a URL(product deatil page):
```
If N:
```console
    Enter an max count:
```

This will launch the web scraper, which will open up a Chromium window and navigate to the specified URL. The program will then use BeautifulSoup to extract data from the page, and Selenium to interact with the web page (e.g. clicking buttons, scrolling webpage etc.). Finally, the data will be saved to a CSV file in the `products_scrap_data.xlsx` file.





