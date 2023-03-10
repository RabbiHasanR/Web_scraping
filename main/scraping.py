import asyncio
import aiohttp
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

    def __init__(self, soup) -> None:
        self.soup = soup
        self.url = 'https://shop.adidas.jp/'

    
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
        # data['cordinate_product_info'] = self.get_cordinate_product_info()
        data['description'] = self.get_description()
        data['size_chart'] = self.get_size_chart()
        data['review_info'] = self.get_product_review_info()
        data['user_reviews'] = self.get_users_reviews()
        data['keywords'] = self.get_keywords()

        return data




# def get_page_source(url):
#     ua = UserAgent()
#     user_agent = ua.random
#     options = Options()
#     options.add_argument(f'user-agent={user_agent}')
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#     driver.get(url)
#     return driver.page_source



# async def scrape_url(url):
#     # page_source = await loop.run_in_executor(None, get_page_source, url)
#     # print(type(page_source))
#     with open('page.txt', 'r') as f:
#         contents = f.read()
#         soup = BeautifulSoup(contents, 'html.parser')
#         product_deatil_page = ProductDetailPage(soup, url)
#         print(product_deatil_page.get_all_data())

# async def main():
    # urls = [
    #         'https://shop.adidas.jp/products/H03740/', 
    #         'https://shop.adidas.jp/products/HB9386/',
    #         'https://shop.adidas.jp/products/B75806/', 
    #         'https://shop.adidas.jp/products/B75807/',
    #         'https://shop.adidas.jp/products/GW6173/',
    #         'https://shop.adidas.jp/products/IE9541/',
    #         'https://shop.adidas.jp/products/FZ6364/',
    #         'https://shop.adidas.jp/products/FZ6389/',
    #         'https://shop.adidas.jp/products/GW6173/',
    #         'https://shop.adidas.jp/products/ID4121/',
    #         'https://shop.adidas.jp/products/HQ8930/'
    #     ]
#     tasks = []
#     for url in urls:
#         task = asyncio.create_task(scrape_url(url))
#         tasks.append(task)
#     await asyncio.gather(*tasks)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())


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

def find_category(driver):
    try:
        categories_lis = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.breadcrumbListItem'))
            )
        categories = [li.text for li in categories_lis]
        return categories
    except TimeoutException:
        return []

def find_product_images_urls(driver):
    try:
        img_tags = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'img.test-main_image'))
            )
        images_urls = [img_tag.get_attribute('src') for img_tag in img_tags]
        return images_urls
    except TimeoutException:
        return []
    
def find_cordinate_products(driver):
    try:
        cordinate_divs = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.test-coordinate_item_tile'))
            )
        cordinate_products = []
        for cordinate_div in cordinate_divs:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(cordinate_div)
            )
            cordinate_div.click()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ' div.coordinate_item_container.test-coordinate_item_container.add-open'))
            )
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

        return cordinate_products
    except TimeoutException:
        return []
    
def find_product_info(driver):
    try:
        category_name = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.articlePurchaseBox.css-gxzada > div.articleInformation.css-itvqo3 > div.articleNameHeader.css-t1z1wj > a > span'))
            )
        
        name = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.articlePurchaseBox.css-gxzada > div.articleInformation.css-itvqo3 > div.articleNameHeader.css-t1z1wj > h1'))
            )
        
        price = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.articleInformation.css-itvqo3 > div.articlePrice.test-articlePrice.css-1apqb46 > p.price-text.test-price-text.mod-flat > span'))
            )
        product = {}

        product['category_name'] = category_name.text
        product['name'] = name.text
        product['price'] = price.text
        try:
            size_buttons = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul > li.sizeSelectorListItem> button'))
            )
            product['sizes'] = [button.text for button in size_buttons]
            return product
        except TimeoutException:
            return product
    except TimeoutException:
        return {}

def find_description(driver):
    try:
        description_div = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.js-componentsTabTarget.js-articlePromotion.add-close.css-62zuw8'))
                )
        descritpion = {}
        descritpion['title'] = driver.find_element(By.CSS_SELECTOR, 'div.js-componentsTabTarget.js-articlePromotion.add-close.css-62zuw8 > div > h4').text
        descritpion['general_description'] = driver.find_element(By.CSS_SELECTOR, 'div.commentItem-mainText.test-commentItem-mainText').text
        itemization_lis = driver.find_elements(By.CSS_SELECTOR, 'ul > li.articleFeaturesItem')
        descritpion['itemization_descriptions'] = [li.text for li in itemization_lis]
        return descritpion
    except TimeoutException:
        return {}
    
