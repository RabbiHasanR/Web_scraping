import os
import time
import asyncio
import aiohttp
import requests
import pandas as pd
from urllib.parse import urlparse
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
from selenium.webdriver.common.keys import Keys

class WebScraper:
    def __init__(self, url):
        self.url = url
        ua = UserAgent()
        user_agent = ua.random
        options = Options()
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--start-maximized")
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def open_new_tab(self):
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + 't')
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def back_first_tab(self):
        self.driver.switch_to.window(self.driver.window_handles[0])


    def load_page(self, sleep=0):
        self.driver.get(self.url)
        try:
            body = self.driver.find_element(By.TAG_NAME,"body")
            body.send_keys(Keys.END)
            time.sleep(sleep)
        except NoSuchElementException as e:
            raise Exception(f'Something Went Wrong! {e}')

    
    def wait_for_product_deatils_page(self, second):
        try:
            # wait for the dynamic component to load
            WebDriverWait(self.driver, second).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.sizeDescription.section.css-w0j2zy > div'))
            )

            WebDriverWait(self.driver, second).until(
                EC.presence_of_element_located((By.ID, 'BVRRDisplayContentID'))
            )
        except TimeoutException as e:
            print('Timeout exception')
            # raise TimeoutException(f'Time out! {e}')
        
    def cordinate_product_info_scrap(self, second):
        try:
            cordinate_divs = WebDriverWait(self.driver, second).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.test-coordinate_item_tile'))
                )         

            cordinate_products = []
            for cordinate_div in cordinate_divs:
                cordinate_div.click()
                time.sleep(second) 
                try:
                    product_page_src = self.driver.find_element(By.CSS_SELECTOR, 'div.coordinate_item_container.test-coordinate_item_container.add-open > div > div.detail > div.image_wrapper > a').get_attribute('href')
                    product_image_url = self.driver.find_element(By.CSS_SELECTOR, 'img.coordinate_item_image').get_attribute('src')
                    product_name = self.driver.find_element(By.CSS_SELECTOR, 'span.titleWrapper').text
                    product_price = self.driver.find_element(By.CSS_SELECTOR, 'div.coordinate_item_container.test-coordinate_item_container.add-open > div > div.detail > div.info_wrapper > div.mdl-price.test-Type2.css-izzs0m > p > span').text
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
            print('cordinate products timeout exception!')
            return []

    def get_page_source(self):
        return self.driver.page_source

    def close_browser(self):
        self.driver.quit()


class Util:
    def __init__(self) -> None:
        pass

    def find_element_by_id(self, parent_element, tag_name, id):
        if parent_element:
            element = parent_element.find(tag_name, {"id": id})
            return element
        return None
    
    def find_element_by_class(self, parent_element, tag_name, class_name):
        if parent_element:
            element = parent_element.find(tag_name, class_=class_name)
            return element
        return None
    
    def find_element_by_tag(self, parent_element, tag_name):
        if parent_element:
            element = parent_element.find(tag_name)
            return element
        return None
    
    def find_elements_by_class(self, parent_element, tag_name, class_name):
        if parent_element:
            element = parent_element.find_all(tag_name, class_=class_name)
            return element
        return []
    
    def find_elements_by_tag(self, parent_element, tag_name):
        if parent_element:
            element = parent_element.find_all(tag_name)
            return element
        return []
    
    def get_text(self, element):
        if element:
            return str(element.get_text())
        return ''
    
    def get_attribute_value(self, element, attribute):
        if element and attribute:
            return element.get(attribute)
        return ''

    def get_src(self, element):
        if element:
            return element.get('src')
        return ''
    
    def get_href(self, element):
        if element:
            return element.get('href')
        return ''
    
    def join_url_path(self, url, path):
        return requests.compat.urljoin(url, path)

class NavigationPage:

    def __init__(self, url, source) -> None:
        self.url = url
        self.source = source
        self.soup = BeautifulSoup(source, 'html.parser')
        self.util = Util()


    def scrap_navigation_links(self):
        ul = self.util.find_element_by_class(self.soup, 'ul', 'lpc-ukLocalNavigation_itemList js-animetionTarget')
        a_tags = self.util.find_elements_by_tag(ul, 'a')
        links = [self.util.join_url_path(self.url, self.util.get_href(a)) for a in a_tags]
        return links
    

