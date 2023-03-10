# selenium and chrome driver version check


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

options = Options()
# options.add_argument(f'user-agent={user_agent}')
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# str1 = driver.capabilities['browserVersion']
# str2 = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
# print(str1)
# print(str2)
# print(str1[0:2])
# print(str2[0:2])
# if str1[0:2] != str2[0:2]: 
#   print("please download correct chromedriver version")


import os
import time



driver.get("https://shop.adidas.jp/products/GV6905/")
# driver.implicitly_wait(30)
my_element = driver.find_element(By.XPATH,'//*[@id="__next"]/div/div[1]/div[4]/main/div/div/div[2]/div[3]/div[5]/div[2]/div[1]/div/div[1]/span/span[1]')
my_element.click()
time.sleep(2) 
