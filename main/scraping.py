import asyncio
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class ProductDetailPage:

    def __init__(self, soup) -> None:
        self.soup = soup

    
    def get_breadcrumb_category(self):
        # print('soup:', self.soup)
        ul = self.soup.find('ul', class_="test-breadcrumb")
        # print('ul', ul)
        if ul:
            lis = ul.find_all('li', recursive=False)
            categories = [str(li.a.get_text()) for li in lis]
            return categories
        return []





async def scrape_url(url):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    response = await loop.run_in_executor(None, requests.get, url, headers)
    # print('response:', response.status_code)
    soup = BeautifulSoup(response.text, 'html.parser')
    product_deatil_page = ProductDetailPage(soup)
    print(product_deatil_page.get_breadcrumb_category())

async def main():
    urls = ['https://shop.adidas.jp/products/H03740/', 
            'https://shop.adidas.jp/products/B75806/', 
            'https://shop.adidas.jp/products/B75807/',
            'https://shop.adidas.jp/products/GW6173/',
            'https://shop.adidas.jp/products/IE9541/',
            'https://shop.adidas.jp/products/FZ6364/',
            'https://shop.adidas.jp/products/FZ6389/',
            'https://shop.adidas.jp/products/GW6173/',
            'https://shop.adidas.jp/products/ID4121/',
            'https://shop.adidas.jp/products/HQ8930/'
        ]
    tasks = []
    for url in urls:
        task = asyncio.create_task(scrape_url(url))
        tasks.append(task)
    await asyncio.gather(*tasks)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())




