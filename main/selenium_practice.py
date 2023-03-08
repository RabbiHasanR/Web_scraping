from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from fake_useragent import UserAgent
ua = UserAgent()
user_agent = ua.random
 
options = Options()
# options.page_load_strategy = 'eager'
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

print('start')

website = 'https://shop.adidas.jp/products/HB9386/'
# website = 'https://www.adamchoi.co.uk/teamgoals/detailed'

# open Google Chrome with chromedriver
# driver.get(website)
driver.maximize_window()
driver.get(website)

cordinate_product = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[4]/main/div/div/div[2]/div[1]/div[2]/div[3]/div/div/div[1]/div/div[1]/ul/li/div')
cordinate_product.click()

# MAX_RETRIES = 4
# # Load the page
# retry_count = 0
# while retry_count < MAX_RETRIES:
#     try:
#         driver.get(website)
#         WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[1]/div[4]/main/div/div/div[2]/div[1]/div[2]/div[3]/div/div/div[1]/div/div[1]/ul/li/div')))
#         WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[1]/div[4]/main/div/div/div[5]/div[1]/div'))) 
#         break
#     except TimeoutException:
#         retry_count += 1
#         print(f"Failed to load the page. Retrying... ({retry_count}/{MAX_RETRIES})")

# if retry_count == MAX_RETRIES:
#     print("Failed to load the page after multiple retries.")
# else:
#     cordinate_product = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[4]/main/div/div/div[2]/div[1]/div[2]/div[3]/div/div/div[1]/div/div[1]/ul/li/div')
#     cordinate_product.click()
#     while retry_count < MAX_RETRIES:
#         try:
#             WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[1]/div[4]/main/div/div/div[2]/div[1]/div[2]/div[3]/div/div/div[2]/div')))
#             html = driver.page_source
#             # with open('page.txt', 'w') as f:
#             #     f.write(html)
#             print("Page loaded successfully!")
#             break
#         except TimeoutException:
#             retry_count += 1
#             print(f"Failed to load the page. Retrying... ({retry_count}/{MAX_RETRIES})")

# wait = WebDriverWait(driver, 300) # Wait for a maximum of 10 seconds
# element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[1]/div[4]/main/div/div/div[5]/div[1]/div')))
# driver.execute_script("arguments[0].scrollIntoView();", element)
# # element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[1]/div[4]/main/div/div/div[2]/div[1]/div[2]/div[3]/div/div/div[1]/div/div[1]/ul/li/div')))

# cordinate_product = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[4]/main/div/div/div[2]/div[1]/div[2]/div[3]/div/div/div[1]/div/div[1]/ul/li/div')
# cordinate_product.click()
# size_chart = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[4]/main/div/div/div[5]/div[1]')
# print('size chart:', size_chart)
# tables = size_chart.find_elements(By.TAG_NAME, 'table')
# print('tables:', tables)
# ths = tables[0].find_elements(By.TAG_NAME, 'th')
# print('ths:', ths)

# html = driver.page_source
# with open('page.txt', 'w') as f:
#     f.write(html)


# cordinate_product_button = driver.find_element(By.XPATH, '//div[@data-ga-event-category="pdp-coordinate"]')

# cordinate_product_button.click()



# div = driver.find_element(By.CLASS_NAME, "test-coordinate_item_container")

# product_name = div.find_element(By.CLASS_NAME, "title")
# # product_page_src = div.find_element(By.CLASS_NAME, "test-link_a")
# # product_number = product_page_src.split("/")[-1]
# product_price = div.find_element(By.CLASS_NAME, "price-value test-price-salePrice-value")
# # product_page_url = product_page_src
# product_image_url = div.find_element(By.CLASS_NAME, "coordinate_item_image test-img").get('src') 

# print(product_image_url, product_name, product_price)




# locate a button
# all_matches_button = driver.find_element(By.XPATH, '//label[@analytics-event="All matches"]')
# size_table = driver.find_element(By.XPATH, '//div[@data-gtm-vis-recent-on-screen-219692_603="18573"]')

# try:
#     wait = WebDriverWait(driver, 120) # Wait for a maximum of 10 seconds
#     element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[1]/div[4]/main/div/div/div[5]/div[1]')))
#     div = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[4]/main/div/div/div[5]/div[1]')
#     nested_div = div.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[4]/main/div/div/div[5]/div[1]/div')
#     tables = nested_div.find_elements(By.TAG_NAME, 'table')
#     print('element:', tables)
#     # html = driver.page_source
#     # with open('page.txt', 'w') as f:
#     #     f.write(html)
# except:
#     print('not found')

# print('size table', size_table)
# tables = driver.find_elements(By.CLASS_NAME, 'sizeChartTable')

# print('tables:', tables)

# items_table = tables[0]
# items_table_ths = items_table.find_elements(By.TAG_NAME, 'th')
# blank_th = items_table_ths.pop(0)

# items_value_table = tables[1]
# items_value_trs = items_value_table.find_elements(By.TAG_NAME, 'tr')
# size_names_tr = items_value_trs.pop(0)
# size_names_span = size_names_tr.find_elements(By.TAG_NAME, 'span')
# size_names = [span.text for span in size_names_span]
            
# size_chart = {}
# count = 0
# print('size chart:', size_names)
# print('size chart:', len(items_table_ths), len(items_value_trs))
# while count < len(items_table_ths) and count < len(items_value_trs):
#     print('count:', count)
#     value = str(items_table_ths[count].text)
#     values_span = items_value_trs[count].find_elements(By.TAG_NAME, 'span')
#     values = [str(span.text) for span in values_span]
#     size_chart[value] = dict(zip(size_names, values))
#     count += 1
# print('size chart value:', size_chart)
# click on a button
# all_matches_button.click()

# html = driver.page_source

# with open('page.txt', 'w') as f:
#     f.write(html)

# matches = driver.find_elements(By.TAG_NAME, 'tr')

# for match in matches:
#     print('match:', match.text)