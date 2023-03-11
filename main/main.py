import os
import time
import asyncio
import aiohttp
import pandas as pd
from urllib.parse import urlparse

from webscraper import SeleniumWebScraper
from product_details_page import ProductDetailsPage
from navagation_page import NavigationPage
from products_page import ProductsPage


class Main:
    def __init__(self, is_single_product_scrap, single_product_url=None, max_count=10) -> None:
        self.is_single_product_scrap = is_single_product_scrap
        self.single_product_url = single_product_url
        self.navigation_page_url = 'https://shop.adidas.jp/men/'
        self.max_count = max_count
        self.counter = 0


    def run(self):
        if self.is_single_product_scrap:
            dict_data = self.get_single_product_page_data(self.single_product_url)
            self.write_in_spreadsheet([dict_data])
        else:
            loop = asyncio.get_event_loop()
            list_of_data = loop.run_until_complete(self.extract_multiple_product_page_data())
            dict_list = list(filter(lambda x: isinstance(x, dict), list_of_data))
            self.write_in_spreadsheet(dict_list)


    def get_single_product_page_data(self, url):
        webscraper = SeleniumWebScraper(url)
        cordinate_products = webscraper.cordinate_product_info_scrap(second=3)
        webscraper.load_page(sleep=3)
        webscraper.wait_for_product_deatils_page(second=3)
        page_source = webscraper.get_page_source()
        product_detail_page = ProductDetailsPage(url, page_source, cordinate_products)
        dict_data = product_detail_page.get_product_data()
        return dict_data

    async def get_single_product_page_data_async(self, url):
        webscraper = SeleniumWebScraper(url)
        webscraper.load_page(sleep=1)
        cordinate_products = webscraper.cordinate_product_info_scrap(second=1)
        webscraper.wait_for_product_deatils_page(second=1)
        page_source = webscraper.get_page_source()
        product_detail_page = ProductDetailsPage(url, page_source, cordinate_products)
        dict_data = product_detail_page.get_product_data()
        return dict_data
    
    async def extract_multiple_product_page_data(self):
        product_page_urls = self.extract_max_product_urls()
        print('products urls:', product_page_urls)
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.ensure_future(self.get_single_product_page_data_async(url)) for url in product_page_urls]
            items = await asyncio.gather(*tasks)
            return items
    
    def extract_max_product_urls(self):
        product_page_urls = []
        navigation_urls = self.get_navigation_urls()
        print('navigation_urls:', navigation_urls)
        for url in navigation_urls:
            link = url
            while self.counter < self.max_count:
                product_urls , next_page_url = self.get_product_urls(link)
                product_page_urls = product_page_urls + product_urls
                self.counter += len(product_urls)
                link = next_page_url
            if self.counter >= self.max_count:
                product_page_urls = product_page_urls[:self.max_count]
                break
        return product_page_urls

    
    def get_navigation_urls(self):
        webscraper = SeleniumWebScraper(self.navigation_page_url)
        webscraper.load_page(sleep=0)
        page_source = webscraper.get_page_source()
        navigation_page = NavigationPage(self.navigation_page_url, page_source)
        navigation_urls = navigation_page.scrap_navigation_links()
        return navigation_urls
    
    def get_product_urls(self, url):
        webscraper = SeleniumWebScraper(url)
        webscraper.load_page(sleep=0)
        page_source = webscraper.get_page_source()
        product_page = ProductsPage(url, page_source)
        urls = product_page.scrap_products_urls()
        next_page_link = product_page.scrap_products_next_page_url()
        return urls, next_page_link

    def write_in_spreadsheet(self, dict_data):
        file_path = 'products_scrap_data.xlsx'
        if self.is_file_already_exist(file_path=file_path):
            df = pd.read_excel(file_path)
            new_df = pd.DataFrame(dict_data)
            df = pd.concat([df, new_df], ignore_index=True)
            df.to_excel(file_path, index=False)
        else:
            df = pd.DataFrame(dict_data)
            df.to_excel('products_scrap_data.xlsx', index=False)

    def is_file_already_exist(self, file_path):
        if os.path.exists(file_path):
            return True
        else:
            return False



if __name__ == '__main__':
    while True:
        answer = input("Do you want to scrap single product info? (y/n): ")
        if answer.lower() == 'y':
            while True:
                url = input("Enter a URL(product deatil page): ")
                parsed_url = urlparse(url)
                if parsed_url.scheme and parsed_url.netloc:
                    start_time = time.time()
                    print('start time:', start_time)
                    main = Main(True, url)
                    main.run()
                    end_time = time.time()
                    print('end time:', end_time)
                    execution_time = end_time - start_time
                    print('successfully scrap and save data in spreadsheet')
                    print(f"Execution time: {execution_time:.2f} seconds")
                    break
                else:
                    print("Invalid URL. Please enter a valid URL.")
        elif answer.lower() == 'n':
            while True:
                try:
                    user_input = input("Enter an max count: ")
                    max_count = int(user_input)
                    start_time = time.time()
                    print('start time:', start_time)
                    main = Main(False, max_count=max_count)
                    main.run()
                    end_time = time.time()
                    print('end time:', end_time)
                    execution_time = end_time - start_time
                    print('successfully scrap and save data in spreadsheet')
                    print(f"Execution time: {execution_time:.2f} seconds")
                    break

                except ValueError:
                    print("Error: please enter an integer")

        else:
            print("Invalid input. Please enter 'y' or 'n'.")