class ProductsPage:
    def __init__(self, url, source) -> None:
        self.url = url
        self.source = source
        self.soup = BeautifulSoup(source, 'html.parser')
        self.util = Util()

    
    def scrap_products_urls(self):
        container_div = self.util.find_element_by_class(self.soup, 'div', 'test-articleDisplay css-1yuo7po')
        product_divs = self.util.find_elements_by_class(container_div, 'div', 'itemCardArea-cards test-card css-dhpxhu')
        product_urls = []
        for product_div in product_divs:
            a_tag = self.util.find_element_by_tag(product_div, 'a')
            href_path = self.util.get_href(a_tag)
            if href_path:
                product_urls.append(self.util.join_url_path(self.url, href_path))
        return product_urls
    
    def scrap_products_next_page_url(self):
        next_buttons = self.util.find_elements_by_class(self.soup, 'li', 'arrowButton test-arrowButton test-next next test-active-link css-1bwzh30')
        next_tag = self.util.find_element_by_tag(next_buttons[0], 'a') if len(next_buttons) > 0 else None
        href_path = self.util.get_href(next_tag)
        next_page_link = self.util.join_url_path(self.url, href_path)
        return next_page_link
    

class ProductDetailsPage:
    def __init__(self,url, source, cordinate_products) -> None:
        self.url = url
        self.source = source
        self.cordinate_products = cordinate_products
        self.soup = BeautifulSoup(source, 'html.parser')
        self.util = Util()


    def scrap_breadcrumb_category(self):
        ul = self.util.find_element_by_class(self.soup, 'ul', 'test-breadcrumb')
        lis = self.util.find_elements_by_tag(ul, 'li')
        categories = [self.util.get_text(self.util.find_element_by_tag(li, 'a')) for li in lis]
        return categories
    
    def scrap_product_images_urls(self):
        ul = self.util.find_element_by_class(self.soup, 'ul', 'slider-list test-slider-list')
        img_tags = self.util.find_elements_by_tag(ul, 'img')
        images_urls = [self.util.join_url_path(self.url, self.util.get_text(img_tag)) for img_tag in img_tags]
        return images_urls
    
    def scrap_product_info(self):
        div = self.util.find_element_by_class(self.soup, 'div', 'articlePurchaseBox css-gxzada')
        category_name = self.util.get_text(self.util.find_element_by_class(div, 'span', 'categoryName test-categoryName'))
        product_name = self.util.get_text(self.util.find_element_by_class(div, 'h1', 'itemTitle test-itemTitle'))
        product_price = self.util.get_text(self.util.find_element_by_class(div, 'span', 'price-value test-price-value'))
        buttons = self.util.find_elements_by_class(div, 'button', 'sizeSelectorListItemButton')
        available_sizes = [self.util.get_text(button) for button in buttons]
        return {
            'category_name': category_name,
            'product_name': product_name,
            'product_price': product_price,
            'available_sizes': available_sizes
        }
    
    def scrap_description(self):
        div = self.util.find_element_by_class(self.soup, 'div', 'js-componentsTabTarget js-articlePromotion add-close css-62zuw8')
        description_title = self.util.get_text(self.util.find_element_by_class(div, 'h4', 'heading itemFeature test-commentItem-subheading'))
        general_description = self.util.get_text(self.util.find_element_by_class(div, 'div', 'commentItem-mainText test-commentItem-mainText'))
        lis = self.util.find_elements_by_class(div, 'li', 'articleFeaturesItem')
        general_itemization_description = [self.util.get_text(li) for li in lis]

        return {
                'description_title': description_title,
                'general_description': general_description,
                'general_itemization_description': general_itemization_description
            }
    
    def scrap_size_chart(self):
        div = self.util.find_element_by_class(self.soup, 'div', 'sizeChart test-sizeChart css-l7ym9o')
        tables = self.util.find_elements_by_class(div, 'table', 'sizeChartTable')
        table_length = len(tables)
        if table_length > 1:
            item_table = tables[0]
            item_table_ths = self.util.find_elements_by_class(item_table, 'th', 'sizeChartTHeaderCell test-combined_table_header')
            item_table_ths.pop(0)

            item_value_table = tables[1]
            item_value_trs = self.util.find_elements_by_class(item_value_table, 'tr', 'sizeChartTRow')
            size_names_tr = item_value_trs.pop(0)
            size_names_span = self.util.find_elements_by_tag(size_names_tr, 'span')
            size_names = [self.util.get_text(span) for span in size_names_span]

            size_chart = {}
            count = 0
            while count < len(item_table_ths) and count < len(item_value_trs):
                value = self.util.get_text(item_table_ths[count])
                values_span = self.util.find_elements_by_tag(item_value_trs[count], 'span')
                values = [self.util.get_text(span) for span in values_span]
                size_chart[value] = dict(zip(size_names, values))
                count += 1
            return size_chart
        return {}
    
    def scrap_special_function(self):
        special_functions = []
        divs = self.util.find_elements_by_class(self.soup, 'div', 'contents clearfix')
        for div in divs:
            page_link_div = self.util.find_element_by_class(div, 'div', 'item_part illustration')
            page_link = self.util.join_url_path(
                self.url,
                self.util.get_href(
                    self.util.find_element_by_tag(page_link_div, 'a')
                )
                
            )

            image_link = self.util.get_src(
                self.util.find_element_by_class(page_link_div, 'img', 'illustrationBody')
            )

            title = self.util.get_text(
                self.util.find_element_by_class(div, 'a', 'tecTextTitle')
            )

            description = self.util.get_text(
                self.util.find_element_by_class(div, 'div', 'item_part details')
            )
            special_functions.append(
                    {
                        'page_link': page_link,
                        'image_link': image_link,
                        'title': title,
                        'description': description
                    }
                )
        return special_functions


    def scrap_product_review_info(self):
        div = self.util.find_element_by_class(self.soup, 'div', 'BVRRQuickTakeCustomWrapper')
        rating = self.util.get_text(
            self.util.find_element_by_class(div, 'span', 'BVRRNumber BVRRRatingNumber')
        )
        number_of_review = self.util.get_text(
            self.util.find_element_by_class(div, 'span', 'BVRRNumber BVRRBuyAgainTotal')
        )
        recommended_rate = self.util.get_text(
            self.util.find_element_by_class(div, 'span', 'BVRRBuyAgainPercentage')
        )

        img_tags = self.util.find_elements_by_class(div, 'img', 'BVImgOrSprite')
        items_sence = [self.util.get_attribute_value(img, 'title') for img in img_tags]

        return {
                'rating': rating,
                'number_of_review': number_of_review,
                'recommended_rate': recommended_rate,
                'items_sence': items_sence
            }
    
    def scrap_users_reviews(self):
        div = self.util.find_element_by_id(self.soup, 'div', 'BVRRDisplayContentBodyID')
        all_review_divs = self.util.find_elements_by_class(div, 'div', 'BVRRContentReview')
        user_reviews = []
        for review_div in all_review_divs:
            rating = self.util.get_text(
                self.util.find_element_by_class(review_div, 'span', 'BVRRNumber BVRRRatingNumber')
            )
            date = self.util.get_text(
                self.util.find_element_by_class(review_div, 'span', 'BVRRValue BVRRReviewDate')
            )
            title = self.util.get_text(
                self.util.find_element_by_class(review_div, 'span', 'BVRRValue BVRRReviewTitle')
            )
            description = self.util.get_text(
                self.util.find_element_by_class(review_div, 'span', 'BVRRReviewText')
            )
            reviewer_id = self.util.get_text(
                self.util.find_element_by_class(review_div, 'span', 'BVRRNickname')
            )

            user_review = {
                    'rating': rating,
                    'date': date,
                    'title': title,
                    'description': description,
                    'reviewer_id': reviewer_id
                }

            user_reviews.append(user_review)
        return user_reviews
    
    def scrap_keywords(self):
        div = self.util.find_element_by_class(self.soup, 'div', 'test-category_link null css-vxqsdw')
        all_a = self.util.find_elements_by_class(div, 'a', 'css-1ka7r5v')
        keywords = [self.util.get_text(a) for a in all_a]
        return keywords
    

    def get_product_data(self):
        data = {}
        data['url'] = self.url
        data['breadcrumb_category'] = self.scrap_breadcrumb_category()
        data['product_images_urls'] = self.scrap_product_images_urls()
        data['product_info'] = self.scrap_product_info()
        data['cordinate_products'] = self.cordinate_products
        data['description'] = self.scrap_description()
        data['special_functions'] = self.scrap_special_function()
        data['size_chart'] = self.scrap_size_chart()
        data['review_info'] = self.scrap_product_review_info()
        data['user_reviews'] = self.scrap_users_reviews()
        data['keywords'] = self.scrap_keywords()

        return data



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
        webscraper = WebScraper(url)
        cordinate_products = webscraper.cordinate_product_info_scrap(second=3)
        webscraper.load_page(sleep=3)
        webscraper.wait_for_product_deatils_page(second=3)
        page_source = webscraper.get_page_source()
        product_detail_page = ProductDetailsPage(url, page_source, cordinate_products)
        dict_data = product_detail_page.get_product_data()
        return dict_data

    async def get_single_product_page_data_async(self, url):
        webscraper = WebScraper(url)
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
        webscraper = WebScraper(self.navigation_page_url)
        webscraper.load_page(sleep=0)
        page_source = webscraper.get_page_source()
        navigation_page = NavigationPage(self.navigation_page_url, page_source)
        navigation_urls = navigation_page.scrap_navigation_links()
        return navigation_urls
    
    def get_product_urls(self, url):
        webscraper = WebScraper(url)
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
                url = input("Enter a URL: ")
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


    
        
