import asyncio
import requests
from requests_html import HTMLSession, AsyncHTMLSession
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


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
    
    def get_cordinate_product_info(self):
        div = self.soup.find('div', class_="test-coordinate_item_container")
        if div:
            product_name = str(div.find('span', class_="title").get_text())
            product_page_src = str(div.find('a', class_="test-link_a").get('href'))
            product_number = str(product_page_src).split("/")[-2]
            product_price = str(div.find('span', class_="price-value test-price-salePrice-value").get_text())
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
        div = self.soup.find('div', class_="js-componentsTabTarget js-articlePromotion add-close css-62zuw8")
        if div:
            description_title = str(div.find('h4', class_="heading itemFeature test-commentItem-subheading").get_text())
            general_description = str(div.find('div', class_="commentItem-mainText test-commentItem-mainText").get_text())
            lis = div.find_all('li', class_="articleFeaturesItem")
            general_itemization_description = [str(li.get_text()) for li in lis]

            return {
                'description_title': description_title,
                'general_description': general_description,
                'general_itemization_description': general_itemization_description
            }
        return {}

    def get_size_chart(self):
        div = self.soup.find('div', class_="sizeChart test-sizeChart css-l7ym9o")
        if div:
            tables = div.find_all('table', class_="sizeChartTable")

            items_table = tables[0]
            items_table_ths = items_table.find_all('th', class_="sizeChartTHeaderCell test-combined_table_header")
            blank_th = items_table_ths.pop(0)

            items_value_table = tables[1]
            items_value_trs = items_value_table.find_all('tr', class_="sizeChartTRow")
            size_names_tr = items_value_trs.pop(0)
            size_names_span = size_names_tr.find_all('span')
            size_names = [str(span.get_text()) for span in size_names_span]
            
            size_chart = {}
            count = 0
            while count < len(items_table_ths) and count < len(items_value_trs):
                value = str(items_table_ths[count].get_text())
                values_span = items_value_trs[count].find_all('span')
                values = [str(span.get_text()) for span in values_span]
                size_chart[value] = dict(zip(size_names, values))

                count += 1
            return size_chart
        return {}
        
        

    def get_special_function(self):
        pass

    def get_product_review_info(self):
        div = self.soup.find('div', class_="BVRRQuickTakeCustomWrapper")
        if div:
            rating = str(div.find('span', class_="BVRRNumber BVRRRatingNumber").get_text())
            number_of_review = str(div.find('span', class_="BVRRNumber BVRRBuyAgainTotal").get_text())
            percentage = str(div.find('span', class_="BVRRBuyAgainPercentage").get_text())
            images = div.find_all('img', class_="BVImgOrSprite")
            items_sence = [img.get('title') for img in images]

            return {
                'rating': rating,
                'number_of_review': number_of_review,
                'percentage': percentage,
                'items_sence': items_sence
            }
        return {}

    def get_users_reviews(self):
        div = self.soup.find('div', {"id": "BVRRDisplayContentBodyID"})
        if div:
            all_review_divs = div.find_all('div', class_="BVRRContentReview")
            user_reviews = []
            for review_div in all_review_divs:
                rating = str(review_div.find('span', class_="BVRRNumber BVRRRatingNumber").get_text())
                date = str(review_div.find('span', class_="BVRRValue BVRRReviewDate").get_text())
                title = str(review_div.find('span', class_="BVRRValue BVRRReviewTitle").get_text())
                description = str(review_div.find('span', class_="BVRRReviewText").get_text())
                reviewer_id = str(review_div.find('span', class_="BVRRNickname").get_text())

                user_review = {
                    'rating': rating,
                    'date': date,
                    'title': title,
                    'description': description,
                    'reviewer_id': reviewer_id
                }

                user_reviews.append(user_review)
            return user_reviews
        return []


    def get_keywords(self):
        div = self.soup.find('div', class_="test-category_link null css-vxqsdw")
        if div:
            all_a = div.find_all('a', class_="css-1ka7r5v")
            keywords = [str(a.get_text()) for a in all_a]
            return keywords
        return keywords
    
    def get_all_data(self):
        data = {}
        data['breadcrumb_category'] = self.get_breadcrumb_category()
        data['product_images_urls'] = self.get_product_images_urls()
        data['product_info'] = self.get_product_info()
        data['cordinate_product_info'] = self.get_cordinate_product_info()
        data['description'] = self.get_description()
        data['size_chart'] = self.get_size_chart()
        data['review_info'] = self.get_product_review_info()
        data['user_reviews'] = self.get_users_reviews()
        data['keywords'] = self.get_keywords()

        return data




def get_page_source(url):
    ua = UserAgent()
    user_agent = ua.random
    options = Options()
    options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    return driver.page_source



async def scrape_url(url):
    # page_source = await loop.run_in_executor(None, get_page_source, url)
    # print(type(page_source))
    with open('page.txt', 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')
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




