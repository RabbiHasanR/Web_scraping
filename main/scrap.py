import time
import json
import asyncio
import aiohttp
import requests
import pandas as pd
import concurrent.futures
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
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys



class ProductDetailPage:

    def __init__(self, soup) -> None:
        self.soup = soup
        self.url = 'https://shop.adidas.jp/'

    
    def get_breadcrumb_category(self):
        ul = self.soup.find('ul', class_="test-breadcrumb")
        if ul:
            lis = ul.find_all('li')
            categories = [str(li.a.get_text()) for li in lis]
            return categories
        return []
    
    def get_product_images_urls(self):
        ul = self.soup.find('ul', class_="slider-list test-slider-list")
        if ul:
            img_tags = ul.find_all('img')
            if len(img_tags) > 0:
                images_urls = [ requests.compat.urljoin(self.url, img_tag.get('src')) for img_tag in img_tags]
                return images_urls
            return []
        return []
    
    def get_product_info(self):
        div = self.soup.find('div', class_="articlePurchaseBox css-gxzada")
        if div:
            category_name = product_name = product_price = available_sizes = None
            category_span = div.find('span', class_="categoryName test-categoryName")
            name_h1 = div.find('h1', class_="itemTitle test-itemTitle")
            price_span = div.find('span', class_="price-value test-price-value")
            buttons = div.find_all('button', class_="sizeSelectorListItemButton")
            if category_span:
                category_name = str(category_span.get_text())
            if name_h1:
                product_name = str(name_h1.get_text())
            if price_span:
                product_price = str(price_span.get_text())
            if len(buttons) > 0:
                available_sizes = [str(button.get_text()) for button in buttons]
            return {'category_name': category_name, 'product_name': product_name, 'product_price': product_price, 'available_sizes': available_sizes}
        return {}
    
    # def get_cordinate_product_info(self):
    #     div = self.soup.find('div', class_="test-coordinate_item_container")
    #     if div:
    #         product_name = str(div.find('span', class_="title").get_text())
    #         product_page_src = str(div.find('a', class_="test-link_a").get('href'))
    #         product_number = str(product_page_src).split("/")[-2]
    #         product_price = str(div.find('span', class_="price-value test-price-salePrice-value").get_text())
    #         product_page_url = requests.compat.urljoin(self.url, product_page_src) 
    #         product_image_url = requests.compat.urljoin(self.url, div.find('img', class_="coordinate_item_image test-img").get('src')) 
    #         return {
    #             'product_name': product_name,
    #             'product_price': product_price,
    #             'product_page_url': product_page_url,
    #             'product_image_url': product_image_url,
    #             'product_number': product_number
    #         }
    #     return {}
    
    def get_description(self):
        div = self.soup.find('div', class_="js-componentsTabTarget js-articlePromotion add-close css-62zuw8")
        if div:
            description_title = general_description = general_itemization_description = None
            title_h4 = div.find('h4', class_="heading itemFeature test-commentItem-subheading")
            description_div = div.find('div', class_="commentItem-mainText test-commentItem-mainText")
            lis = div.find_all('li', class_="articleFeaturesItem")
            if title_h4:
                description_title = str(title_h4.get_text())
            if description_div:
                general_description = str(description_div.get_text())
            if lis:
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
            if len(tables) > 0:
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
        return {}
        
        

    def get_special_function(self):
        divs = self.soup.find_all('div', class_="contents clearfix")
        if divs:
            special_functions = []
            for div in divs:
                page_link = image_link = title = description = None
                page_link_div = div.find('div', class_="item_part illustration")
                if page_link_div:
                    page_link_a = page_link_div.find('a')
                    if page_link_a:
                        page_link = requests.compat.urljoin(self.url, page_link_a.get('href')) 
                    image_link_img = page_link_div.find('img', class_="illustrationBody")
                    if image_link_img:
                        image_link = image_link_img.get('src')
                
                title_a = div.find('a', class_="tecTextTitle")
                if title_a:
                    title = str(title_a.get_text())
                
                description_div = div.find('div', class_="item_part details")
                if description_div:
                    description = description_div.get_text()
                
                special_functions.append(
                    {
                        'page_link': page_link,
                        'image_link': image_link,
                        'title': title,
                        'description': description
                    }
                )
            return special_functions
        return []

    def get_product_review_info(self):
        div = self.soup.find('div', class_="BVRRQuickTakeCustomWrapper")
        if div:
            rating = number_of_review = recommended_rate = items_sence = None
            rating_span = div.find('span', class_="BVRRNumber BVRRRatingNumber")
            total_span = div.find('span', class_="BVRRNumber BVRRBuyAgainTotal")
            recomended_span = div.find('span', class_="BVRRBuyAgainPercentage")
            img_tags = div.find_all('img', class_="BVImgOrSprite")
            if rating_span:
                rating = str(rating_span.get_text())
            if total_span:
                number_of_review = str(total_span.get_text())
            if recomended_span:
                recommended_rate = str(recomended_span.get_text())
            if len(img_tags) > 0:
                items_sence = [img.get('title') for img in img_tags]

            return {
                'rating': rating,
                'number_of_review': number_of_review,
                'recommended_rate': recommended_rate,
                'items_sence': items_sence
            }
        return {}

    def get_users_reviews(self):
        div = self.soup.find('div', {"id": "BVRRDisplayContentBodyID"})
        if div:
            all_review_divs = div.find_all('div', class_="BVRRContentReview")
            user_reviews = []
            for review_div in all_review_divs:
                rating = date = title = description = reviewer_id = None
                rating_span = review_div.find('span', class_="BVRRNumber BVRRRatingNumber")
                date_span = review_div.find('span', class_="BVRRValue BVRRReviewDate")
                title_span = review_div.find('span', class_="BVRRValue BVRRReviewTitle")
                description_span = review_div.find('span', class_="BVRRReviewText")
                id_span = review_div.find('span', class_="BVRRNickname")

                if rating_span:
                    rating = str(rating_span.get_text())
                if date_span:
                    date = str(date_span.get_text())
                if title_span:
                    title = str(title_span.get_text())
                if description_span:
                    description = str(description_span.get_text())
                if id_span:
                    reviewer_id = str(id_span.get_text())

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
        return []
    
    def get_all_data(self):
        data = {}
        data['breadcrumb_category'] = self.get_breadcrumb_category()
        data['product_images_urls'] = self.get_product_images_urls()
        data['product_info'] = self.get_product_info()
        data['description'] = self.get_description()
        data['special_functions'] = self.get_special_function()
        data['size_chart'] = self.get_size_chart()
        data['review_info'] = self.get_product_review_info()
        data['user_reviews'] = self.get_users_reviews()
        data['keywords'] = self.get_keywords()

        return data
    


