import asyncio
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class ProductDetailPage:

    def __init__(self, soup, url) -> None:
        self.soup = soup
        self.url = url

    
    def get_breadcrumb_category(self):
        ul = self.soup.find('ul', class_="test-breadcrumb")
        if ul:
            lis = ul.find_all('li', recursive=False)
            categories = [str(li.a.get_text()) for li in lis]
            return categories
        return []
    
    def get_product_images_urls(self):
        ul = self.soup.find('ul', class_="slider-list test-slider-list")
        if ul:
            img_tags = ul.find_all('img')
            images_urls = [ requests.compat.urljoin(self.url, img_tag.get('src')) for img_tag in img_tags]
            return images_urls
        return []
    
    def get_product_info(self):
        div = self.soup.find('div', class_="articlePurchaseBox css-gxzada")
        if div:
            category_name = str(div.find('span', class_="categoryName test-categoryName").get_text())
            product_name = str(div.find('h1', class_="itemTitle test-itemTitle").get_text())
            product_price = str(div.find('span', class_="price-value test-price-value").get_text())
            buttons = div.find_all('button', class_="sizeSelectorListItemButton")
            available_sizes = [str(button.get_text()) for button in buttons]
            # sense_of_the_size = 
            return {'category_name': category_name, 'product_name': product_name, 'product_price': product_price, 'available_sizes': available_sizes}
        return {}
    
    # need to use selenium to click div and show info conatiner div then extract
    def get_cordinate_product_info(self):
        div = self.soup.find('div', class_="test-coordinate_item_container")
        if div:
            product_name = div.find('span', class_="title")
            product_page_src = div.find('a', class_="test-link_a")
            product_number = product_page_src.split("/")[-1]
            product_price = div.find('span', class_="price-value test-price-salePrice-value")
            product_page_url = requests.compat.urljoin(self.url, product_page_src) 
            product_image_url = requests.compat.urljoin(self.url, div.find('img', class_="coordinate_item_image test-img").get('src')) 
            return {
                'product_name': product_name,
                'product_price': product_price,
                'product_page_url': product_page_url,
                'product_image_url': product_image_url,
                'product_number': product_number
            }
        return {}
    
    def get_description(self):
        pass

    def get_size_chart(self):
        pass

    def get_spcial_function(self):
        pass

    def get_product_review_info(self):
        pass

    def get_rating_of_each_item(self):
        pass

    def get_users_reviews(self):
        pass

    def get_keywords(self):
        pass
    
    def get_all_data(self):
        data = {}
        data['breadcrumb_category'] = self.get_breadcrumb_category()
        data['product_images_urls'] = self.get_product_images_urls()
        data['product_info'] = self.get_product_info()
        # data['cordinate_product_info'] = self.get_cordinate_product_info()

        return data






async def scrape_url(url):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    response = await loop.run_in_executor(None, requests.get, url, headers)
    # print('response:', response.status_code)
    soup = BeautifulSoup(response.text, 'html.parser')
    product_deatil_page = ProductDetailPage(soup, url)
    print(product_deatil_page.get_all_data())

async def main():
    urls = [
            # 'https://shop.adidas.jp/products/H03740/', 
            'https://shop.adidas.jp/products/HB9386/',
            # 'https://shop.adidas.jp/products/B75806/', 
            # 'https://shop.adidas.jp/products/B75807/',
            # 'https://shop.adidas.jp/products/GW6173/',
            # 'https://shop.adidas.jp/products/IE9541/',
            # 'https://shop.adidas.jp/products/FZ6364/',
            # 'https://shop.adidas.jp/products/FZ6389/',
            # 'https://shop.adidas.jp/products/GW6173/',
            # 'https://shop.adidas.jp/products/ID4121/',
            # 'https://shop.adidas.jp/products/HQ8930/'
        ]
    tasks = []
    for url in urls:
        task = asyncio.create_task(scrape_url(url))
        tasks.append(task)
    await asyncio.gather(*tasks)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())