def find_size_table_chart(driver):
    try:
        print('find size table')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print('now bottom to top')
        driver.execute_script("window.scrollTo(0, 0);")
        size_table_div = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.sizeDescription.section.css-w0j2zy'))
                )
        size_items_ths = driver.find_elements(By.CSS_SELECTOR, 'table:nth-child(1) > thead > tr > th')
        size_items = [th.text for th in size_items_ths if th.text]
        size_names_tds = driver.find_elements(By.CSS_SELECTOR, 'table:nth-child(2) > tbody > tr:nth-child(1) > td')
        size_names = [td.text for td in size_names_tds if td.text]
        table_trs = driver.find_elements(By.CSS_SELECTOR, 'div > table:nth-child(2) > tbody > tr')
        table_trs.pop(0)

        size_chart = {}
        count = 0
        while count < len(size_items) and count < len(table_trs):
            value = size_items[count].text
            values_span = table_trs[count].find_elements(By.CSS_SELECTOR, 'td > span')
            values = [span.text for span in values_span]
            size_chart[value] = dict(zip(size_names, values))

            count += 1
        return size_chart
    except TimeoutException:
        return {}

def find_review_info(driver):
    try:
        rating_span = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '#BVRRRatingOverall_ > div.BVRRRatingNormalOutOf > span.BVRRNumber.BVRRRatingNumber'))
                    )
        total_review_span = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'span.BVRRValue.BVRRBuyAgain > span.BVRRNumber.BVRRBuyAgainTotal'))
                    )
        recommended_span = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.BVRRRatingPercentage > span.BVRRBuyAgainPercentage > span'))
                    )
        review_rating_of_each_item_imgs = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.BVRRSecondaryRatingsContainer > div.BVRRRatingContainerRadio > div.BVRRCustomRatingEntryWrapper > div.BVRRRatingEntry > div.BVRRRatingRadio > div.BVRRRatingRadioImage > img'))
                    )
        items_sence = [img.get_attribute('title') for img in review_rating_of_each_item_imgs]
        print('review info:',rating_span, total_review_span, recommended_span, items_sence)
        review_info = {}
        review_info['rating'] = rating_span.text
        review_info['number_of_review'] = total_review_span.text
        review_info['recommended_rate'] = recommended_span.text
        review_info['items_sence'] = items_sence
        return review_info
    except TimeoutException as e:
        print('TimeoutException:', e)
        return {}
    except Exception as e:
        print('exceptioN:', e)
        return {}
    

# async 

async def fetch_page_source_and_click_button(url):
    """Fetches the pagesource for a given URL and clicks a specific button"""
    ua = UserAgent()
    user_agent = ua.random
    options = Options()
    options.add_argument(f'user-agent={user_agent}')
    # options.add_argument("--kiosk")
    options.add_argument("--start-maximized")
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)  # create a new webdriver instance for each URL
    driver.implicitly_wait(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(0, 0);")
    driver.get(url)

    # result = {}
    # print('start')
    # find and click a specific button on the page
    # result['breadcrumb_category'] = find_category(driver)
    # result['product_images_urls'] = find_product_images_urls(driver)
    # result['cordinate_products'] = find_cordinate_products(driver)
    # result['product_info'] = find_product_info(driver)
    # result['description'] = find_description(driver)
    # result['size_chart'] = find_size_table_chart(driver)
    # result['review_info'] = find_review_info(driver)
        
    pagesource = driver.page_source
    driver.quit()
    return pagesource

async def get_multiple_pagesources_and_click_button():
    """Fetches pagesources for multiple URLs and clicks a specific button concurrently"""
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(fetch_page_source_and_click_button(url)) for url in urls]
        pagesources = await asyncio.gather(*tasks)
        return pagesources

async def scrape_file(pagesource):
    """Scrape a single HTML file and return the parsed BeautifulSoup object"""
    soup = BeautifulSoup(pagesource, 'html.parser')
    product_deatil_page = ProductDetailPage(soup)
    result = product_deatil_page.get_all_data()
    return result

async def scrape_files(pagesources):
    """Scrape multiple HTML files concurrently and return a list of parsed BeautifulSoup objects"""
    tasks = [asyncio.ensure_future(scrape_file(pagesource)) for pagesource in pagesources]
    soup_list = await asyncio.gather(*tasks)
    return soup_list

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    pagesources = loop.run_until_complete(get_multiple_pagesources_and_click_button())
    # print('results:', pagesources)
    if pagesources:
        soup_list = loop.run_until_complete(scrape_files(pagesources))
        print('final result:', soup_list)