reviews_and_size_chart_urls = [
    'https://shop.adidas.jp/products/HK7339/',
    'https://shop.adidas.jp/products/IA6340/',
    'https://shop.adidas.jp/products/HY2729/',
    'https://shop.adidas.jp/products/HH9430/'
]

reviews_with_button = [
    'https://shop.adidas.jp/products/GZ5891/',
    'https://shop.adidas.jp/products/GZ5896/'
]

special_function = [
    'https://shop.adidas.jp/products/GZ3774/',
    'https://shop.adidas.jp/products/GZ3779/'
]

urls = [
            'https://shop.adidas.jp/products/HK7339/',


            # 'https://shop.adidas.jp/products/H03740/', 
            # 'https://shop.adidas.jp/products/HB9386/',

            # 'https://shop.adidas.jp/products/HB9386/',

            # 'https://shop.adidas.jp/products/HQ6900/',

            # 'https://shop.adidas.jp/products/EG1758/'



            # 'https://shop.adidas.jp/products/GV6905/'
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


def find_cordinate_products(driver):
    try:
        cordinate_divs = WebDriverWait(driver, 1).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.test-coordinate_item_tile'))
            )         

        cordinate_products = []
        for cordinate_div in cordinate_divs:
            cordinate_div.click()
            time.sleep(2) 
            try:
                product_page_src = driver.find_element(By.CSS_SELECTOR, 'div.coordinate_item_container.test-coordinate_item_container.add-open > div > div.detail > div.image_wrapper > a').get_attribute('href')
                product_image_url = driver.find_element(By.CSS_SELECTOR, 'img.coordinate_item_image').get_attribute('src')
                product_name = driver.find_element(By.CSS_SELECTOR, 'span.titleWrapper').text
                product_price = driver.find_element(By.CSS_SELECTOR, 'div.coordinate_item_container.test-coordinate_item_container.add-open > div > div.detail > div.info_wrapper > div.mdl-price.test-Type2.css-izzs0m > p > span').text
                cordinate_products.append(
                    {
                        'product_page_src': product_page_src,
                        'product_image_url': product_image_url,
                        'product_name': product_name,
                        'product_price': product_price
                    }
                )
            except:
                continue
        return cordinate_products
    except TimeoutException:
        return []

