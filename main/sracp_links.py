import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


MAIN_URL = 'https://shop.adidas.jp/men/'

MAIN_DOMAIN = 'https://shop.adidas.jp/'


def get_page_source(url):
    ua = UserAgent()
    user_agent = ua.random
    headers = {
        'User-Agent': user_agent
    }
    try:
        response = requests.get(url, headers)
        return response.text
    except:
        return None

def get_navigation_items_link(pagesource):
    soup = BeautifulSoup(pagesource, 'html.parser')
    ul = soup.find('ul', class_="lpc-ukLocalNavigation_itemList js-animetionTarget")
    a_tags = ul.find_all('a')
    links = [requests.compat.urljoin(MAIN_DOMAIN, a.get('href')) for a in a_tags]
    return links

def get_products_urls(pagesource):
    soup = BeautifulSoup(pagesource, 'html.parser')
    divs = soup.find_all('div', class_="itemCardArea-cards test-card")
    product_urls = []
    for div in divs:
        a_tag = div.find('a', class_="image_link test-image_link")
        product_urls.append(requests.compat.urljoin(MAIN_DOMAIN, a_tag.get('href')))
    next_buttons = soup.find_all('li', class_="arrowButton test-arrowButton test-next next test-active-link css-1bwzh30")
    next_tag =  next_buttons[0].find('a')
    next_page_link = requests.compat.urljoin(MAIN_DOMAIN,next_tag.get('href')) if next_tag else None
    result = {
        'total': len(product_urls),
        'next_page_link': next_page_link,
        'product_urls': product_urls
    }
    #  itemCardArea-cards test-card   productcardcssclass
    # viewSwitcher test-ViewSwitcher test-UpViewSwitcher mod-higher css-sxttxn     paginationdropdown
    # arrowButton test-arrowButton test-next next test-active-link css-1bwzh30   next arro butotn

    return result


def final_products(url):
    products = []
    final_url = url
    max_product = 300
    count = 0
    while count < max_product:
        if final_url:
            pagesource = get_page_source(final_url)
            if pagesource:
                result = get_products_urls(pagesource)
                count += result['total']
                products.append(result['product_urls'])
                final_url = result['next_page_link']
            else:
                continue
        break
    return {
        'total': len(products),
        'products': products
    }

product_urls = []

def web_crawler():
    pagesource = get_page_source(MAIN_URL)
    if pagesource:
        navigation_links = get_navigation_items_link(pagesource)
        print('navigation links:', navigation_links)
        for nav in navigation_links:
            pasesource = get_page_source(nav)
            result = get_products_urls(pasesource)
            print('result:', result)
        # results = []
        # for link in navigation_links:
        #     result = final_products(link)
        #     if result['total'] >= 300:
        #         results.append(result['products'])
        #         break
        #     else:
        #         results.append(result['products'])
        #         continue
    print('Not found')


web_crawler()