def write_in_spreadsheet(soup_list):
    # data = json.loads(soup_list)
    df = pd.DataFrame(soup_list)
    # df = df.set_index('url')
    df.to_excel('single_page.xlsx', index=False)
        

# async 

async def fetch_page_source(url):
    ua = UserAgent()
    user_agent = ua.random
    options = Options()
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--start-maximized")
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    cordinate_products = find_cordinate_products(driver)
    page_info = {'url': url, 'cordinate_products': cordinate_products}
    try:
        body = driver.find_element(By.TAG_NAME,"body")
        body.send_keys(Keys.END)
        time.sleep(10)
    except NoSuchElementException as e:
        pass

    try:
        # wait for the dynamic component to load
        size_chart_component = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.sizeDescription.section.css-w0j2zy > div'))
        )

        review_component = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, 'BVRRDisplayContentID'))
        )

        # for relaod reviews
        
        # reviews_reload_button = WebDriverWait(driver, 1).until(
        #         EC.presence_of_all_elements_located((By.CSS_SELECTOR, '//*[@id="BVRRDisplayContentFooterID"]/div/a'))
        #     ) 
        # reviews_reload_button.click()

        pagesource = driver.page_source
        driver.quit()
        page_info['pagesource'] = pagesource
        return page_info
    except TimeoutException as e:
        pagesource = driver.page_source
        driver.quit()
        page_info['pagesource'] = pagesource
        return page_info


async def get_multiple_pagesources():
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(fetch_page_source(url)) for url in urls]
        items = await asyncio.gather(*tasks)
        return items
    

async def scrape_file(item):
    soup = BeautifulSoup(item['pagesource'], 'html.parser')
    product_deatil_page = ProductDetailPage(soup)
    result = product_deatil_page.get_all_data()
    # print('result:', result)
    result['url'] = item['url']
    result['cordinate_products'] = item['cordinate_products']
    return result

async def scrape_files(items):
    tasks = [asyncio.ensure_future(scrape_file(item)) for item in items]
    soup_list = await asyncio.gather(*tasks)
    return soup_list






if __name__ == '__main__':
    start_time = time.time()
    print('start time:', start_time)
    loop = asyncio.get_event_loop()
    pagesources = loop.run_until_complete(get_multiple_pagesources())
    # json_string = json.dumps(pagesources)
    # with open('resultone.txt', 'w') as f:
    #     f.write(json_string)



    if pagesources:
        results = loop.run_until_complete(scrape_files(pagesources))
        json_string = json.dumps(results)
        with open('single_page.txt', 'w') as f:
            f.write(json_string)

        write_in_spreadsheet(results)

    end_time = time.time()
    print('end time:', end_time)
    execution_time = end_time - start_time

    print(f"Execution time: {execution_time:.2f} seconds")


